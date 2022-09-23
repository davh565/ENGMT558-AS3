# import the necessary packages
# https://pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/
import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import colorsys

def get_colour(clusters, input):
    im = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
    # im = input
    # plt.figure()
    # plt.axis("off")
    # plt.imshow(im)
    im_pixels = im.reshape((im.shape[0] * im.shape[1], 3))
    clt = KMeans(n_clusters=clusters)
    clt.fit(im_pixels)
    rgb_colours = clt.cluster_centers_/255
    hsl_colours = [colorsys.rgb_to_hls(*rgb) for rgb in rgb_colours]
    # print(rgb_colours)
    hues = [int(360*hsl[0]) for hsl in hsl_colours]
    if any(i >= 120 and i <= 150 for i in hues): 
        return("green")
    else: 
        return("red")
    
    print(hues)
    # for colour in hsl_colours:
        
    score_colours = []
    for colour in hsl_colours:
        score_colours.append(colour[1]*colour[2])
    hi_score_index = np.array(score_colours).argmax()
    hi_score_colour = clt.cluster_centers_[hi_score_index]
    return '#{:02x}{:02x}{:02x}'.format(int(hi_score_colour[0]),int(hi_score_colour[1]),int(hi_score_colour[2]))

def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	# return the histogram
	return hist

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
			color.astype("uint8").tolist(), -1)
		startX = endX
	
	# return the bar chart
	return bar