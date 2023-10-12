### Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

This repository contains a computer vision project that uses the MediaPipe library to detect and track landmarks on a person's face, hands, and body in real time. The project is built using Python and depends on the following libraries:
- mediapipe==0.8.9.1
- numpy==1.22.3
- opencv_contrib_python==4.5.5.64
- scikit-learn==1.1.1
- tensorflow==2.8.0

The project includes a dataset with videos of people signing in American Sign Language. The dataset is used to train a model that can recognize signs and display the results in real time.

## Installation

To install the necessary dependencies, navigate to the root folder of the project and run the command `pip install -r requirements.txt`. This will install all the required libraries and packages.

## Usage

To create the dataset, uncomment line 166 in the `main.py` file. This will enable video capture, and thirty videos of thirty frames each will be captured for each phrase in the `Constants.PHRASES` list.

To run tests, comment out line 166 in the `main.py` file. This will disable video capture and allow the program to recognize gestures in American Sign Language.

The `README.md` file also includes two images for demonstration purposes. The first image, named `demo.png`, shows an example of the program in action. The second image, named `asl.jpg`, is another visual representation related to the project.

## Contributing

Contributions are welcome! If you would like to contribute, please follow the guidelines in the [contributing file](https://github.com/username/repo/blob/main/CONTRIBUTING.md).

## License

This project is licensed under the [Apache 2.0 license](https://github.com/username/repo/blob/main/LICENSE).

---

## Summary of the Code

The `main.py` file contains code for a computer vision project that uses the MediaPipe library to detect and track landmarks on a person's face, hands, and body. Here is a summary of the code:

```
1. The code imports necessary libraries such as `time`, `cv2` (OpenCV), `tensorflow.keras`, `numpy`, `os`, `mediapipe`, and `sklearn`.
2. The code defines a class called `Constants` that holds various constants used in the project. Some of the constants include flags for summarization, a camera object, paths to data directories, phrases to be recognized, and the number of sequences and frames.
3. The code defines a function called `detect` that takes an image and a model as input. It converts the image from BGR to RGB format and processes it using the model. The function returns the original image and the results of the processing.
4. The code defines a function called `show_contours` that takes an image and a result as input. It draws landmarks on the face, hands, and body on the image using the `DRAW` object from the `mediapipe.solutions.drawing_utils` module.
5. The code defines a function called `return_flattened_keypoints` that takes a `landmarks` object as input. It extracts landmarks from the facial, hand, and body landmarks and returns a numpy array concatenation of flattened landmarks.
6. The code defines a function called `create_directories` that is a helper function for recursively creating directories. However, the function is incomplete and ends with a syntax error.

Overall, the code appears to be a part of a larger project that involves real-time detection and tracking of landmarks on a person's face, hands, and body using computer vision techniques.
```

The `requirements.txt` file contains the following dependencies:

```
1. mediapipe==0.8.9.1: This is the version 0.8.9.1 of the mediapipe library. It is used for building applications that can process and analyze multimedia data, such as videos and images.
2. numpy==1.22.3: This is the version 1.22.3 of the numpy library. It provides support for large, multi-dimensional arrays and matrices, along with a collection of mathematical functions to operate on these arrays.
3. opencv_contrib_python==4.5.5.64: This is the version 4.5.5.64 of the opencv_contrib_python library. OpenCV (Open Source Computer Vision Library) is a popular computer vision and machine learning software library. The opencv_contrib_python package provides additional modules and functionalities for OpenCV.
4. scikit-learn==1.1.1: This is the version 1.1.1 of the scikit-learn library. It is a machine learning library that provides various algorithms and tools for data mining and data analysis tasks. It is built on top of NumPy, SciPy, and matplotlib.
5. tensorflow==2.8.0: This is the version 2.8.0 of the TensorFlow library. TensorFlow is an open-source machine learning framework developed by Google. It provides a comprehensive ecosystem of tools, libraries, and resources for building and deploying machine learning models.
```

These dependencies are required for the code in the repository to function properly.