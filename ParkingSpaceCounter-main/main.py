import cv2
import pickle
import numpy as np
import os

WIDTH, HEIGHT = 107, 48
VIDEO_PATH = 'Resources/carPark.mp4'
POSITIONS_FILE = 'Resources/car_park_pos'


def draw_counter(image, text, position, scale=3, thickness=5, offset=20, text_color=(255, 255, 255),
                 rect_color=(0, 200, 0), font=cv2.FONT_HERSHEY_PLAIN):
    x, y = position
    (w, h), _ = cv2.getTextSize(text, font, scale, thickness)
    x1, y1, x2, y2 = x - offset, y + offset, x + w + offset, y - h - offset
    cv2.rectangle(image, (x1, y1), (x2, y2), rect_color, cv2.FILLED)
    cv2.putText(image, text, (x, y), font, scale, text_color, thickness)

    return image, [x1, y2, x2, y1]


def check_spaces(image, positions, threshold=900):
    # Process the image
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_thresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)
    space_counter = 0
    for pos in positions:
        x, y = pos
        img_crop = img_dilate[y:y + HEIGHT, x:x + WIDTH]
        count = cv2.countNonZero(img_crop)
        if count < threshold:
            color = (0, 255, 0)
            space_counter += 1
        else:
            color = (0, 0, 255)

        cv2.rectangle(image, pos, (pos[0] + WIDTH, pos[1] + HEIGHT), color, 2)
    draw_counter(image, f'{space_counter}/{len(positions)} free spaces', (100, 50))


pos_list = []
if os.path.isfile(POSITIONS_FILE):
    with open(POSITIONS_FILE, 'rb') as f:
        pos_list += pickle.load(f)
else:
    raise FileNotFoundError('Run parking_space_picker.py first')

# Video feed
cap = cv2.VideoCapture(VIDEO_PATH)

while pos_list:
    # Restart the video
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == cap.get(cv2.CAP_PROP_POS_FRAMES):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    check_spaces(img, pos_list)
    cv2.imshow("Img", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

