<h1>Eye Tracking System using OpenCV and MediaPipe</h1>

This repository contains an eye tracking system implemented with OpenCV and MediaPipe. The system utilizes computer vision techniques to detect and track the movement of the user's left eye, providing insights into visual attention distribution.

<h1>Features</h1>

Real-time eye tracking: The system processes video input from a webcam and tracks the user's left eye movement in real-time.

Grid-based analysis: The screen is divided into a grid of segments, and the system calculates the duration of gaze in each segment as the eye moves.

Non-intrusive setup: No specialized equipment is required. The system uses the user's webcam, making it accessible and easy to set up.

High accuracy: Powered by the MediaPipe FaceMesh library and OpenCV, the system delivers accurate eye tracking results for reliable analysis.

Versatile applications: The eye tracking system can be used in various domains, including usability testing, human-computer interaction research, and assistive technologies.

<h1>Dependencies</h1>

OpenCV: For video capture, image processing, and display.

Mediapipe: For facial landmark detection using the FaceMesh model.

Numpy: For numerical operations and array manipulation.

Tkinter: For creating the graphical user interface.

<h1>Usage</h1>

1) Launch the eye tracking system using the provided script.

2) The system will open a graphical user interface displaying information about the eye tracking system and its advantages.

3) Click on the "Start Testing" button to begin the eye tracking process. 

4) The webcam feed will be displayed, with the detected eye landmarks and gaze duration information overlaid.

5) As the user's eye moves across the screen, the system calculates and updates the gaze duration for each segment.

6) Press the 'q' key to stop the eye tracking system.

7) After stopping, the system will display a summary of the total time spent on each segment and the screen divisions.

8) Close the graphical user interface to exit the program.

Let's explore the fascinating world of eye tracking and gain valuable insights into visual attention patterns. Happy coding! 👁️💻
