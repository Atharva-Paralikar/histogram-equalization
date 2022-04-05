import cv2
import numpy as np
from collections import OrderedDict

def get_pmf(image):
	pmf = [0]*256
	pmf_data = []
	h,w = image.shape
	a = h*w
	for i in range(h):
		for j in range(w):
			pixel_data = image[i][j]
			pmf[pixel_data] = pmf[pixel_data] + 1
	for x in pmf:
		pmf_data.append(x/a)
	return pmf_data

def get_cdf(image):	
	pmf = get_pmf(image)
	cdf =[]
	prev_pmf = 0
	for x in pmf:
		curr_cdf = x + prev_pmf
		cdf.append(curr_cdf)
		prev_pmf = curr_cdf
	return cdf

def equalized_histogram(image):
	h,w = image.shape
	cdf = get_cdf(image)
	for i in range(h):
		for j in range(w):
			image[i][j] = int(255*cdf[image[i][j]])
	return image

def heq(image):
	B,G,R = cv2.split(image)
	B_eq = equalized_histogram(B)
	G_eq = equalized_histogram(G)
	R_eq = equalized_histogram(R)
	image_out = cv2.merge((B_eq,G_eq,R_eq))
	return image_out

def histogram(image):
	pixels, count = np.unique(image, return_counts=True)
	hist = OrderedDict()
	for i in range(len(pixels)):
		hist[pixels[i]] = count[i]
	return np.array(list(hist.values())), np.array(list(hist.keys()))

def clip_histogram(hist,bins):
	n_bins = len(bins)
	excess = 0
	clip_limit = 40
	for i in range(n_bins):
		if hist[i] > clip_limit:
			excess += hist[i] - clip_limit
			hist[i] = clip_limit
	for_each_bin = excess // n_bins
	leftover = excess % n_bins

	hist += for_each_bin
	for i in range(leftover):
		hist[i] += 1
	return hist

def cdf(hist,bins):
	pixel_probability = hist / hist.sum()
	cdf = np.cumsum(pixel_probability)
	cdf_normalized = cdf * 255
	hist_eq = {}
	for i in range(len(cdf)):
		hist_eq[bins[i]] = int(cdf_normalized[i])

	return hist_eq

def adaptive_equalized_histogram(image):
	h,w = image.shape
	equalized_image = np.zeros((h,w),dtype = np.uint8)
	hist, bins = histogram(image)
	clipped_hist = clip_histogram(hist, bins)
	cdf1 = cdf(hist, bins)
	for i in range(h):
		for j in range(w):
			equalized_image[i][j] = cdf1[image[i][j]]
	return equalized_image

def adaptive_heq(image):
	B,G,R = cv2.split(image)
	B_eq = adaptive_equalized_histogram(B)
	G_eq = adaptive_equalized_histogram(G)
	R_eq = adaptive_equalized_histogram(R)
	image_out = cv2.merge((B_eq,G_eq,R_eq))
	return image_out

def adaptive_eq(image):
	tiles = []
	imagex = image[:370,:]
	h,w = imagex.shape[0],imagex.shape[1]
	grid_size = 8
	vstack=[]
	for i in range(0,grid_size):
		for j in range(0,grid_size):
			tile = imagex[i*(h//8):(i+1)*h//8, j*(w//8):(j+1)*w//8]
			tiles.append(tile)
	for tile in tiles:
		tile = adaptive_heq(tile)
	image_set1 = tiles[0:8]
	image_set1 = np.concatenate((image_set1),axis = 1)
	image_set2 = tiles[8:16]
	image_set2 = np.concatenate((image_set2),axis = 1)
	image_set3 = tiles[16:24]
	image_set3 = np.concatenate((image_set3),axis = 1)
	image_set4 = tiles[24:32]
	image_set4 = np.concatenate((image_set4),axis = 1)
	image_set5 = tiles[32:40]
	image_set5 = np.concatenate((image_set5),axis = 1)
	image_set6 = tiles[40:48]
	image_set6 = np.concatenate((image_set6),axis = 1)
	image_set7 = tiles[48:56]
	image_set7 = np.concatenate((image_set7),axis = 1)
	image_set8 = tiles[56:64]
	image_set8 = np.concatenate((image_set8),axis = 1)
	vstack = (image_set1,image_set2,image_set3,image_set4,image_set5,image_set6,image_set7,image_set8)
	image_out = np.concatenate((vstack),axis = 0)

	return image_out[:370,:]

def videowrite():
	image = cv2.imread("./docs/frames/1.jpg")
	h,w,l = image.shape
	size = (w,h)
	video = cv2.VideoWriter("./comparison.mp4",cv2.VideoWriter_fourcc(*'mp4v'),3,size)
	print("generating video...")
	for i in range(0,24):
		img = cv2.imread("./docs/frames/"+str(i)+".jpg")
		video.write(img)
	video.release()

def main():

	for i in range(24):
		image = cv2.imread("./docs/adaptive_hist_data/"+str(i)+".png")
		he = heq(image)
		cv2.putText(he," Normal Histogram Equalization",(300,220),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA,False)
		ahe = adaptive_eq(image)
		cv2.putText(ahe," Adaptive Histogram Equalization",(300,220),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA,False)
		final = np.concatenate((image,he,ahe),axis = 0)
		cv2.putText(final,"Original",(500,220),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA,False)
		cv2.imwrite("./docs/frames/"+str(i)+".jpg",final)
		print("Current Frame: ",i+1,end = '\r')
	videowrite()

if __name__ == '__main__':
	main()
