""" Simple test app to display the depth and video images from a Kinect """
import pygame
import freenect
import numpy as np
import Image

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

def dof_filter(image, masks):
    ''' filter image using dof masks '''
    ret = np.zeros((480, 640, 3), dtype=np.uint8)
    w, h = image.size
    for factor, mask in masks:
        smallim = image.resize((w//factor, h//factor), Image.NEAREST)
        blurim = smallim.resize((w, h), Image.NEAREST)
        np.add(ret, np.asarray(blurim) * mask.reshape((480, 640, 1)), ret)
    return ret

def to_surfimage(video):
    r = video[..., 2].astype(np.uint32) << 24
    g = video[..., 1].astype(np.uint32) << 16
    b = video[..., 0].astype(np.uint32) << 8
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

        depth, depth_timestamp = freenect.sync_get_depth(format=freenect.DEPTH_REGISTERED)
        masks = dof_buckets(depth)

        video, video_timestamp = freenect.sync_get_video(format=freenect.VIDEO_RGB)
        videoim = Image.fromarray(video, mode='RGB')
        dof = dof_filter(videoim, masks)

        sa = pygame.surfarray.pixels2d(surf)
        sa[:640, :480] = to_surfimage(dof).transpose()
        del sa # unlock the surface by removing the array reference

        pygame.display.flip()
        print clock.get_fps()

    pygame.quit()
