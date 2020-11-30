import matplotlib.pyplot as plt
import nibabel as nib

FILENAME = "LungSeg.Obj.Airway.nii.gz"

img = nib.load(FILENAME).dataobj

plt.figure()
for i in range(int(img.shape[2]/5)):
    plt.imshow(img[:,:,i*5])
    plt.show()
