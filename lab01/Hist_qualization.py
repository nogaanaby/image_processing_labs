import skimage.io as io
import numpy as np
from skimage import exposure
import matplotlib.pyplot as plt



def ploth(hist,b_c):
    plt.figure(figsize=(10, 4))
    plt.bar(b_c, hist, width=1)
    plt.title('Histogram of the Image')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.show()



origin_img = io.imread('boat.png')
origin_hist, bin_centers = exposure.histogram(origin_img)
# ploth(origin_hist, bin_centers)


#cast to range 0-1: is it neccesary to do so for discreate hist qualization?
img_in_float_range = origin_img / 255.0
total_pixels=origin_img.sum()
float_hist, gray_scales = exposure.histogram(img_in_float_range)

# Normalize the histogram - instaed of pixel values I have the rare of each grayscale value
#  פונקציית הצפיפות = probability_mass= normalize histogram
total_pixels=float_hist.sum()
norm_hist = float_hist / total_pixels
y=np.linspace(0,1,256)
ploth(norm_hist, y)

# Calculate the cumulative sum (cumulative distribution function)
#original=[a, b, c, d]
#cumsum=[a, a+b, a+b+c, a+b+c+d]
#cdf=cumulative distribution function = פונקציית ההתפלגות המצטברת
cdf = np.cumsum(norm_hist)


avg_pixels_on_grayscales_in_the_normilize_hist=cdf[-1] / len(gray_scales)
ideal_hist= np.ones(gray_scales) * avg_pixels_on_grayscales_in_the_normilize_hist
ideal_cfd=np.cumsum(ideal_hist)




for i in range(0,len(gray_scales)):
    #empty lut
    LUT=np.ones(gray_scales)
    # look at the normalize_hist`s CDF in the first grayscale total pixels:
    # cdf[i]
    # and the ideal hist`s cdf:
    # ideal_cfd[i]


    # find the closest number to cdf[i] : ,[prev ,ideal_cfd[i-1] ,next ]
    #[
    # (index, ideal_val),
    # (0,40),
    # (1,80),
    # (2,80)
    # ]

    min_diff=np.argmin([
        #outbounds=> if i=0, so for the prev also you may take the first element
        np.abs(ideal_cfd[np.argmax([i-1,0])] - cdf[i]) ,
        np.abs(ideal_cfd[i] - cdf[i]) ,
        # outbounds=> if i=the end, so for the next also you may take the last element
        np.abs(ideal_cfd[np.argmin([i+1,len(gray_scales)-1])] - cdf[i])
    ])


    if min_diff==np.abs(ideal_cfd[np.argmax([i,0])] - cdf[i]):
        LUT[i]=cdf[ np.argmax([i-1,0]) ]
    elif min_diff == np.abs(ideal_cfd[i] - cdf[i]):
        LUT[i] = cdf[i]
    elif min_diff == np.abs(ideal_cfd[np.argmin([i,len(gray_scales)-1])] - cdf[i]):
        LUT[i] = cdf[ np.argmin([i+1,len(gray_scales)-1]) ]

    #check that you have no cross - > correct calculation
    if(i>0):
        if(LUT[i]<LUT[i-1]):
            raise("Wrong calculation! somthing went wrong!!")













# Histogram Equalization LUT (Look-Up Table)
HE_lut = cdf.astype(np.uint8)

# Apply the transformation: map the image through the LUT
HE_img = HE_lut[origin_img]

io.imsave('HE_img.png', HE_lut)

