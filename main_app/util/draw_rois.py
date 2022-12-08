import cv2

path = "/Users/huyquang/huyquang/SelfProject/DemoC9/Output/base.jpg"
scale = 0.5
image = cv2.imread(path)
image = cv2.resize(image, dsize=None, fx=scale, fy=scale)
cv2.namedWindow("image")

rois = cv2.selectROIs("image", image, False, False)
print(rois)

for roi in rois:
    x, y, w, h = roi
    x1, y1, x2, y2 = x, y, x + w, y + h
    x1, y1, x2, y2 = list(map(lambda x: int(x / scale), [x1, y1, x2, y2]))
    with open("slot_2.txt", "a") as f:
        f.write(f"{x1},{y1},{x2},{y2}\n")