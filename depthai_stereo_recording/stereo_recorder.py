from depthai_sdk import Previews
from depthai_sdk.managers import PipelineManager, PreviewManager
import depthai as dai
import cv2
import argparse
import h5py
from PIL import Image
from datetime import datetime
import os


def toImgPIL(imgOpenCV):
    return Image.fromarray(imgOpenCV)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-pcl",
        "--pointcloud",
        help="enables point cloud convertion and visualization",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-static",
        "--static_frames",
        default=False,
        action="store_true",
        help="Run stereo on static frames passed from host 'dataset' folder",
    )
    args = parser.parse_args()

    save_path: os.path = os.path.join(
        "./", "data", "captured_" + datetime.utcnow().strftime("%Y_%m_%d_%H_%M")
    )
    os.makedirs(save_path, exist_ok=True)

    pipeline = dai.Pipeline()

    # Define sources and outputs
    monoLeft = pipeline.create(dai.node.MonoCamera)
    monoRight = pipeline.create(dai.node.MonoCamera)
    xoutLeft = pipeline.create(dai.node.XLinkOut)
    xoutRight = pipeline.create(dai.node.XLinkOut)

    xoutLeft.setStreamName("left")
    xoutRight.setStreamName("right")

    # Properties
    monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
    monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
    monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

    # Linking
    monoRight.out.link(xoutRight.input)
    monoLeft.out.link(xoutLeft.input)

    # Connect to device and start pipeline
    with dai.Device(pipeline) as device:
        device.readCalibration2().eepromToJsonFile(
            os.path.join(save_path, f"calibration.json")
        )
        # print(device.readFactoryCalibration().eepromToJson())
        # Output queues will be used to get the grayscale frames from the outputs defined above
        print(device.getDeviceInfo())
        qLeft: dai.DataOutputQueue = device.getOutputQueue(
            name="left", maxSize=4, blocking=False
        )
        qRight: dai.DataOutputQueue = device.getOutputQueue(
            name="right", maxSize=4, blocking=False
        )

        while True:
            # Instead of get (blocking), we use tryGet (non-blocking) which will return the
            # available data or None otherwise
            inLeft: dai.ImgFrame = qLeft.tryGet()
            inRight: dai.ImgFrame = qRight.tryGet()

            if inLeft is not None and inRight is not None:
                rightCV: cv2.Mat = inRight.getCvFrame()
                leftCV: cv2.Mat = inLeft.getCvFrame()
                cv2.imshow("right", rightCV)
                cv2.imshow("left", leftCV)

                if cv2.waitKey(100) == ord(" "):
                    leftPath = os.path.join(
                        save_path, f"{inLeft.getSequenceNum()}_left.png"
                    )
                    cv2.imwrite(leftPath, leftCV)

                    rightPath = os.path.join(
                        save_path, f"{inRight.getSequenceNum()}_right.png"
                    )
                    cv2.imwrite(rightPath, rightCV)

            if cv2.waitKey(1) == ord("q"):
                break


main()
