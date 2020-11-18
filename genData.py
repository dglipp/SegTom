import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

def genCircles(n_circles, min_r, max_r, pad):
    return
def genImage(n_circles, min_r, max_r, min_int, max_int, img_size, pad, bbDispl):
    image = np.zeros((512, 512, 1), dtype = "int16") - 1000
    centers = (np.random.rand(n_circles, 2)*(img_size - pad*2) + pad).astype(int)
    rads = (np.random.rand(n_circles) * max_r).astype(int)
    intensities = (np.random.rand(n_circles) * (max_int - min_int) + min_int).astype(np.int16)

    for i in range(n_circles):
        c = centers[i,:]
        r = rads[i]
        f = int(intensities[i])
        image = cv2.circle(image, tuple(c), r, f, -1)
        randDispl = int(np.random.rand()*bbDispl)
        downleft = (c[0] - r - randDispl, c[1] - r - randDispl)
        upright = (c[0] + r + randDispl, c[1] + r + randDispl)
        bb = (downleft, upright)
        cv2.rectangle(image,bb[0], bb[1],max_int,1)
    return image

plt.imshow(genImage(12, 3, 50, -1000, 1000, 512, 20, 4)[:,:,0], cmap='gray', vmin=-1000, vmax=1000)
plt.show()