""" Simple test app to display the depth and video images from a Kinect """
import pygame
import freenect
import numpy as np
from scipy.misc import pilutil

def dof_buckets(depth):
    ''' return array masks corresponding to different depths '''
    masks = [(4, depth==0)]
    prev = depth == 0
    for i, stop in enumerate((600, 1000, 1400, 1800, 2200, 2600, 3000, 65535)):
        mask = depth < stop
        # Blur amount is (currently) just set to mask level
        masks.append((i*4+1, mask & ~prev))
        prev = mask
    return masks

def dof_filter(channel, masks):
    ''' filter image `channel' using dof masks '''
    accum = np.zeros_like(channel)
    for sigma, mask in masks:
        w, h = channel.shape
        small = pilutil.imresize(channel, (w//sigma, h//sigma))
        blurred = pilutil.imresize(small, (w, h))
        np.add(accum, blurred * mask, accum)
    return accum

def to_surfimage(r, g, b):
    r = r.astype('uint32') << 24
    g = g.astype('uint32') << 16
    b = b.astype('uint32') << 8
    return (r + g + b + 0xff)

if __name__ == '__main__':
    pygame.init()
    surf = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(70) # Run at 70 FPS (maximum)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.unicode == u'q'):
                running = False

        sa = pygame.surfarray.pixels2d(surf)

        depth, depth_timestamp = freenect.sync_get_depth(format=freenect.DEPTH_REGISTERED)
        masks = dof_buckets(depth)

        video, video_timestamp = freenect.sync_get_video(format=freenect.VIDEO_RGB)
        r = dof_filter(video[..., 2], masks)
        g = dof_filter(video[..., 1], masks)
        b = dof_filter(video[..., 0], masks)
        sa[:640, :480] = to_surfimage(r, g, b).transpose()

        del sa

        pygame.display.flip()
        print clock.get_fps()

    pygame.quit()
