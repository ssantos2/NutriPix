import streamlit as st
from PIL import Image, ImageDraw
import torch
import torchvision.transforms as T
from torchvision.models.detection import maskrcnn_resnet50_fpn
import requests

# Load the pre-trained Mask R-CNN model
model = maskrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Image preprocessing
preprocess = T.Compose([
    T.ToTensor()
])

# Food API for calorie information
FOOD_API_ENDPOINT = "https://api.edamam.com/api/food-database/v2/parser"
APP_ID = "APP_ID"  # Replace with your Edamam Application ID
API_KEY = "API_KEY"  # Replace with your Edamam API Key

# COCO class labels
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A',
    'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
    'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# Function to get food information from API
def get_food_info(food_name):
    params = {
        "app_id": APP_ID,
        "app_key": API_KEY,
        "ingr": food_name,
    }
    response = requests.get(FOOD_API_ENDPOINT, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["hints"]:
            return data["hints"][0]["food"]
    return None

# Function to estimate calories
def estimate_calories(image):
    # Preprocess the image
    image_tensor = preprocess(image).unsqueeze(0)
    
    # Get model prediction
    with torch.no_grad():
        prediction = model(image_tensor)
    
    detected_foods = []
    total_calories = 0
    for label, score, box in zip(prediction[0]['labels'], prediction[0]['scores'], prediction[0]['boxes']):
        if score > 0.7:  # Increased confidence threshold to reduce false positives
            category = COCO_INSTANCE_CATEGORY_NAMES[label]
            if category in ['apple', 'sandwich', 'pizza', 'donut', 'cake', 'banana', 'orange', 'broccoli', 'carrot', 'hot dog']:
                food_info = get_food_info(category)
                if food_info:
                    calories = food_info.get("nutrients", {}).get("ENERC_KCAL", 0)
                    detected_foods.append((category, calories, box))
                    total_calories += calories
    
    return detected_foods, total_calories

# Function to draw segmentation masks on the image
def draw_segmentation_masks(image, detected_foods):
    draw = ImageDraw.Draw(image)
    for food, _, box in detected_foods:
        box = box.int().tolist()
        draw.rectangle(box, outline="red", width=3)
        draw.text((box[0], box[1]), food, fill="red")
    return image

# Streamlit app
st.title("Food Calorie Estimation App")

uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Perform segmentation and calorie estimation
    detected_foods, total_calories = estimate_calories(image)
    image_with_masks = draw_segmentation_masks(image, detected_foods)
    st.image(image_with_masks, caption='Segmented Image', use_column_width=True)

    if detected_foods:
        st.write("Detected Foods:")
        for food, calories, _ in detected_foods:
            st.write(f"- {food}: {calories:.2f} kcal")
        st.write(f"Total Estimated Calories: {total_calories:.2f} kcal")
    else:
        st.write("No foods detected.")