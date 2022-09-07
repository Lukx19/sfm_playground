from typing import List
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from nptyping import NDArray, Int, Shape, Float16


def PlotCamera(R, t, ax, scale=0.5, depth=0.5, faceColor="grey"):
    C = -t  # camera center (in world coordinate system)

    # Generating camera coordinate axes
    axes = np.zeros((3, 6))
    axes[0, 1], axes[1, 3], axes[2, 5] = 1, 1, 1

    # Transforming to world coordinate system
    axes = R.T.dot(axes) + C[:, np.newaxis]

    # Plotting axes
    ax.plot3D(xs=axes[0, :2], ys=axes[1, :2], zs=axes[2, :2], c="r")
    ax.plot3D(xs=axes[0, 2:4], ys=axes[1, 2:4], zs=axes[2, 2:4], c="g")
    ax.plot3D(xs=axes[0, 4:], ys=axes[1, 4:], zs=axes[2, 4:], c="b")

    # generating 5 corners of camera polygon
    pt1 = np.array([[0, 0, 0]]).T  # camera centre
    pt2 = np.array([[scale, -scale, depth]]).T  # upper right
    pt3 = np.array([[scale, scale, depth]]).T  # lower right
    pt4 = np.array([[-scale, -scale, depth]]).T  # upper left
    pt5 = np.array([[-scale, scale, depth]]).T  # lower left
    pts = np.concatenate((pt1, pt2, pt3, pt4, pt5), axis=-1)

    # Transforming to world-coordinate system
    pts = R.T.dot(pts) + C[:, np.newaxis]
    ax.scatter3D(xs=pts[0, :], ys=pts[1, :], zs=pts[2, :], c="k")

    # Generating a list of vertices to be connected in polygon
    verts = [
        [pts[:, 0], pts[:, 1], pts[:, 2]],
        [pts[:, 0], pts[:, 2], pts[:, -1]],
        [pts[:, 0], pts[:, -1], pts[:, -2]],
        [pts[:, 0], pts[:, -2], pts[:, 1]],
    ]

    # Generating a polygon now..
    ax.add_collection3d(
        Poly3DCollection(
            verts, facecolors=faceColor, linewidths=1, edgecolors="k", alpha=0.25
        )
    )


def PlotCameras(
    camsR: List[NDArray[Shape["3, 3"], Float16]],
    camsTrans: List[NDArray[Shape["3, 1"], Float16]]
):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    for R, t in zip(camsR, camsTrans):
        PlotCamera(R, t, ax)
