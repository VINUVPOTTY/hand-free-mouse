import cv2
import mediapipe as mp
import pyautogui
import time
import math

mphands = mp.solutions.hands
hand = mphands.Hands(max_num_hands=1)
video = cv2.VideoCapture(0)
action_cooldown = 0.8  # seconds
last_action_time = 0

tipid = [4, 8, 12, 16, 20]
screen_w, screen_h = pyautogui.size()

while True:
    suc, img = video.read()
    img = cv2.flip(img, 1)  # Flip the camera for natural movement
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = hand.process(img1)
    lmlist = []

    if res.multi_hand_landmarks:
        for handLms in res.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * img.shape[1]), int(lm.y * img.shape[0])
                lmlist.append((id, cx, cy, lm.x, lm.y))  # Add normalized x, y for screen mapping

            # Draw a red circle at point 8 (index fingertip)
            if len(lmlist) > 8:
                cv2.circle(img, (lmlist[8][1], lmlist[8][2]), 15, (0, 0, 255), -1)
                # Move mouse to fingertip position (using normalized coordinates)
                mouse_x = int(lmlist[8][3] * screen_w)
                mouse_y = int(lmlist[8][4] * screen_h)
                pyautogui.moveTo(mouse_x, mouse_y, duration=0.1)
                # Click if thumb tip and index tip are close (use pixel coordinates for distance)
                thumb_tip = lmlist[4][1], lmlist[4][2]
                index_tip = lmlist[8][1], lmlist[8][2]
                distance = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])
                if distance < 40 and (time.time() - last_action_time) > action_cooldown:
                    pyautogui.click()
                    print("Clicked (thumb and index touch) at:", mouse_x, mouse_y)
                    last_action_time = time.time()

        if len(lmlist) == 21:
            fingers = []
            # Thumb
            if lmlist[tipid[0]][1] > lmlist[tipid[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # Other fingers
            for i in range(1, 5):
                if lmlist[tipid[i]][2] < lmlist[tipid[i] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total_fingers = sum(fingers)

            current_time = time.time()
            if total_fingers == 4 and (current_time - last_action_time) > action_cooldown:
                pyautogui.scroll(500)  # Scroll up
                print("Scroll up")
                last_action_time = current_time
            elif total_fingers == 5 and (current_time - last_action_time) > action_cooldown:
                pyautogui.scroll(-500)  # Scroll down
                print("Scroll down")
                last_action_time = current_time

    cv2.imshow("Hand Mouse", img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()