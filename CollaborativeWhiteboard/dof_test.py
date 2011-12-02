"""
Simple test app to display the depth and video images from a Kinect.
"""

import pygame
import freenect
import numpy as np
import Image # PIL

DEPTH_FORMAT = freenect.DEPTH_11BIT # freenect.DEPTH_REGISTERED

def dof_buckets(depth, sub):
    ''' return array masks corresponding to different depths '''
    masks = [(1, sub < 20)]
    prev = (sub < 20)
    for factor, stop in (
      #(1, 1),
      (1, 700),
      (6, 1200),
      (12, 1600),
      (20, 2300),
      (25, 3200),
      (30, 65536)):
        mask = depth < stop
        masks.append((factor, mask & ~prev))
        prev |= mask
    return masks

def dof_filter(image, masks):
    ''' filter image using dof masks '''
    ret = np.zeros((480, 640, 3), dtype=np.uint8)
    w, h = image.size
    for factor, mask in masks:
        smallim = image.resize((w//factor, h//factor), Image.NEAREST)
        # Remarkably, NEAREST actually has a decent effect.
        # It's also over 3 times faster than BILINEAR.
        blurim = smallim.resize((w, h), Image.NEAREST)
        np.add(ret, np.asarray(blurim) * mask.reshape((480, 640, 1)), ret)
    return ret

def to_surfimage(video):
    r = video[..., 2].astype(np.uint32) << 24
    g = video[..., 1].astype(np.uint32) << 16
    b = video[..., 0].astype(np.uint32) << 8
    return (r + g + b + 0xff)

def depth11_cvt(depth):
    return ((depth >> 4) * 0x01010100 + 0xff)

if __name__ == '__main__':
    pygame.init()
    surf = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    running = True

    # Capture background depth, making a copy to avoid referencing
    # freenect's internal depth buffer.
    backdepth, backdepth_ts = freenect.sync_get_depth(format=DEPTH_FORMAT)
    backdepth = backdepth.astype('int16')

    while running:
        clock.tick(70) # Run at 70 FPS (maximum)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.unicode == u'q'):
                running = False
            elif event.type == pygame.KEYDOWN and event.unicode == 'r':
                # Recalibrate
                backdepth, backdepth_ts = freenect.sync_get_depth(format=DEPTH_FORMAT)
                backdepth = backdepth.astype('int16')

        depth, depth_timestamp = freenect.sync_get_depth(format=DEPTH_FORMAT)

        # Depth subtract (background should be farther than foreground objects,
        # so we subtract depth from backdepth)
        sub = backdepth - depth

        masks = dof_buckets(depth, sub)

        video, video_timestamp = freenect.sync_get_video(format=freenect.VIDEO_RGB)
        videoim = Image.fromarray(video, mode='RGB')
        dof = dof_filter(videoim, masks)

        sa = pygame.surfarray.pixels2d(surf)
        sa[:640, :480] = to_surfimage(dof).transpose()
        del sa # unlock the surface by removing the array reference

        pygame.display.flip()
        print clock.get_fps()

    pygame.quit()
