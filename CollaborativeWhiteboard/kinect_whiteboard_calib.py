""" Crude whiteboard calibration routine.

The projected screen will turn green, then it will display the
Kinect's captured view. Click on the four corners of the projected
image (CCW from top-left corner) to define the projected region,
then copy the resulting output to kinect_whiteboard. """
import pygame
import numpy as np
import freenect
import time

def depth11_cvt(depth):
    return ((depth >> 3) * 0x01010100 + 0xff)

def rgb_cvt(video):
    r = video[..., 2].astype('uint32') << 24
    g = video[..., 1].astype('uint32') << 16
    b = video[..., 0].astype('uint32') << 8
    return (r + g + b + 0xff)

if __name__ == '__main__':
    pygame.init()
    surf = pygame.display.set_mode((0, 0), pygame.DOUBLEBUF | pygame.NOFRAME)
    clock = pygame.time.Clock()
    running = True

    # Fill display with an easy-to-identify green colour
    surf.fill((0, 255, 0))
    pygame.display.flip()

    # Give the Kinect time to update
    time.sleep(2)

    # Grab a video frame from the Kinect
    video, video_timestamp = freenect.sync_get_video(format=freenect.VIDEO_RGB)

    # Display the frame by copying it into the current surface
    sa = pygame.surfarray.pixels2d(surf)
    sa[:640, :480] = rgb_cvt(video).transpose()
    del sa
    pygame.display.flip()

    points = []

    # Calibration procedure:
    # Click on each corner of the projected (green) image, in the order
    # top-left, bottom-left, bottom-right, top-right (counter-clockwise from top-left).
    while running:
        clock.tick(70) # Run at 70 FPS (maximum)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.unicode == u'q'):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(event.pos)
                if len(points) == 4:
                    running = False

        for x, y in points:
            pygame.draw.circle(surf, (255, 0, 0), (x, y), 3)
        pygame.display.flip()
    pygame.quit()

    # Print the accumulated points here.
    # Copy those points to kinect_whiteboard.py.
    print "Calibration:", points
    yn = raw_input("Save calibration (y/n)? ")
    if yn == "y":
        with open("whiteboard_calib.txt", "w") as f:
            print >> f, points
        print "Calibration saved."
    else:
        print "Calibration not saved."
