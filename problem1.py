import cv2
import numpy as np

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
	cv2.imshow("asd",image_out)
	cv2.waitKey(0)

# def adaptive_eq(image):
# 	h,w = image.shape
# 	tiles = []
# 	m = h//8
# 	n = h//8
# 	for i in range(0,w):
	


def main():
	image = cv2.imread("./docs/adaptive_hist_data/0.png")
	cv2.imshow("asda",image)
	heq(image)
	grayimg = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	# adaptive_eq(grayimg)
	
if __name__ == '__main__':
	main()