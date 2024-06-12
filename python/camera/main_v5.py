import cv2
import numpy as np
import json
import requests

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Initialize the data dictionary
data = {"picture": []}

# Define the start and end indices for the 4x4 cell range
start_row, start_col = 3, 3
end_row, end_col = 6, 6

# Define the number of grid cells
grid_rows, grid_cols = 10, 10 

def sendData(data, destination):
    url = 'http://192.168.0.69:5000/' + destination
    response = requests.post(url, json=data)
    print(response.json())

def detect_color_in_cell(cell_roi):
    """
    Detects the dominant color in a given cell ROI.
    
    Args:
        cell_roi (numpy.ndarray): The region of interest (ROI) of the cell.
        
    Returns:
        str: The detected color, or 'None' if no color is detected.
    """
    # Define the color ranges you want to detect
    color_ranges = {
        'blue': ([94, 80, 2], [120, 255, 255]),
        'red': ([136, 87, 111], [180, 255, 255]),
        'green': ([25, 52, 72], [102, 255, 255]),
        'white': ([0, 0, 215], [179, 30, 255]),
        'black': ([0, 0, 0], [179, 255, 50])
    }
    
    for color, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(cell_roi, np.array(lower), np.array(upper))
        if np.any(mask):
            return color
    
    return 'None'

# Main function
def main():
    while True:
        # Capture a frame from the webcam
        ret, frame = cap.read()

        # Define the region of interest (ROI)
        roi_x1, roi_y1 = 0, 0  # Top-left corner of the ROI
        roi_x2, roi_y2 = 480, 480  # Bottom-right corner of the ROI

        # Divide the ROI into a grid
        cell_width = (roi_x2 - roi_x1) // grid_cols
        cell_height = (roi_y2 - roi_y1) // grid_rows

        # Get the frame dimensions
        frame_height, frame_width, _ = frame.shape
        print(f"Frame size: {frame.shape}, ROI dimensions: ({roi_x1}, {roi_y1}) - ({roi_x2}, {roi_y2}), Grid size: {grid_rows} x {grid_cols}")

        # Ensure the ROI coordinates are within the frame
        roi_x1 = max(0, roi_x1)
        roi_y1 = max(0, roi_y1)
        roi_x2 = min(frame_width, roi_x2)
        roi_y2 = min(frame_height, roi_y2)
            
        # Extract the ROI
        roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
        if roi.size == 0:
            print("ROI is empty, skipping frame.")
            continue

        # Convert the ROI to HSV color space
        try:
            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        except cv2.error as e:
            print(f"Error converting to HSV: {e}")
            continue

        for j in range(start_row, end_row + 1):
            for i in range(start_col, end_col + 1):
                x1 = j * cell_width + roi_x1
                y1 = i * cell_height + roi_y1
                x2 = x1 + cell_width
                y2 = y1 + cell_height

                # Detect the colors in the current grid cell
                cell_roi = hsv_roi[y1:y2, x1:x2]

                # Check for empty or invalid ROIs
                if cell_roi.size == 0 or np.any(np.isnan(cell_roi)) or np.any(np.isinf(cell_roi)):
                    continue

                detected_color = detect_color_in_cell(cell_roi)
                if detected_color != 'None':
                    print(f"Cell ({j}, {i}): {detected_color}")
                    #print(type(j), type(j), type(detected_color))
                    data["picture"][f"{j}, {i}"] = detected_color
            
        # Display the modified frames
        cv2.imshow('Color detection', frame)

        # Press 'x' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    # Release the video capture and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__": 
    main()
    sendData(data, "send_picture")