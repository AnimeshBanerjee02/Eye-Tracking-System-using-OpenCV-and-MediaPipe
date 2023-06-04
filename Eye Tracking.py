import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
GRID_ROWS, GRID_COLS = 4, 4
ROI_WIDTH = SCREEN_WIDTH // GRID_COLS
ROI_HEIGHT = SCREEN_HEIGHT // GRID_ROWS

# Initialize MediaPipe FaceMesh and drawing utility
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Initialize video capture
cap = cv2.VideoCapture(0)

# Set screen size
cap.set(3, SCREEN_WIDTH)
cap.set(4, SCREEN_HEIGHT)

# Create empty list to store gaze data
gaze_data_list = []

# Initialize start time
start_time = None

# Create the UI window
window = tk.Tk()
window.title("Eye Tracking System")

# Create the system information and advantages label
info_text = """                                                                                                                     Eye Tracking System

            This eye tracking system utilizes the MediaPipe FaceMesh library and OpenCV to detect and track the movement of the user's left eye. 
            It divides the screen into a grid and calculates the gaze duration in each segment as the user's eye moves across the screen. 
            The system provides valuable insights into the user's visual attention distribution and can be used in various applications such as usability testing, human-computer interaction research, and assistive technologies.

            Advantages:
            - Non-intrusive eye tracking without the need for specialized equipment
            - Real-time tracking and analysis of eye movement
            - High accuracy and reliability
            - Versatile application possibilities"""

info_label = tk.Label(window, text=info_text, font=("Times New Roman", 12), bg='#D6EAF8', fg='#800517', justify="left")
info_label.pack(pady=10)

# Create the system information and advantages label
divisions_text = """                                                                                                                     Screen Divisions (Segments)

            The screen is divided into a grid of segments. Each segment represents a distinct region of the screen.
            The system tracks the user's eye movement and calculates the gaze duration in each segment as the eye moves across the screen.
            The table below shows the division of the screen into segments:
"""

divisions_label = tk.Label(window, text=divisions_text, font=("Arial", 12), bg='#D6EAF8', fg='#154360', justify="left")
divisions_label.pack(pady=10)

# Create a table frame to display the divisions
divisions_frame = tk.Frame(window, bg='#D6EAF8')
divisions_frame.pack(pady=10)

# Create the segments grid
for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        segment_label = tk.Label(divisions_frame, text=f"Segment {row * GRID_COLS + col + 1}", font=("Arial", 12),
                                 bg='#D6EAF8', fg='#154360', padx=10, pady=5, relief=tk.RIDGE)
        segment_label.grid(row=row, column=col, sticky=tk.W)

# Function to start testing
def start_testing():
    global start_time
    
    # Hide the start button
    start_button.pack_forget()
    
    # Start capturing frames
    while True:
        # Read frame from video capture
        ret, frame = cap.read()

        # Flip the frame horizontally for intuitive mirror view
        frame = cv2.flip(frame, 1)

        # Convert BGR image to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face landmarks
        with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
            # Process the frame to find face landmarks
            results = face_mesh.process(frame_rgb)

            # Check if landmarks are detected
            if results.multi_face_landmarks:
                # Get the first face landmarks
                face_landmarks = results.multi_face_landmarks[0]

                # Initialize empty list to store left eye landmarks
                left_eye_landmarks = []

                # Extract left eye landmarks
                for landmark in face_landmarks.landmark:
                    left_eye_landmarks.append((int(landmark.x * SCREEN_WIDTH), int(landmark.y * SCREEN_HEIGHT)))

                # Calculate the average position of the left eye
                left_eye_pos = tuple(map(int, np.mean(left_eye_landmarks, axis=0)))

                # Determine which segment the left eye is in based on the position
                row_index = left_eye_pos[1] // ROI_HEIGHT
                col_index = left_eye_pos[0] // ROI_WIDTH
                segment = f"Segment {row_index * GRID_COLS + col_index + 1}"

                # Calculate gaze duration
                current_time = datetime.now()
                if start_time is not None:
                    gaze_duration = current_time - start_time
                else:
                    gaze_duration = timedelta(seconds=0)

                # Add the gaze data to the list
                gaze_data_list.append((segment, gaze_duration))

                # Update start time for the next gaze duration
                start_time = current_time

                # Draw segment and gaze duration on the frame
                cv2.putText(frame, segment, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Gaze Duration: {gaze_duration.total_seconds():.2f} seconds", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Press q to exit", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Show the frame
        cv2.imshow("Eye Tracking", frame)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

    # Create a label to display the total times on the screen
    total_times_label = tk.Label(window, text="Total Time Spent on Each Segment:", font=("Arial", 14), bg='#D6EAF8', fg='#154360')
    total_times_label.pack(pady=10)
    
    # Calculate total time spent on each segment
    total_times = {}
    for segment, gaze_duration in gaze_data_list:
        if segment in total_times:
            total_times[segment] += gaze_duration
        else:
            total_times[segment] = gaze_duration

    # Create a table to display the segments and their total times
    table_frame = tk.Frame(window, bg='#D6EAF8')
    table_frame.pack(pady=10)

    # Create table headers
    headers = ['Segment', 'Total Time (s)']
    for col_index, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), bg='#D6EAF8', fg='#154360', padx=10, pady=5, relief=tk.RIDGE)
        label.grid(row=0, column=col_index, sticky=tk.W)

    # Display segment data in the table
    for row_index, (segment, total_time) in enumerate(total_times.items()):
        label_segment = tk.Label(table_frame, text=segment, font=("Arial", 12), bg='#D6EAF8', fg='#154360', padx=10, pady=5, relief=tk.RIDGE)
        label_time = tk.Label(table_frame, text=f"{total_time.total_seconds():.2f}", font=("Arial", 12), bg='#D6EAF8', fg='#154360', padx=10, pady=5, relief=tk.RIDGE)
        label_segment.grid(row=row_index+1, column=0, sticky=tk.W)
        label_time.grid(row=row_index+1, column=1, sticky=tk.W)

    # Create the stop testing button
    stop_button = tk.Button(window, text="Stop Testing", font=("Arial", 16), bg='#800517', fg='#FFFFFF', command=window.destroy)
    stop_button.pack(pady=10)

# Create the start testing button
start_button = tk.Button(window, text="Start Testing", font=("Arial", 16), bg='#1ABC9C', fg='#FFFFFF', command=start_testing)
start_button.pack(pady=10)

# Run the UI window
window.mainloop()
