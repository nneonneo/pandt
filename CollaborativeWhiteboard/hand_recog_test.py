#cv.NamedWindow('depth')
#cv.NamedWindow('rgb')
#
#while True:
#  (depth,_),(rgb,_)=freenect.sync_get_depth(),freenect.sync_get_video()
#  depth=depth.astype(numpy.uint8)
#  cv.ShowImage("depth",cv.fromarray(depth))
#  cv.ShowImage("rgb",cv.fromarray(rgb))


"""Sweeps throught the depth image showing 100 range at a time"""
import freenect
import cv
import math
import numpy as np
import numpy.ma as ma
import time
import frame_convert

def disp_rgb_masked(depthmask):
  video,_ = freenect.sync_get_video()
  masked_video = ma.masked_array(video,mask=depthmask).filled(0)
  cv.ShowImage('RGB',cv.fromarray(masked_video))
  return masked_video

def disp_thresh(lower, upper, show_masked_rgb=True):
  depth, timestamp = freenect.sync_get_depth()
  min_depth = depth.min()
  video,_ = freenect.sync_get_video()

  if show_masked_rgb:
    video = video.astype(np.uint8)
    depthmask = (255*np.logical_and(depth>lower,depth<upper)).reshape(480,640,1)
    depthmask = depthmask.astype(np.uint8)
    masked_video = video & depthmask
    #print reduce(lambda count, curr: curr>0 and count+1 or count,masked_video.flatten(),0)
    cv.ShowImage('RGB',frame_convert.video_cv(masked_video.reshape(480,640,3)))

  depth = 255 * np.logical_and(depth > lower, depth < upper)
  depth = depth.astype(np.uint8)
  image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),
                               cv.IPL_DEPTH_8U,
                               1)
  cv.SetData(image, depth.tostring(),
             depth.dtype.itemsize * depth.shape[1])

  canny = doCanny(image,150.0,200.0,7)
  templates = template_match(image,template)
  smoothed = smooth(canny)
  cv.ShowImage('Depth', image)
  return depth,canny,min_depth

def doCanny(img,lt=70.0,ht=140.0,a=3):
  if img.nChannels != 1:
    return false

  out = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
  cv.Canny(img, out, lt, ht, a)
  return out

def template_match(src,tmpl):
  method = 5
  size = (cv.GetSize(src)[0]-cv.GetSize(tmpl)[0]+1,cv.GetSize(src)[1]-cv.GetSize(tmpl)[1]+1)
  dst = [cv.CreateImage(size,32,1) for i in xrange(6)]
  copy = cv.CreateImage(cv.GetSize(src),8,1)
  cv.Copy(src,copy)
  for i in xrange(6):
    cv.MatchTemplate(src,tmpl,dst[i],i)
    #cv.Normalize(dst[i],dst[i],1,0,cv.CV_MINMAX)
  
  minVal,maxVal,minLoc,maxLoc = cv.MinMaxLoc(dst[method])
  threshVal = maxVal if method > 2 else minVal
  matchLoc = maxLoc if method > 2 else minLoc
  
  if threshVal > THRESH_MIN:
    cv.Rectangle(src,matchLoc,(matchLoc[0]+tmpl.height,matchLoc[1]+tmpl.width),(127,127,127,255),2,8,0)
    cv.SetImageROI(copy,(matchLoc[0],matchLoc[1],tmpl.width,tmpl.height))
    copy = doCanny(copy)
    fingerDetection(smooth(copy),(matchLoc[0],matchLoc[1]))

  return dst


#TODO extend template match to more than just one match

def fingerDetection(handsrc,offset=(0,0)):
  contour = cv.FindContours(handsrc, cv.CreateMemStorage(), cv.CV_RETR_EXTERNAL, cv.CV_LINK_RUNS)
  #cv.DrawContours(handsrc,contour,(255,127,127),(255,127,127),-1,cv.CV_FILLED,8)
  #cv.FillConvexPoly(handsrc,polys,(255,0,0))
  #do the finger detection
  retVal = []
  failcount = 0
  k_threshold = 10
  interval = 5

  for i in xrange(interval,len(contour)-interval):
    angle,cent = angle_centroid(contour[i-interval],contour[i],contour[i+interval])
    if angle < k_threshold and angle > 0:
      retVal.append(cent)
    else:
      failcount += 1

  for (x,y) in retVal:
    cv.Rectangle(handsrc,(x,y),(x+5,y+5),(127,127,127,255),2,8,0)


  cv.ShowImage('Templ',handsrc)
  del contour

def smooth(src):
  dst = cv.CreateImage(cv.GetSize(src),cv.IPL_DEPTH_8U,1)
  cv.Smooth(src,dst,cv.CV_GAUSSIAN,1,1,0)
  return dst

def angle_centroid(j,i,k):
  #the two vectors are IJ and IK
  ij = (i[0]-j[0],i[1]-j[1])
  ik = (k[0]-i[0],k[1]-i[1])
  
  len_ij = math.sqrt(ij[0]**2 + ij[1]**2)
  len_ik = math.sqrt(ik[0]**2 + ik[1]**2)
  dot = ij[0]*ik[0] + ij[1]*ik[1]

  if len_ij == 0 or len_ik == 0 or ij == ik:
    return 180, (0,0)
  
  costheta = dot/float(len_ij*len_ik)
  if costheta < -1 or costheta > 1:
    return 180, (0,0)
  theta = math.acos(dot/float(len_ij*len_ik))

  cent_x = (i[0]+j[0]+k[0])/3
  cent_y = (i[1]+j[1]+k[1])/3
  return theta * 180 / math.pi, (cent_x,cent_y)

#this is for if we flatten the pixels
def kCurvAngleCentroid(i,j,k,width,height):
  x1 = i % width
  y1 = i / width
  x2 = j % w
  y2 = j / w
  x3 = k % w
  y3 = k / w
  sqd12 = (x2-x1)**2+(y2-y1)**2
  sqd13 = (x3-x1)**2+(y3-y1)**2
  spd23 = (x2-x3)**2+(y2-y3)**2
  theta = math.acos((sqd13-sqd12-sqd23)/(-2*sqd12**0.5*sqd23**0.5))

  cent_x = (x1+x2+x3)/3
  cent_y = (y1+y2+y3)/3
  return theta * 180 / math.PI,y*width+x

#scales template to account for depth
def scaleTempl(ndepth):
  factor = float(tdepth)/float(ndepth)
  if factor == 0:
    return
  template = cv.CreateMat(int(tempM.rows * factor), int(tempM.cols * factor), cv.CV_8UC1)
  cv.Resize(tempM,template)


def reset():
  lower = 0
  upper = 100
  found = False

lower = 0
upper = 100
slice_width = 50
max_upper = 2048
THRESH_MIN = 0.60

#template information
tempM = cv.LoadImageM("hand-template.png",cv.CV_LOAD_IMAGE_GRAYSCALE)
template = cv.LoadImage("hand-template.png",cv.CV_LOAD_IMAGE_GRAYSCALE)
tdepth = 630

while True:
  depth,canny,lower = disp_thresh(lower, upper)
  upper = lower + slice_width
  scaleTempl((upper+lower)/2)
  key = cv.WaitKey(2)
  
  if key == 115:
    print 'saving hand-template.png'
    cv.SaveImage("hand-template.png",cv.fromarray(depth))
