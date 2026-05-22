# Model1_FoodDetection/download_dataset.py

from roboflow import Roboflow

rf = Roboflow(api_key="8oLSnnnn7cv17Hnmloth")  # ← paste your key here

# ✅ BEST SINGLE DATASET — covers Indian food, chicken, paneer, salad, roti, dal
project = rf.workspace("object-detection-vpvcm").project("food-images-2lpjg")
dataset  = project.version(1).download("yolov8")

print("✅ Dataset downloaded!")
print("📁 Check the folder: food-images-2lpjg-1/")