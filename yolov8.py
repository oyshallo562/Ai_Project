from ultralytics import YOLO

# Create a new YOLO model from scratch
model = YOLO('yolov8n.yaml')

# Load a pretrained YOLO model (recommended for training)
model = YOLO('yolov8l.pt')
results = model.train(cfg="./dataset.yaml")
# 모델 평가
model.val()  # It'll automatically evaluate the data you trained on.

# Train the model using the 'coco128.yaml' dataset for 3 epochs
#results = model.train(data='coco128.yaml', epochs=3)

# Evaluate the model's performance on the validation set
#results = model.val()

# Perform object detection on an image using the model
#results = model('https://ultralytics.com/images/bus.jpg')

# Export the model to ONNX format
success = model.export(format='onnx', dynamic=True)
