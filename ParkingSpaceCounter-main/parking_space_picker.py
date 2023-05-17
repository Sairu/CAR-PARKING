import cv2
import pickle
import os

IMAGE_PATH = 'Resources/carParkImg.png'
POSITIONS_FILE = 'Resources/car_park_pos'
WIDTH, HEIGHT = 107, 48

pos_list = []

# Add parking spaces currently in the file to the list
if os.path.isfile(POSITIONS_FILE):
    with open(POSITIONS_FILE, 'rb') as f:
        pos_list += pickle.load(f)


def mouse_click(events, x, y, flags, params):
    # Add parking space to list
    if events == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))
    # Remove space from list
    if events == cv2.EVENT_RBUTTONDOWN:
        i = 0
        while i < len(pos_list):
            x1, y1 = pos_list[i]
            if x1 < x < x1 + WIDTH and y1 < y < y1 + HEIGHT:
                pos_list[i], pos_list[-1] = pos_list[-1], pos_list[i]
                pos_list.pop()
                i -= 1
            i += 1


while True:
    img = cv2.imread(IMAGE_PATH)
    for pos in pos_list:
        cv2.rectangle(img, pos, (pos[0] + WIDTH, pos[1] + HEIGHT), (255, 0, 255), 2)
    cv2.imshow('Img', img)
    cv2.setMouseCallback('Img', mouse_click)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Dump parking spaces to a file
with open(POSITIONS_FILE, 'wb') as f:
    pickle.dump(pos_list, f)
cv2.destroyAllWindows()
