from ultralytics import YOLO
import numpy as np
import cv2

# Initialize the YOLO model
model = YOLO("yolov8m-worldv2.pt")

def process_image(image, class_list):
    # Convert class_list string to list
    classes = [cls.strip() for cls in class_list.split(",")]
    
    # Set the model to detect only the specified classes
    model.set_classes(classes)
    
    # Convert the input image (PIL) to a NumPy array
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV
    
    # Perform prediction
    results = model.predict(image)
    boxes = results[0].boxes.xyxy.cpu().numpy()  # Bounding box coordinates
    class_indices = results[0].boxes.cls.cpu().numpy()  # Class indices
    
    # Annotate the image with bounding boxes and class names
    for box, class_idx in zip(boxes, class_indices):
        x1, y1, x2, y2 = map(int, box)  # Coordinates of the bounding box
        class_name = classes[int(class_idx)] if int(class_idx) < len(classes) else "Unknown"
        
        # Draw the bounding box with thicker lines
        cv2.rectangle(image, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=3)  # Red color
        
        # Add text above the bounding box
        font_scale = 0.8
        font_thickness = 2
        text_size = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
        text_x, text_y = x1, y1 - 10
        
        # Draw a filled rectangle as background for the text
        cv2.rectangle(
            image,
            (text_x, text_y - text_size[1] - 5),
            (text_x + text_size[0] + 5, text_y + 5),
            color=(0, 0, 255),
            thickness=-1
        )
        
        # Draw the class label text
        cv2.putText(
            image,
            class_name,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            color=(255, 255, 255),
            thickness=font_thickness
        )
    
    # Convert the image back to RGB format for display in Gradio
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image