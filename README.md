This app uses the following technologies:
- Python: The programming language used to develop the application.
- Edamam API: A food database API used to fetch nutritional information, including calorie content, for detected food items.
- Mask R-CNN: A pre-trained AI model (maskrcnn_resnet50_fpn) from the torchvision library, used for food detection and segmentation.
This model is pretrained on following food items ['banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake']

Setup:
Clone the repository and navigate to the Nutripix folder.
Create a virtual environment by running:
python -m venv test
(This will create a virtual environment named test, isolating all installed libraries to this environment and not affecting the rest of your system.)
Activate the virtual environment with:
source test/bin/activate
Install the required libraries:
pip install streamlit torch torchvision
Run the image analysis code using Streamlit:

streamlit run mask_rcnn_upd.py

## NutriPix 

*** 
## Prototype 

*** 
## Contributors 
