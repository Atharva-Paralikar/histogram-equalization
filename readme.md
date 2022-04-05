## License
```
MIT License

Copyright (c) 2022 Atharva Paralikar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
## Author
Atharva Paralikar - M.Engg Robotics Student at University of Maryland, College Park

## Overview of Histogram Equalization
Histogram of an image represents the graphical representation of the intensity
distribution in a digital image. The horizontal axis of the graph represents the
intensities of the pixels, and the vertical axis represents the number of pixels. The left
side of the histograms represents the darker areas of the image, and the right side
represents the lighter area of the image.
In computer vision histograms are useful tools in thresholding. They can be analyzed
for peaks and valleys. These can be used for edge detection, segmentation, and other
operations.

1.1 Histogram Equalization
Histogram equalization is a technique in image processing of contrast adjustment
using image’s histogram. This method increases the global contrast of the image.
Histogram equalization accomplishes this by effectively spreading out the highly
populated intensity values which are used to degrade image contrast.

Steps to Equalize histogram:
a) The color image is split into three channels using cv2.split(). Each channel is
processed individually.
b) Calculate the Probability Mass Function (PMF) of the image pixels from the
histogram.
c) Calculate the cumulative Distribution function (CDF) for the pixel intensities.
d) Multiply the CDF by the (max intensity value -1) to get the new CDF values.
e) Multiply the original intensity values by the new CDF and map them over the
entire image.
f) The three equalized channels are then merged into color image using
cv2.merge().

1.2 Adaptive Histogram Equalization

Adaptive Histogram Equalization is an image processing technique used to improve
contrast in images. It differs from regular histogram equalization in the respect that it
computes histogram equalizations for distinct sections of images. It is more suitable
for improving the local contrast and enhancing edge definitions in each region. This method tends to overamplify noise hence a variant contrast limited adaptative
histogram equalization (CLAHE) is used which prevents this overamplification.

Steps for CLAHE:

a) The image is divided into 8x8 grid. And each tile is equalized separately.
b) This follows the same procedure as above except for one step.
c) Before the new CDF is calculated, the peaks in the histograms are clipped at a
certain threshold and then distributed evenly among other pixels.

## Steps to Run Code

1. Copy the repository
```
git clone --recursive https://github.com/Atharva-Paralikar/histogram-eq.git
```
2. Source the repository 
```
cd ~/histogram-eq
```
3. Run the package 
```
python3 HistogramEqualization.py
```
![Comparison](https://github.com/Atharva-Paralikar/histogram-eq/blob/master/docs/comparison.gif)
