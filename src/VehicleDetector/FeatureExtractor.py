"""Feature Extractor class"""
import cv2
import numpy as np
# from skimage.feature import hog


class FeatureExtractor():
    """Feature Extractor"""

    def __init__(self):
        """Initialize feature extractor"""
        # Set hog extractor parameters
        self.hog_orientations = 18
        self.cell_size = (8, 8)
        self.block_size = (2, 2)

        self.spatial_size = (32, 32)
        self.histogram_bins = 64

    def get_features(self, img):
        """Return feature vector for given image"""
        YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

        ch1 = YCrCb[:, :, 0]
        ch2 = YCrCb[:, :, 1]
        ch3 = YCrCb[:, :, 2]

        hog1 = self.get_hog_features(ch1, feature_vec=False)
        hog2 = self.get_hog_features(ch2, feature_vec=False)
        hog3 = self.get_hog_features(ch3, feature_vec=False)

        # print(hog1.shape)
        # print(hog1.ravel().shape)

        hog_features = np.hstack((hog1.ravel(), hog2.ravel(), hog3.ravel()))

        # spatial_features = self.bin_spatial(YCrCb)
        # hist_features = self.color_hist(YCrCb)

        # stacked = np.hstack((hog_features.ravel())).ravel()

        return hog_features.ravel()

    def bin_spatial(self, img):
        """Resize given image to size and convert to a single horizontal array"""
        color1 = cv2.resize(img[:, :, 0], self.spatial_size).ravel()
        color2 = cv2.resize(img[:, :, 1], self.spatial_size).ravel()
        color3 = cv2.resize(img[:, :, 2], self.spatial_size).ravel()

        return np.hstack((color1, color2, color3))

    def color_hist(self, img):
        """Compute color channel histograms and combine into single array."""
        # Compute the histogram of the color channels separately
        channel1_hist = np.histogram(img[:, :, 0], bins=self.histogram_bins)
        channel2_hist = np.histogram(img[:, :, 1], bins=self.histogram_bins)
        channel3_hist = np.histogram(img[:, :, 2], bins=self.histogram_bins)
        # Concatenate the histograms into a single feature vector
        hist_features = np.concatenate((channel1_hist[0], channel2_hist[0], channel3_hist[0]))
        # Return the individual histograms, bin_centers and feature vector
        return hist_features

    def get_hog_features(self, img, vis=False, feature_vec=True):
        """Extract hog features for given image."""
        hog = cv2.HOGDescriptor(_winSize=(img.shape[1] // self.cell_size[1] * self.cell_size[1],
                                img.shape[0] // self.cell_size[0] * self.cell_size[0]),
                                _blockSize=(self.block_size[1] * self.cell_size[1],
                                self.block_size[0] * self.cell_size[0]),
                                _blockStride=(self.cell_size[1], self.cell_size[0]),
                                _cellSize=(self.cell_size[1], self.cell_size[0]),
                                _nbins=self.hog_orientations)
        hist = hog.compute(img)

        return hist

        # Call with two outputs if vis==True
        # if vis:
        #     features, hog_image = hog(img, orientations=self.hog_orientations,
        #                               pixels_per_cell=(self.pixel_per_cell, self.pixel_per_cell),
        #                               cells_per_block=(self.cells_per_block, self.cells_per_block),
        #                               transform_sqrt=False,
        #                               visualise=vis, feature_vector=feature_vec)
        #     return features, hog_image
        # # Otherwise call with one output
        # else:
        #     features = hog(img, orientations=self.hog_orientations,
        #                    pixels_per_cell=(self.pixel_per_cell, self.pixel_per_cell),
        #                    cells_per_block=(self.cells_per_block, self.cells_per_block),
        #                    transform_sqrt=False,
        #                    visualise=vis, feature_vector=feature_vec)
        # return features
