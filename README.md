![image](https://github.com/yumbiakyumu/MaizeDaktari.ai/assets/100669436/18cc3dc3-ada2-49fc-a7df-c48451a57e77) ![image](https://github.com/yumbiakyumu/MaizeDaktari.ai/assets/100669436/3ea7152e-6dc0-434f-aa71-70336f7e05c7)
# Maize Daktari.ai

## Introduction

Maize Daktari.ai is a pioneering machine learning project focused on detecting and diagnosing maize diseases using computer vision and deep learning techniques. This project utilizes a tech stack including HTML, CSS, JavaScript, Python, TensorFlow, and Convolutional Neural Networks (CNNs) to provide accurate disease identification and detailed diagnoses for maize plants.

## Functionalities

### 1. Disease Detection
Utilizing Convolutional Neural Networks (CNNs) to accurately identify various maize diseases from leaf images.

### 2. Disease Diagnosis
Providing detailed diagnoses and recommendations for detected diseases based on the analysis of symptoms.

### 3. Model Trainin
Leveraging Machine Learning to train the model used in diagnosis and detection

## Tech Stack

- HTML
- CSS
- JavaScript
- Python
- TensorFlow
- Convolutional Neural Networks (CNNs)

### HOW TO RUN THE WEB APP
## Prerequisites

- Python 3.6 - 3.9
- pip (Python package installer)
## Setup

1. Clone the repository:
  https://github.com/yumbiakyumu/MaizeDaktari.ai.git

2. Navigate to the project directory:
  cd (the directory you saved the work in) eg cd MaizeDaktari.ai]

3. Create a new virtual environment (optional, but recommended):
   python -m venv env

4. Activate the virtual environment:

   - On Windows: env\Scripts\activate
   - On Unix or macOS: source env/bin/activate
5. Install the required packages:
   pip install flask flask-cors tensorflow numpy Pillow

6. Download the Machine Learning Model
  The machine learning model used in this project is too large to be stored directly in the repository. To obtain the model file, follow these steps:

    1. Go to [this Google Drive link] (https://drive.google.com/file/d/1PgGQr-fmkIPOCX0tKJwqlIr7HEhaJne1/view?usp=sharing)
    2. Click on the "Download" button to download the model file.
    3. Extract the downloaded file (if applicable).
    4. Place the model file in the `root` directory of this your repository.

Once you have the model file in the correct location, you can proceed with running the code and using the model

7. Run the Flask application:
   flask run

The application should now be running at `http://localhost:5000`.

## Usage

1. Navigate to the root URL (`http://localhost:5000`) to access the home page.
2. Click on the "Upload Image" button to select a leaf image from your local machine.
3. The application will analyze the image and provide a prediction of the disease (if any) along with control information.
4. You can also register/login to access additional features like viewing your diagnosis history and submitting queries.

To access the admin dashboard, log in with an admin account.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

