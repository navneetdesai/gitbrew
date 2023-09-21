# Sign Language Recognition

![Demo](demo.png)

## Introduction
Welcome to the Sign Language Recognition project! This repository contains code for a computer vision project that uses the MediaPipe library to detect and track landmarks on a person's face, hands, and body. The goal of this project is to recognize gestures in American Sign Language (ASL) in real-time.

## Installation
To install the necessary dependencies, please follow these steps:
1. Navigate to the root folder of the project.
2. Run the command `pip install -r requirements.txt`.

## Usage
### Dataset Creation
To create the dataset, please follow these steps:
1. Open the `main.py` file.
2. Uncomment line 166 in the file.
3. This will enable video capture, and thirty videos of thirty frames each will be captured for each phrase in the `Constants.PHRASES` list.

### Gesture Recognition
To run the gesture recognition, please follow these steps:
1. Open the `main.py` file.
2. Comment out line 166 in the file.
3. This will disable video capture and allow the program to recognize gestures in American Sign Language.

## Contributing
Contributions are welcome! If you would like to contribute to this project, please follow these guidelines:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them with descriptive messages.
- Push your changes to your forked repository.
- Submit a pull request to the main repository.

## License
This project is licensed under the [MIT License](LICENSE).

![ASL](asl.jpg)

## Acknowledgements
Special thanks to the creators of the following libraries and frameworks used in this project:
- [MediaPipe](https://mediapipe.dev/): Used for detecting and tracking landmarks.
- [OpenCV](https://opencv.org/): Used for computer vision tasks.
- [NumPy](https://numpy.org/): Used for array manipulation and mathematical operations.
- [scikit-learn](https://scikit-learn.org/): Used for machine learning algorithms.
- [TensorFlow](https://www.tensorflow.org/): Used for building and deploying machine learning models.

## Contact
For any questions or inquiries, please contact [email protected]

#To be written by you: Add any additional sections, such as "Features", "Demo", "Results", etc. based on the information you have.