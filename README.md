# Hand Dart Game

This project is an interactive virtual dart game played using hand gestures and computer vision. It leverages `cv2` (OpenCV) for video processing and `cvzone` for hand detection and tracking. Players "throw" darts by bringing their hand close to the camera while their hand's bounding box overlaps with a moving target, aiming to score points within a time limit.

## Features

* **Real-time Hand Tracking:** Detects and tracks hands from a webcam feed.
* **Proximity-Based "Throw":** Detects a "throw" action when the player's hand comes within a certain distance from the camera.
* **Target Interaction:** Scores a point when the player's hand is close enough and its bounding box overlaps with the dartboard target.
* **Dynamic Target:** The dartboard target moves to a new random position after each successful hit.
* **Game Timer & Score:** Tracks game time and the player's score, displaying them in real-time.
* **Game Over & Restart:** Ends the game after a set time limit and allows for restarting the game.
* **Visual Feedback:** Changes dartboard color on hit and displays game-related information (time, score, game over).

## Prerequisites

* Python (3.6 or higher recommended).
* A webcam connected to your computer.

## Installation

1.  **Clone or Download the Repository:**
    Get the project files to your local machine.

2.  **Install Required Libraries:**
    Open your terminal or command prompt and run:
    ```bash
    pip install opencv-python numpy cvzone
    ```

## Usage

1.  **Run the script:**
    Open your terminal or command prompt, navigate to the project directory, and execute the script:
    ```bash
    python dart_game.py
    ```
2.  **Start Playing:**
    * The game window will open, showing your webcam feed and a dartboard target (magenta circle).
    * **To Score:** Bring your hand close to the camera (within approximately 40cm, as calibrated). Simultaneously, ensure your hand's bounding box overlaps with the dartboard target.
    * **Hit Feedback:** Upon a successful hit, the dartboard will turn green briefly, your score will increase, and the target will move to a new random location.
    * **Timer:** The game has a 30-second timer displayed at the top right.
3.  **Game Over:**
    * Once the time runs out, "Game Over" will be displayed, along with your final score.
    * **Restart:** Press the `R` key on your keyboard to restart the game.
4.  **Exit:** Press the `Q` key on your keyboard to close the application window.

## How it Works

1.  **Video Capture & Hand Detection:** The webcam feed is continuously captured and horizontally flipped. The `HandDetector` identifies hands and provides their landmark details.
2.  **Distance Calibration:** Similar to typical hand distance measurement projects, a `(pixel_distance, cm_distance)` calibration curve (using `np.polyfit`) is used to estimate the real-world distance of the hand from the camera based on the pixel distance between two specific hand landmarks (landmark 5 and 17).
3.  **Hit Detection Logic:**
    * A "throw" is registered when the calculated `distanceCM` (hand distance from camera) is below a certain threshold (e.g., 40 cm). This simulates the act of throwing.
    * Concurrently, the bounding box of the detected hand is checked for overlap with the dartboard target's `(cx, cy)` coordinates.
    * If both conditions are met, a hit is registered.
4.  **Game State Management:**
    * A `counter` variable manages a brief visual feedback for a successful hit (target turning green) before resetting.
    * `score` and `timeStart` variables track the game's progress.
    * The `totalTime` variable defines the game duration.
5.  **Target Movement:** After a hit, `random.randint` is used to reposition the dartboard target on the screen.
6.  **Display:** The game interface, including the dartboard, real-time score, and timer, is overlaid on the live video feed.

## Customization

* **Camera Resolution:** Adjust `cap.set(3, 1280)` and `cap.set(4, 720)` for different webcam resolutions.
* **Detection Confidence:** `detector = HandDetector(detectionCon=0.8, maxHands=2)`: Adjust `detectionCon` for better hand detection performance.
* **Distance Threshold:** The `distanceCM < 40` threshold for a "throw" can be tuned based on your camera setup and how far you want players to extend their hands.
* **Game Time:** Change `totalTime = 30` to modify the duration of the game.
* **Target Size/Appearance:** Modify the `cv2.circle` parameters to change the size, color, and thickness of the dartboard target.
* **Dartboard Movement Range:** Adjust `random.randint(100, 1100)` and `random.randint(100, 600)` to control where the dartboard can appear on the screen.
