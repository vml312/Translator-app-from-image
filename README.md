# Translator app from image
Python app that translates the text from the uploaded image
 
To execute the app its necessary to have pytesseract downloaded (with conda: 'conda install -c conda-forge pytesseract') and execute 'streamlit run app.py' (if the terminal is in the directory)
 
Works better with latin-alphabet languages, other alphabets are not so well captured.

If the image is quite blurred it might not work well.

In each picture of the results folder there are two parts, the left one is the image to translate and the right one is the result in the app.

## Credits

App made with Streamlit (https://github.com/streamlit/streamlit)


Libraries used:


https://github.com/filyp/autocorrect --> Language autocorrector


https://github.com/prataffel/deep_translator --> Translator (able to detect language)


https://github.com/Mimino666/langdetect --> Language detector from text


https://github.com/madmaze/pytesseract --> OCR, detects rotation, etc.


https://github.com/opencv/opencv-python --> Image processing


https://github.com/python-pillow/Pillow --> Image loader
