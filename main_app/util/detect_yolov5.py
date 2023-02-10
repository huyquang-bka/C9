import os
import time
import torch
from ..yolov5_module.models.common import DetectMultiBackend
from ..yolov5_module.utils.general import (
    check_img_size, non_max_suppression, scale_coords)
from ..yolov5_module.utils.augmentations import letterbox
import numpy as np
import cv2


class Detection:
    def __init__(self):
        self.weights = 'resources/Weight/face_v3.pt'
        self.imgsz = (640, 640)
        self.conf_thres = 0.25
        self.iou_thres = 0.45
        self.max_det = 1000
        self.device = 'cpu'
        self.classes = None
        self.agnostic_nms = True
        self.half = False
        self.dnn = False  # use OpenCV DNN for ONNX inference

    def _load_model(self):
        # Load model
        # self.device = select_device(self.device)
        if self.device == "cpu":
            arg = "cpu"
        else:
            arg = f"cuda:{self.device}"
        print(self.weights, self.classes,
              self.conf_thres, arg, self.imgsz)
        self.device = torch.device(arg)
        self.model = DetectMultiBackend(
            self.weights, device=self.device, dnn=self.dnn, fp16=self.half)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size(
            self.imgsz, s=self.stride)  # check image size

    def detect(self, image):
        image_copy = image.copy()
        bboxes = []
        im = letterbox(image, self.imgsz, stride=self.stride,
                       auto=self.pt)[0]  # resize
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)
        im = torch.from_numpy(im).to(self.device)
        im = im.half() if self.model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

        pred = self.model(im, augment=False, visualize=False)
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes,
                                   self.agnostic_nms, max_det=self.max_det)
        for i, det in enumerate(pred):
            if len(det):
                det[:, :4] = scale_coords(
                    im.shape[2:], det[:, :4], image_copy.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    x1, y1, x2, y2 = list(map(lambda x: max(0, int(x)), xyxy))
                    bboxes.append([x1, y1, x2, y2, int(cls), float(conf)])

        return bboxes

