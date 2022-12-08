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
    path_save_txt = "main/C9_result.txt"
    slots = load_slot("resources/Slot/slot.txt")
    print("Number of slots: ", len(slots))
    list_file = natsort.os_sorted(os.listdir(path))
    
    ip = "202.191.56.104"
    port = 5518
    buffer_size = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((ip, port))
            print("Connected to server: ")
            print("*" * 50)
            break
        except:
            print("Can't connect to server")
            print("*" * 50)
            time.sleep(0.5)
            continue
    
    for fn in tqdm(list_file):        
        name = os.path.splitext(fn)[0]
        image_path = os.path.join(path, fn)
        img = cv2.imread(image_path)
        img_copy = img.copy()
        if img is None:
            continue
        bboxes = detector.detect(img)
        slot_dict = check_slot(bboxes, slots)
        image_process = draw_slot(img, slots, slot_dict)
        # for bbox in bboxes:
        #     x1, y1, x2, y2 = bbox[:4]
        #     center_x, center_y = int((x1 + x2) / 2), int((y1 + y2) / 2)
        #     cv2.circle(image_process, (center_x, center_y), 2, (0, 0, 255), 2)
        # cv2.imwrite("Output/base.jpg", img_copy)
        # cv2.imwrite("Output/process.jpg", image_process)
        cv2.imwrite(f"resources/Process/{fn}", image_process)
        save_slot_to_txt(path_save_txt, slot_dict)
        save_slot_to_txt(f"resources/Txt/{name}.txt", slot_dict)
        shutil.make_archive("main", "zip", "main")
        if not os.path.exists("main.zip"):
            # s.close()
            continue
        with open("main.zip", "rb") as f:
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                s.sendall(data)
                print("Send data at: ", datetime.now())
        os.remove("main.zip")
        # s.close()
        print("*" * 50)
        time.sleep(5)

if __name__ == "__main__":
    process()