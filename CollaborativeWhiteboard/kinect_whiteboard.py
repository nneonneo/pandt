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

def depth11_cvt(depth):
    return ((depth >> 3) * 0x01010100 + 0xff)

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
        if not valid_inds.any():
            # No indices to paint...
            continue
        ptst = ptst[..., valid_inds] # pick out only the points with valid indices

        # Convert [-1,1]*[-1,1] into window coords
        indx = ((ptst[0] + 1) * (w-1)/2).astype(int)
        indy = ((ptst[1] + 1) * (h-1)/2).astype(int)

        # Paint the whiteboard
        sa = pygame.surfarray.pixels2d(surf)
        sa[indx, indy] = 0xff00ff00
        del sa
        pygame.display.flip()

    pygame.quit()
