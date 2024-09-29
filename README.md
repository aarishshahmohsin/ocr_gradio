# OCR Application (IIT Roorkee Assignment)

This is a web application that utilizes OCR technology to extract text from images using two models: Surya OCR for Hindi and GOT-OCR for English. The extracted text can be searched for specific terms, with results highlighted for easier reference.

## Table of Contents

- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Running the Application Locally](#running-the-application-locally)
- [Deployment on Hugging Face Spaces](#deployment-on-hugging-face-spaces)
- [Usage](#usage)
- [License](#license)

## Features

- Upload an image for OCR processing.
- Extract Hindi text using Surya OCR and English text using GOT-OCR.
- Search functionality to highlight terms in the extracted text.

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/aarishshahmohsin/ocr_gradio
   cd ocr_gradio
   ```

2. **Create and activate a virtual environment:**

   For example, using Anaconda:

   ```bash
   conda create -n ocr_env python=3.12
   conda activate ocr_env
   ```

3. **Install the required packages:**

   Make sure you have `pip` installed, and then run:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application Locally

1. **Run the application:**

   Once all dependencies are installed, you can run the application using:

   ```bash
   python app.py
   ```

   This will start a local server, typically at `http://127.0.0.1:7860`.

2. **Open your web browser:**

   Navigate to the URL provided in the terminal (e.g., `http://127.0.0.1:7860`) to access the application.

## Deployment on Hugging Face Spaces

The Deployed application can be checked at : [Link](https://huggingface.co/spaces/aarishshahmohsin/ocr_gradio) (Takes 2-3 minutes for inferring due to it running on CPU).

## Usage

1. **Upload an Image:**

   Click on the "Upload an Image" button to select an image for OCR processing.

2. **Run OCR:**

   After uploading, click the "Run OCR" button to process the image. This will extract the Hindi and English text from the image.

3. **Search Extracted Text:**

   Enter a search term in the textbox and click "Search" to highlight the term in the extracted text.

## Details

The models used are :

### For English: 
The model used is [GOT OCR](https://github.com/Ucas-HaoranWei/GOT-OCR2.0).
<br>
For this application the CPU version of this model was implemented: https://huggingface.co/aarishshahmohsin/got_ocr_2
### For Hindi: 
The model used is [Surya](https://github.com/VikParuchuri/surya?tab=readme-ov-file).
