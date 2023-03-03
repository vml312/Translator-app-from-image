# -*- coding: utf-8 -*-
"""
Created on Tue Mar 1 - Fri Mar  3 11:54:09 2023

UPM Etsidi

ETSIDI.py

@author: vml312
"""

import cv2
import pytesseract
from PIL import Image
from autocorrect import Speller
from deep_translator import GoogleTranslator
import numpy as np
import streamlit as st
from langdetect import detect
import re

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = (r"C:\Users\Usuario\AppData\Local\Programs\Tesseract-OCR\tesseract.exe")
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'


img_file_buffer = st.file_uploader("Upload an image")
if img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    img_array = np.array(image) # if you want to pass it to OpenCV
    st.image(image, caption="Input", use_column_width=True)

    img=cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    image=cv2.blur(img,(1,1))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 1)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    
    img_erosion = cv2.erode(blur, kernel, iterations=1)
    
    pil_erosion = Image.fromarray(img_erosion)
    st.image(pil_erosion, caption="Erosion", use_column_width=True)
    
    pil_thresh = Image.fromarray(thresh)
    st.image(pil_thresh, caption="Thresh", use_column_width=True)

    def detect_image_lang(pil_imagen):
            osd = pytesseract.image_to_osd(pil_imagen)
            script = re.search("Script: ([a-zA-Z]+)\n", osd).group(1)
            conf = re.search("Script confidence: (\d+\.?(\d+)?)", osd).group(1)
            return script, float(conf)

    
    script_name, confidence = detect_image_lang(pil_thresh)
    st.write("Alphabet: "+script_name)

    if script_name=="Arabic": 
        lenguaje="ara"
    elif script_name=="Devanagari":
        lenguaje='hin'
    elif script_name=="Han":
        lenguaje="chi-sim"
    else:
        lenguaje="spa" #Solo funciona si detecta alfabeto latino

    text_input = pytesseract.image_to_string(img,lang=lenguaje)
    
    lenguaje_detec=detect(text_input)
    
    st.write("Language detected: "+lenguaje_detec)
    
    if lenguaje_detec=="es": 
        lenguaje="spa"
    elif lenguaje_detec=="en": 
        lenguaje="eng"
    elif lenguaje_detec=="fr":
        lenguaje="fra"
    elif lenguaje_detec=="it":
        lenguaje="ita"
    elif lenguaje_detec=="no":
        lenguaje="nor"
    elif lenguaje_detec=="deu":
        lenguaje="de"
    elif lenguaje_detec=="ell":
        lenguaje="el"
    else:
        lenguaje="spa"

    text_erosion=pytesseract.image_to_string(img_erosion,lang=lenguaje)
    text_thresh = pytesseract.image_to_string(thresh, lang=lenguaje)
    text_input = pytesseract.image_to_string(img,lang=lenguaje)

    spell = Speller(lang=lenguaje_detec)
    
    input_corr=spell(text_input)
    erosion_corr=spell(text_erosion)
    thresh_corr=spell(text_thresh)
    
    if lenguaje=="spa":
        spell=Speller(lang='en')
        if erosion_corr > thresh_corr and erosion_corr>input_corr:
            final_txt=GoogleTranslator(source='auto', target='en').translate(erosion_corr) 
        elif thresh_corr > input_corr and thresh_corr > input_corr:
            final_txt=GoogleTranslator(source='auto', target='en').translate(thresh_corr)
        else:
            final_txt=GoogleTranslator(source='auto', target='en').translate(input_corr)
    else:
        spell=Speller(lang='es')
        if erosion_corr > thresh_corr and erosion_corr>input_corr:
            final_txt=GoogleTranslator(source='auto', target='es').translate(erosion_corr) 
        elif thresh_corr > input_corr and thresh_corr > input_corr:
            final_txt=GoogleTranslator(source='auto', target='es').translate(thresh_corr)
        else:
            final_txt=GoogleTranslator(source='auto', target='es').translate(input_corr)
    
    
    final_txt_corr= spell(final_txt)
    
    st.write("\nTRADUCCIÓN\n")
    
    st.write(final_txt_corr)
