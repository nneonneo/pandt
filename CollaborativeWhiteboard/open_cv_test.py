#!/usr/bin/env python
import cv
import tkFileDialog

##file = tkFileDialog.askopenfilename()
#capture1 = cv.CaptureFromCAM(0)
#cv.NamedWindow('a_window', cv.CV_WINDOW_AUTOSIZE)
##image = cv.LoadImage(file, cv.CV_LOAD_IMAGE_COLOR)
#image = cv.QueryFrame(capture1)
#dst = cv.CloneImage(image)
#cv.Not(image,dst)
#cv.ShowImage('a_window', dst)
#
#cv.WaitKey(10000)

capture = cv.CaptureFromCAM(0)
writer = cv.CreateVideoWriter("temp.mov", 0, 10, cv.GetSize(cv.QueryFrame(capture)),1)
count = 0
print cv.GetSize(cv.QueryFrame(capture))
while count < 250:
  image=cv.QueryFrame(capture)
  dst = cv.CloneImage(image)
  cv.Not(image,dst)
  cv.WriteFrame(writer,image)
  cv.ShowImage('Image_Window',dst)
  cv.WaitKey(2)

  count += 1
