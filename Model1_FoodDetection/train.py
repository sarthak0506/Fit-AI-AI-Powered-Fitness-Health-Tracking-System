# Model1_FoodDetection/train.py

from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # downloads automatically ~6MB

results = model.train(
    data='Food-Images-1/data.yaml',
    epochs=50,
    imgsz=640,
    batch=8,          # kept at 8 for safety on your PC
    name='food_detector',
    patience=10,
    augment=True,
    device='cpu'      # change to 0 if you have a GPU
)

print("\n✅ Training done!")
print(f"📦 Model saved at: runs/detect/food_detector/weights/best.pt")