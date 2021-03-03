# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 03:25:08 2021

@author: Shaswat
"""

##Importing

import streamlit as st
import numpy as np
import pandas as pd
import cv2
from PIL import Image
import base64

    
## Sidebar

options = st.sidebar.selectbox("Choose one of the following:",("Home","Project Description", "How to run the project", "Upload and Download", "The developers"))
st.sidebar.write()


##Upon Selecting options

def get_options(options):
    
    st.sidebar.write("\n")
    st.sidebar.write("#### Page: ", options)
    if(options == "Project Description"): 
        project_description()
        
    elif(options== "Home"):
        home_page()
                 
    elif(options == "How to run the project"):
        how_to_run()
        
    elif(options == "Upload and Download"):
        upload_image()
        
    elif(options == "The developers"):
         about_dev()



##Individual functions

def home_page():
    
    st.title("Optical Character Recognition")
    st.text("\n")
    st.text("\n")
    st.text("\n")
    #st.image('Home page.jpg',use_column_width=True)
    
    
    
    
    
def project_description():
    
    st.title("Optical Character Recognition")
    st.text("\n")
    st.text("\n")
    st.text("\n")
    st.write("## What does it mean?")
    st.text("\n")
    st.write("""
             ### Image --> Text Conversion
             Optical character recognition (OCR) is the conversion of images to text.
             In order to extract and repurpose data from scanned documents, camera images or PDFs, you need an OCR software that would single out letters on the image thus enabling you to access and edit the original document.
             """)
    st.text("\n")
    st.write("## How did we do it?")
    st.text("\n")
    st.write("""
             ### Step 1. Reading the Image
             For converting an image into text, we have to do a task nobody would have ever thought of: Read the Image. We have done this using a predefined function in Streamlit.
             
             ### Step 2. Image preprocessing
             For this step, we have to use a library specifically made for such a project- Tesseract. Tesseract is an OCR engine with support for unicode and the ability to recognize more than 100 languages out of the box.
             In this we have to alter the image in such a way that it would get the most accurate results.
             Tesseract is finding templates in pixels, letters, words and sentences. It uses a two-step approach that calls adaptive recognition.
             It requires one data stage for character recognition, then the second stage to fulfil any letters, it wasn’t insured in, by letters that can match the word or sentence context.
             #### The better the image quality (size, contrast, lightning) the better the recognition result.
             """)
    #st.image('Preprocessing.png',use_column_width=True)
    st.text("\n")
    st.write("""
             ### Step 3. Text Recognition 
             Before the text recognition, via the image preprocessing, we must ensure that: \n
                 1. It is a binary image
                 2. Size of the image is not too big
                 3. Area of interest is highlighted
                 4. Noise is removed (All unnecessary background data)
                 5. The typography is common (so that it is easier to read) \n
            #### After all these conditions are met, we can convert the image to text with high accuracy.
             """)
    #st.image('Conversion to text.png', use_column_width=True)
    st.text("\n")
    st.write("""
             ### Step 4. Testing
             The final stage of the conversion is testing, which means that the project is tested on several datasets to check its accuracy. A few tweaks are made at the end and the project is retested.
             """)
    st.text("\n")
    st.text("\n")
    st.text("\n")
    st.write("""
             ## Check out how to run the project on the next page
             """)





def how_to_run():
    
    st.title("How to Run the Project")
    st.text("\n")
    st.text("\n")
    st.text("\n")
    st.write("## The project can be run in a few easy steps:")
    st.text("\n")
    st.write("""
             ### Step 1: Capture an Image
             The image captured can be anything with English text (scanned documents, camera images or PDFs)
                 
             """)
    #st.image('how to run 2a.jpg', use_column_width=True)
    st.write("""
             ### Step 2: Upload the from your device
             Upload the image either by clicking on "Browse files" and selecting an image or by dragging the image directly.
             Note that this file can only be of the file types: jpg, png, jpeg
                 
             """)
    #im= Image.open('how to run 3.jpg')
    #st.image(im, use_column_width=True)
    st.write("""
             ### Step 3: Download the image
             The image is now successfully converted from image to text. Click on the button to download the text file as a text file (notepad).
                 
             """)
    #st.image('how to run 4.png', use_column_width=True)
    #st.image('how to run 2b.jpg', use_column_width=True)
    st.text("\n")
    st.text("\n")
    st.text("\n")
    #st.image('How to run1.jpeg', use_column_width=True)
    st.write("""
             ## Try it yourself on the next page!
             """)


def download_link(object_to_download, download_filename, download_link_text):
    
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def upload_image():
    
        st.title("Upload and Download")
        st.text("\n")
        st.text("\n")
        st.text("\n")
        
       ##Upload from desktop
        st.text("\n")
        st.write("### Upload the image")
        
        img = st.file_uploader("Upload Here", type=["jpeg", "png", "jpg"], accept_multiple_files=False)
        if img is not None:
            image = Image.open(img)
            st.image(image, caption="The selected image", use_column_width=True)
            
            ##Print the details of image

            file_details = {"FileName":img.name,"FileType":img.type,"FileSize":img.size}
            st.write(file_details)
    
            # " img " is the output variable
            
            st.text("\n")
            st.text("\n")
            st.text("\n")
            st.write("### Download the converted image")
            st.text("\n")
            s = st.text_input('Enter text here') #s = output function of functions Eg: s = image_to_text(img)
            st.write(s) # Remove this line once replaced with actual function
            if st.button('Download input as a text (.txt) file'):
                tmp_download_link = download_link(s, 'Image_to_text.txt', 'Click here to download the file')
                st.markdown(tmp_download_link, unsafe_allow_html=True)





def about_dev():
    
        st.write("# The Developers")
        st.text("\n")
        st.text("\n")
        st.text("\n")
        st.write("""
                 ## The project was completed by 4 members:
                 """)
        st.text("\n")
        st.text("\n")
        st.write("### 1. Shaswat Srivastava (GUI) \n")
        st.write("### 2. Shubham Gore (Image Preprocessing) \n")
        st.write("### 3. Ved P. Dubey (Image Preprocessing) \n")
        st.write("### 4. Dhruv Kuncha (Testing)")
                     
        
        
        
        
X= get_options(options)