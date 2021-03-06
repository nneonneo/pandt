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

BASE_COLOR = 0x00ff00
# Insert points from calibration here.
points = [(44, 39), (48, 407), (413, 410), (415, 68)]
#points = [(186, 2), (195, 229), (500, 228), (500, 1)]#[(51, 50), (30, 264), (382, 265), (371, 15)]
warpmat = warpmatrix(points)

def depth11_cvt(depth):
    return ((depth >> 3) * 0x01010100 + 0xff)

# Refresh the colors to continue the fading process
def updateColors(time, times, sa):
        # Choose their color based on how long they've been on the board
        colors = BASE_COLOR - ((time - times) / 1000000)
        
        # Fill in the new colors 
        positives = (times > 0) & (colors > 0)
        sa[positives] = colors[positives].astype(np.int32)
        sa[positives == False] = 0
        times[positives == False] = 0
        del positives

if __name__ == '__main__':
    pygame.init()
    surf = pygame.display.set_mode((0, 0), pygame.DOUBLEBUF | pygame.FULLSCREEN)
    times = np.zeros( (640, 480), dtype=np.int32 )
    clock = pygame.time.Clock()
    running = True

    # Capture background depth, making a copy to avoid referencing
    # freenect's internal depth buffer
    backdepth, backdepth_ts = freenect.sync_get_depth(format=freenect.DEPTH_11BIT)
    backdepth = backdepth.copy()

    while running:
        clock.tick(70) # Run at 70 FPS (maximum)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.unicode == u'q'):
                running = False

        # XXX This is atypically complex code because of the extreme use of NumPy operations.

        # Grab a depth image
        depth, depth_timestamp = freenect.sync_get_depth(format=freenect.DEPTH_11BIT)
        time = np.int32(depth_timestamp)
        # Depth subtract (background should be farther than foreground objects,
        # so we subtract depth from backdepth)
        sub = backdepth - depth

        # Select those points which are between 10mm and 20mm in front of the background.
        # This captures most fingers nicely, while avoiding the constant +/- 5mm noise.
        txp = (backdepth != 0) & (depth != 0) & (sub > 10) & (sub < 20)
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
            # No indices to paint...
            updateColors(time, times, sa)
            pygame.display.flip()
            del sa
            continue
        ptst = ptst[..., valid_inds] # pick out only the points with valid indices

        # Convert [-1,1]*[-1,1] into window coords
        indx = ((ptst[0] + 1) * 320).astype(int)
        indy = ((ptst[1] + 1) * 240).astype(int)

        updateColors(time, times, sa)
        # Add the new pixels and update the screen
        sa[indx, indy] = BASE_COLOR
        times[indx, indy] = time
        del sa
        pygame.display.flip()
    pygame.quit()
