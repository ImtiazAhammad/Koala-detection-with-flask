# Koala-detection-with-flask
## Instructions

-  Install all the requirements by using the command "pip -r install requirments.txt"
-  Check out the Notebook where the Yolov8 model training validation part is done.
- After training All the Evaluation metrics can be found in "/runs/detect/val/results.png
- After running the cells in the Inference section the predicted image will be stored in /runs/detect/predict" folder


# Koala Detection with YOLOv8

This repository contains code for building an object detection model using Convolutional Neural Network (CNN)-based architectures that can detect koalas in any picture with the help of object detection. The dataset used in this project contains 186 images of koalas, which were annotated with bounding boxes using the Make Scanse.ai tool. The YOLOv8 architecture was used to train the object detection model on the prepared dataset. After training the model, its performance was evaluated on the test dataset using precision, recall, and other metrics.

The API was developed using Flask, a micro web framework written in Python. The trained model was loaded into memory when the application started, and an API endpoint was created that took input variables, transformed them into the appropriate format, and returned predictions. The API was tested with various test images, and it was able to detect koalas in the images with high accuracy.

## Requirements

- Python 3.6 or higher
- Flask
- PyTorch
- NumPy
- OpenCV

## Usage

To use this code, you can clone the repository and install the required dependencies. You can then run the `koala_detection.ipynb` script to train the YOLOv8 model on your custom dataset. After training the model, you can run the `app.py` script to start the Flask app and test the API.

## Future Improvements

To enhance model performance, future improvements could involve hyperparameter tuning, increasing batch size, and extending the number of training epochs. These adjustments may contribute to further refinement and accuracy in Koala detection.





