import cv2
import pycolmap
import poselib
import numpy as np
from pypopsift import popsift
import os


def extractFeatures(filename: os.path):
    config = {
        'sift_peak_threshold': 0.1,
        'sift_edge_threshold': 10.0,
        'feature_min_frames': 8000,
        'feature_use_adaptive_suppression': False,
    }

    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise IOError("Unable to load image {}".format(filename))

    print(image.shape)

    points, desc = popsift(image.astype(np.uint8),  # values between 0, 1
                            peak_threshold=config['sift_peak_threshold'],
                            edge_threshold=config['sift_edge_threshold'],
                            target_num_features=config['feature_min_frames'])

    print(points.shape)
    print(points)
    print(desc.shape)
    print(desc)

extractFeatures(os.path.join("..","data","captured_2022_08_27_19_28","1604_left.png"))