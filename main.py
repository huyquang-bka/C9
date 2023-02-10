from datetime import datetime
from main_app.util.tools import load_model, load_slot, check_slot, draw_slot, save_slot_to_txt
import os
import cv2
import time
import natsort
import socket
import shutil
from tqdm import tqdm


def process():
    detector = load_model()
    path = "resources/Image"
    slots = load_slot("resources/Slot/slot.txt")
    print("Number of slots: ", len(slots))
    list_file = natsort.os_sorted(os.listdir(path))
    for fn in tqdm(list_file):        
        image_path = os.path.join(path, fn)
        img = cv2.imread(image_path)
        if img is None:
            continue
        bboxes = detector.detect(img)
        slot_dict = check_slot(bboxes, slots)
        image_process = draw_slot(img, slots, slot_dict)
        cv2.imshow("Image", image_process)
        key = cv2.waitKey(100)
        if key == 27:
            break

if __name__ == "__main__":
    process()