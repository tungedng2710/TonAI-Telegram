from ultralytics import YOLO

model = YOLO('features/object_detection/yolov8n.pt')
def detect_objects(file_path, save_path):
    if save_path is None:
        save_path = 'result.jpg'
    results = model([file_path])
    for result in results:
        result.save(filename=save_path)

