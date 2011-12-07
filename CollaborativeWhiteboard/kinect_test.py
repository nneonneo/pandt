#!/usr/bin/env python
""" Simple test app to display the depth and video images from a Kinect """
import pygame
import freenect

def depth11_cvt(depth):
    return ((depth >> 3) * 0x01010100 + 0xff)

def rgb_cvt(video):
    r = video[..., 2].astype('uint32') << 24
    g = video[..., 1].astype('uint32') << 16
    b = video[..., 0].astype('uint32') << 8
    return (r + g + b + 0xff)

def ir8_cvt(video):
    return video.astype('uint32') * 0x01010100 + 0xff

def ir10_cvt(video):
    return ((video >> 2) * 0x01010100 + 0xff)

if __name__ == '__main__':
    pygame.init()
    surf = pygame.display.set_mode((1280, 480), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    running = True

    depthformat = freenect.DEPTH_11BIT
    videoformat = freenect.VIDEO_RGB
    depthfunc = depth11_cvt
    videofunc = rgb_cvt

    while running:
        clock.tick(70) # Run at 70 FPS (maximum)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.unicode == u'q'):
                running = False
            elif event.type == pygame.KEYDOWN:
                # Switch depth/video modes based on keypress
                if event.unicode == u'r':
                    depthformat = freenect.DEPTH_REGISTERED
                    depthfunc = depth11_cvt
                elif event.unicode == u't':
                    depthformat = freenect.DEPTH_11BIT
                    depthfunc = depth11_cvt
                elif event.unicode == u'i':
                    videoformat = freenect.VIDEO_IR_8BIT
                    videofunc = ir8_cvt
                elif event.unicode == u'u':
                    videoformat = freenect.VIDEO_RGB
                    videofunc = rgb_cvt

        sa = pygame.surfarray.pixels2d(surf)

        depth, depth_timestamp = freenect.sync_get_depth(format=depthformat)
        sa[:640, :480] = depthfunc(depth).transpose()

        video, video_timestamp = freenect.sync_get_video(format=videoformat)
        sa[640:, :480] = videofunc(video).transpose()

        del sa

        pygame.display.flip()

    pygame.quit()
