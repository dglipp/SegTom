import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def isOverlapping(prevCenters, prevRads, center, rad):
    for i in range(len(prevCenters)):
        c = prevCenters[i]
        r = prevRads[i]
        d = np.sqrt((c[0]-center[0])**2 + (c[1] - center[1])**2)
        if (d<= r + rad) :
            return True
    return False

def isInBound(center,rad, img_size):
    return not ( center[0] - rad < 0 or 
        center[0] + rad > img_size or 
        center[1] - rad < 0 or 
        center[1] + rad > img_size)

def genCircles(n_circles, min_r, max_r, pad, img_size):
    centers = []
    rads = []
    while (len(centers) < n_circles) :
        center = np.random.rand(2, 1)*(img_size - pad*2) + pad
        rad = np.random.rand() * (max_r - min_r) + min_r
        if ( (not isOverlapping(centers, rads, center, rad)) and isInBound(center,rad,img_size)) :
            centers.append(center)
            rads.append(rad)
    return np.array(centers), np.array(rads)

def genImage(n_circles, min_r, max_r, min_int, max_int, img_size, pad, bbDispl):
    image = np.zeros((img_size, img_size, 1), dtype = "int16") - 1000
    centers,rads = genCircles(n_circles, min_r, max_r, pad, img_size)
    intensities = (np.random.rand(n_circles) * (max_int - min_int) + min_int).astype(np.int16)
    bounding_boxes = []

    for i in range(n_circles):
        c = np.reshape(centers[i,:], (2)).astype(int)
        r = int(rads[i])
        f = int(intensities[i])
        image = cv2.circle(image, tuple(c), r, f, -1)
        randDispl = int(np.random.rand()*bbDispl)
        downleft = (c[0] - r - randDispl, c[1] - r - randDispl)
        upright = (c[0] + r + randDispl, c[1] + r + randDispl)
        bb = (downleft, upright)
        bounding_boxes.append(bb)
        cv2.rectangle(image,bb[0], bb[1],max_int,1)
    return image, bounding_boxes

if(not os.path.isdir('./genImages')):
    os.mkdir('genImages')

# SETTINGS________________________________________________________

n_images = 10
max_circles=12
min_r=3
max_r=20
min_int=-500
max_int=1000
img_size=512
pad=max_r
max_displ = 4

# _________________________________________________________________

reg_list = []
for i in range(n_images):
    n_circles = int(np.random.rand()*max_circles)
    bb_displ = int(np.random.rand()*(max_displ - 1) + 1)
    plt.figure()
    image, bounding_boxes = genImage(n_circles, min_r, max_r,
    min_int, max_int, img_size, pad, bb_displ)
    plt.imshow(image[:,:,0], cmap='gray', vmin=-1000, vmax=1000)
    plt.savefig('genImages/id_'+str(i)+'.pdf')
    plt.close()

    dict1 = {}
    dict1.update({
        'filename': 'id_'+str(i)+'.pdf',
        'bounding_box': bounding_boxes
    })
    reg_list.append(dict1)

reg = pd.DataFrame(reg_list, columns=['filename', 'bounding_box'])

reg.to_pickle('genImages/data')
