#!/usr/bin/env python
""" Crude whiteboard demo app.

Uses background-subtraction to detect interaction. It is therefore not
able to (easily) detect actual objects, only activated pixels. """
import pygame
import numpy as np
import freenect
import time

def warpmatrix(pts):
    """ Projectively map a quadrilateral onto a square. """
    z = np.zeros(3)
    p = [np.array((x,y,1)) for x,y in pts]

    # Solve the system of equations which takes the points of pts
    # to [(-1,-1),(-1,1),(1,1),(1,-1)].
    A = np.array([
        np.hstack((p[0], z, p[0])),
        np.hstack((z, p[0], p[0])),
        np.hstack((p[1], z, p[1])),
        np.hstack((z, p[1], -p[1])),
        np.hstack((p[2], z, -p[2])),
        np.hstack((z, p[2], -p[2])),
        np.hstack((p[3], z, -p[3])),
        np.hstack((z, p[3], p[3])),
        (0,0,0,0,0,0,0,0,1)
    ])
    b = [0,0,0,0,0,0,0,0,1]
    return np.reshape(np.linalg.solve(A,b), (3,3))

CUR_COLOR = 0x00ff00
CUR_STR = "g"
# Refresh the colors to continue the fading process
def updateColors(time, times, sa, colors):
        # Choose their color based on how long they've been on the board
        timeDiff = (time - times) / 500
        isPositive = 255 > timeDiff
        cols = 255 - timeDiff
        
        # Fill in the new colors 
        sa[(colors == "r") & isPositive] = cols[(colors == "r") & isPositive] * (256 * 256)
        sa[(colors == "g") & isPositive] = cols[(colors == "g") & isPositive] * 256
        sa[(colors == "b") & isPositive] = cols[(colors == "b") & isPositive]
        sa[isPositive == False] = 0
        times[isPositive == False] = 0
        colors[isPositive == False] = "n"

def depth11_cvt(depth):
    return ((depth >> 3) * 0x01010100 + 0xff)

def get_backdepth():
    '''
    Capture background depth, making a copy to avoid referencing
    freenect's internal depth buffer
    '''

    backdepth, backdepth_ts = freenect.sync_get_depth(format=freenect.DEPTH_11BIT)
    return backdepth.copy().astype(np.int16)

def set_kinect_angle(angle, device_index=0):
    # Clamp angle to [-30, 30]
    angle = min(angle, max(angle, -30), 30)
    print "Setting Kinect angle to", angle

    # We have to stop the synchronous runloop to interact with the device.
    freenect.sync_stop()

    # Open the device
    ctx = freenect.init()
    dev = freenect.open_device(ctx, device_index)

    # Set angle
    freenect.set_tilt_degs(dev, angle)

    # Shutdown context, allowing synchronous runloop to start
    freenect.shutdown(ctx)

    return angle

if __name__ == '__main__':
    try:
        with open("whiteboard_calib.txt", "r") as f:
            points = eval(f.read().strip())
    except IOError:
        print "Could not open whiteboard calibration; please run kinect_whiteboard_calib.py"
        exit(1)
    warpmat = warpmatrix(points)

    pygame.init()
    surf = pygame.display.set_mode((0, 0), pygame.DOUBLEBUF | pygame.FULLSCREEN)
    w, h = surf.get_size()
    times = np.zeros( (w, h), dtype=np.int32 )
    colors = np.array( [ [ "n" for j in xrange(h)] for i in xrange(w)] )

    clock = pygame.time.Clock()
    running = True

    angle = 15
    set_kinect_angle(angle)

    backdepth = get_backdepth()

    while running:
        clock.tick(70) # Run at 70 FPS (maximum)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.unicode == u'q'):
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode == u'c':
                    # Calibrate
                    backdepth = get_backdepth()
                elif event.key == pygame.K_BACKSPACE:
                    # Clear screen
                    surf.fill((0, 0, 0))
                elif event.unicode == u'a':
                    angle = set_kinect_angle(angle + 2)
                elif event.unicode == u'z':
                    angle = set_kinect_angle(angle - 2)
                elif event.unicode == u'r':
                    CUR_COLOR = 0xff0000
                    CUR_STR = "r"
                elif event.unicode == u'g':
                    CUR_COLOR = 0x00ff00
                    CUR_STR = "g"
                elif event.unicode == u'b':
                    CUR_COLOR = 0x0000ff
                    CUR_STR = "b"

        # XXX This is atypically complex code because of the extreme use of NumPy operations.

        # Grab a depth image
        depth, depth_timestamp = freenect.sync_get_depth(format=freenect.DEPTH_11BIT)
        time = pygame.time.get_ticks()

        # Depth subtract (background should be farther than foreground objects,
        # so we subtract depth from backdepth)
        sub = backdepth - depth.astype(np.int16)

        # Select those points which are between 10mm and 20mm in front of the background.
        # This captures most fingers nicely, while avoiding the constant +/- 5mm noise.
        txp = (backdepth != 0) & (depth != 0) & (sub > 10) & (sub < 16)
        # Convert the boolean mask txp into index arrays
        txpn = np.nonzero(txp)

        # Rearrange the index arrays to make homogenous window coordinates (x, y, 1.0)
        txpn = txpn[1], txpn[0], (1,)*len(txpn[0])

        # Warp the points to the whiteboard rectangle [-1,1]*[-1,1]
        ptst = warpmat.dot(txpn)
        ptst /= ptst[2]

        # Select only those points which actually lie in the square
        valid_inds = (ptst[0] > -1) & (ptst[0] < 1) & (ptst[1] > -1) & (ptst[1] < 1)
        sa = pygame.surfarray.pixels2d(surf)
        if not valid_inds.any():
            updateColors(time, times, sa, colors)
            del sa
            pygame.display.flip()
            # No indices to paint...
            continue

        ptst = ptst[..., valid_inds] # pick out only the points with valid indices

        print "Valid drawing points"
        print ptst

        # Convert [-1,1]*[-1,1] into window coords
        indx = ((ptst[0] + 1) * (w-1)/2).astype(int)
        indy = ((ptst[1] + 1) * (h-1)/2).astype(int)

        # Paint the whiteboard
        updateColors(time, times, sa, colors)
        sa[indx, indy] = CUR_COLOR
        times[indx, indy] = time
        colors[indx, indy] = CUR_STR
        del sa
        pygame.display.flip()

    pygame.quit()
