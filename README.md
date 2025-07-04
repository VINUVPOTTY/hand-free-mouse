🧠 How It Works – Gesture-Based Mouse & Scroll Control
Camera Input
The script uses your webcam to continuously capture video frames in real time.

Hand Detection with MediaPipe
Each frame is processed using MediaPipe Hands, which detects 21 landmarks (key points) on a hand — such as finger tips and joints.

Mouse Movement
The position of your index fingertip (landmark 8) is tracked. This point is mapped to your screen coordinates, allowing the mouse cursor to follow your finger.

Click Gesture
When the thumb tip (landmark 4) comes close to the index fingertip (landmark 8) — i.e., a pinch gesture — the code measures the distance between them. If the distance is small enough, it triggers a mouse click.

Finger Counting for Gestures
The script checks which fingers are extended by comparing the position of each fingertip to the position of its preceding joints. It then counts the number of fingers raised.

Scroll Control

If 4 fingers are up (excluding thumb), the script scrolls up.

If 5 fingers are up, it scrolls down.
This happens only if a short cooldown period has passed, to prevent repeated scrolling from a single gesture.

Visualization
The script draws a red circle on your fingertip and shows a live feed window ("Hand Mouse") for visual feedback.

Exit
Press the ‘q’ key to quit the program.
