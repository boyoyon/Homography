import cv2, sys
import numpy as np

font = cv2.FONT_HERSHEY_PLAIN
font_size = 1

left_click_pos_x = -1
left_click_pos_y = -1
flag_left_click = -1
flag_right_click = -1

WIDTH = 1024
HEIGHT = 768

def mouse_event(event, x, y, flags, param):
    
    global left_click_pos_x, left_click_pos_y
    global flag_left_click, flag_right_click
    
    if(event == cv2.EVENT_LBUTTONUP):
        left_click_pos_x = x
        left_click_pos_y = y
        flag_left_click = 1

    if(event == cv2.EVENT_RBUTTONUP):
        flag_right_click = 1

def usage(progName):
    print('%s executes homography' % progName)
    print('%s <src image>' % progName)

def drawMarkerAndText(image, points, idx):
    global font, font_size

    for i in range(idx):
        cv2.circle(image, (int(points[i][0]), int(points[i][1])), 3, (255, 0, 0), -1)
    
    if(idx == 0):
        text = 'click left top corner'
    elif(idx == 1):
        text = 'click left bottom corner'
    elif(idx == 2):
        text = 'click right bottom corner'
    else:
        text = 'click right top corner'
    cv2.putText(image, text, (10, 20),font, font_size, (255, 0, 0))
    print(text)

def main():

    global flag_left_click, flag_right_click

    argv = sys.argv
    argc = len(argv)
    
    usage(argv[0])
    
    if(argc < 2):
        quit()
    
    Scale = 1.0
    prevScale = -1.0
    
    print('Hit any key to abord')
    
    src = cv2.imread(argv[1])
    height, width = src.shape[:2]
    
    pts_src = np.zeros((4, 2))
    pts_dst = np.zeros((4, 2))
    
    clone1 = src.copy()
    text = 'click left top corner'
    cv2.putText(clone1, text, (10, 20),font, font_size, (255, 0, 0))
    cv2.imshow('src', clone1)
    cv2.setMouseCallback('src', mouse_event)
    print(text)
    
    idx = 0
    fUpdateScale = False
    
    while (idx < 4):
    
        key = cv2.waitKeyEx(10)
        
        if key == ord('-'):
            Scale *= 0.9
    
        elif key == ord('+'):
            Scale *= 1.1
    
        elif key != -1:
            break
    
        if Scale != prevScale:
            clone1 = cv2.resize(src, (int(width * Scale), int(height * Scale)))
            prevScale = Scale
            fUpdateScale = True
    
        if fUpdateScale:
            clone = clone1.copy()
            drawMarkerAndText(clone, pts_src, idx)
            cv2.imshow('src', clone)
            fUpdateScale = False
    
        if idx > 0 and flag_right_click != -1:
            idx -= 1
            flag_right_click = -1
            clone = clone1.copy()
            drawMarkerAndText(clone, pts_src * Scale, idx)
            cv2.imshow('src', clone)
    
        if idx < 4 and flag_left_click != -1:
            pts_src[idx][0] = float(left_click_pos_x) / Scale
            pts_src[idx][1] = float(left_click_pos_y) / Scale
            idx += 1
            clone = clone1.copy()
            drawMarkerAndText(clone, pts_src * Scale, idx)
            cv2.imshow('src', clone)
            flag_left_click = -1
    
    minX = np.min(pts_src[:,0])
    maxX = np.max(pts_src[:,0])
    
    minY = np.min(pts_src[:,1])
    maxY = np.max(pts_src[:,1])
   
    X = sorted(pts_src, key=lambda x:x[0])
    Y = sorted(pts_src, key=lambda x:x[1])

    left   = (X[0][0] + X[1][0]) // 2 + width // 2
    right  = (X[2][0] + X[3][0]) // 2 + width // 2
    top    = (Y[0][1] + Y[1][1]) // 2 + height // 2
    bottom = (Y[2][1] + Y[3][1]) // 2 + height // 2

    pts_dst[0] = (left,  top)
    pts_dst[1] = (left,  bottom) 
    pts_dst[2] = (right, bottom)
    pts_dst[3] = (right, top)
    
    print(pts_src, pts_dst)
    
    clone = src.copy()
    text = 'Hit any key to terminate'
    cv2.putText(clone, text, (10, 20),font, font_size, (255, 0, 0))
    cv2.imshow('src', clone)
    print(text)
    
    h, status = cv2.findHomography(pts_src, pts_dst)
    
    dst = cv2.warpPerspective(src, h, (width * 2, height * 2))
    dispW = int(width * Scale)
    dispH = int(height * Scale)
    dst2 = cv2.resize(dst, (dispW, dispH))

    cv2.imshow('dst', dst2)
    cv2.waitKey(0)
    
    cv2.imwrite('homography.png', dst)
    print('save homography.png')
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
