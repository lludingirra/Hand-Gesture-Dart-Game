import cv2  # Import OpenCV for video and image processing.
import math  # Import math for mathematical operations like square root.
import cvzone  # Import cvzone for helper functions like putting text and rectangles.
import random  # Import random for generating random numbers (for dartboard position).
import time  # Import time for time-related functions (for game timer).
import numpy as np  # Import numpy for numerical operations, especially for polynomial fitting.
from cvzone.HandTrackingModule import HandDetector # Import HandDetector from cvzone for hand detection and tracking.

# Initialize video capture from the default webcam (index 0).
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set the width of the captured video frame to 1280 pixels.
cap.set(4, 720)   # Set the height of the captured video frame to 720 pixels.

# Initialize HandDetector with a detection confidence of 0.8 and a maximum of 2 hands to detect.
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Calibration data for converting pixel distance to real-world cm distance.
# These values represent (pixel_distance, cm_distance) pairs.
x_values = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y_values = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
# Perform polynomial regression (2nd degree) to find coefficients (A, B, C) for the mapping.
coff = np.polyfit(x_values, y_values, 2)

# --- Game State Variables ---
cx, cy = 250, 250 # Initial coordinates for the dartboard target.
color = (255, 0, 255) # Initial color of the dartboard target (magenta).
counter = 0 # Counter for "hit" confirmation animation.
score = 0 # Player's score.
timeStart = time.time() # Timestamp when the game starts (or restarts).
totalTime = 30 # Total game time in seconds.

# --- Main Game Loop ---
while True:
    success, img = cap.read() # Read a frame from the webcam.
    if not success:
        print("Unable to capture camera image!") # Print error if frame reading fails.
        break # Exit the loop.

    img = cv2.flip(img, 1) # Flip the image horizontally (mirror effect).

    # Find hands in the image. flipType=False means it won't flip hand points internally.
    # draw=False means it won't draw landmarks by default on the image.
    hands, img = detector.findHands(img, flipType=False, draw=False)
    
    # Check if game time is still remaining.
    if time.time() - timeStart < totalTime:

        if hands: # If at least one hand is detected:
            lmList = hands[0]['lmList'] # Get landmarks for the first detected hand.

            # Ensure enough landmarks are detected for distance calculation (landmarks 5 and 17).
            if len(lmList) > 17:
                x1, y1 = lmList[5][:2] # Coordinates of landmark 5 (wrist).
                x2, y2 = lmList[17][:2] # Coordinates of landmark 17 (pinky base).

                # Calculate pixel distance between landmark 5 and 17.
                distance = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                A, B, C = coff # Get polynomial coefficients.
                distanceCM = A * distance ** 2 + B * distance + C # Convert pixel distance to cm.

                x, y, w, h = hands[0]['bbox'] # Get bounding box of the hand.

                # Check if the hand is close enough to the camera (distanceCM < 40 cm)
                # AND if the hand's bounding box overlaps with the dartboard target.
                if distanceCM < 40: # Proximity check (e.g., hand "throwing" the dart).
                    if x < cx < x + w and y < cy < y + h: # Bounding box collision with target.
                        counter = 1 # Start "hit" confirmation animation.

                # Draw bounding box around the hand and display distance in cm.
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
                cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x + 5, y - 10))
            else:
                print("Hand coordinates were not detected correctly!") # Error if not enough landmarks.

        if counter: # If a hit is registered (counter > 0):
            counter += 1 # Increment counter for animation.
            color = (0, 255, 0) # Change dartboard color to green (feedback for hit).

            if counter == 3: # After a short delay (3 frames):
                cx = random.randint(100, 1100) # Move dartboard to a new random x position.
                cy = random.randint(100, 600) # Move dartboard to a new random y position.
                color = (255, 0, 255) # Reset dartboard color to magenta.
                score += 1 # Increment score.
                counter = 0 # Reset counter for next hit.

        # Draw the dartboard target (concentric circles).
        cv2.circle(img, (cx, cy), 30, color, cv2.FILLED) # Outer circle (filled with current color).
        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED) # Inner circle (filled white).
        cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2) # Middle circle (white outline).
        cv2.circle(img, (cx, cy), 30, (50, 50, 50), 2) # Outer circle (dark gray outline).

        # Display game time and score.
        cvzone.putTextRect(img, f'Time: {int(totalTime - (time.time() - timeStart))}',
                           (1000, 75), scale=3, offset=20)
        cvzone.putTextRect(img, f'Score: {str(score).zfill(2)}', (60, 75),
                           scale=3, offset=20)

    else: # Game Over state (time ran out).
        cvzone.putTextRect(img, 'Game Over', (400, 400), scale=5, offset=30, thickness=7) # Display "Game Over".
        cvzone.putTextRect(img, f'Your Score: {score}', (450, 500), scale=3, offset=20) # Display final score.
        cvzone.putTextRect(img, 'Press R to restart', (460, 575), scale=2, offset=10) # Instruction to restart.

    cv2.imshow("Hand Tracking", img) # Display the game image.

    key = cv2.waitKey(1) & 0xFF  # Wait for 1ms for a key press.

    if key == ord('q'): # If 'q' is pressed, exit the game.
        break
    
    if key == ord('r'): # If 'r' is pressed, restart the game.
        timeStart = time.time() # Reset game timer.
        score = 0 # Reset score.
        cx, cy = 250, 250 # Reset dartboard position.
        color = (255, 0, 255) # Reset dartboard color.
        counter = 0 # Reset hit counter.

# Release the webcam object and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()