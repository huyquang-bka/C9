from .detect_yolov5 import Detection
import cv2
import base64


def load_model():
    detector = Detection()
    detector.weights = "resources/Weights/yolov5l.pt"
    detector.classes = [2, 5, 7]
    detector.conf_thres = 0.2
    detector.imgsz = (640, 640)
    detector.device = "cpu"
    detector.half = False
    detector._load_model()
    return detector


def check_slot(bboxes, slots):
    slot_dict = {}
    for index, slot in enumerate(slots):
        is_busy = False
        x1, y1, x2, y2 = slot
        for bbox in bboxes:
            center_x = (bbox[0] + bbox[2]) / 2
            center_y = (bbox[1] + bbox[3]) / 2
            if x1 <= center_x <= x2 and y1 <= center_y <= y2:
                slot_dict[index + 1] = bbox
                is_busy = True
                break
        if not is_busy:
            slot_dict[index + 1] = False
    return slot_dict


def load_slot(slot_path):
    slots = []
    with open(slot_path, "r") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            slots.append([int(line[0]), int(line[1]), int(line[2]), int(line[3])])
    return slots

def draw_slot(img, slot, slot_dict):
    for key, value in slot_dict.items():
        x1, y1, x2, y2 = slot[key - 1]
        if value:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        else:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return img

def image_to_base64(image):
    image = cv2.imencode('.jpg', image)[1]
    image = base64.b64encode(image)
    return image.decode('utf-8')

def save_slot_to_txt(path, slot):
    with open(path, "w") as f:
        for key, value in slot.items():
            if value:
                status = 1
            else:
                status = 0
            f.write(f"{key} 70 {status} null\n")