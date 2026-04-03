Gutenberg Text Cleaner

A Flask-based web application that fetches, cleans, summarizes, and analyzes text from Project Gutenberg .txt files.

This project was built for Operational Assignment 3 – Basics of AI (Spring 2026).

Features
Fetch text from Project Gutenberg URLs
Clean and preprocess text (remove boilerplate and front matter)
Generate a 3-sentence summary
Compute statistics:
total characters
total words
total sentences
average word length
average sentence length
most common words

Simple web interface

Error handling for invalid input

How to Run
Clone the repository:
git clone https://github.com/cfisher7595-stack/scaffolding3_startup.git
cd scaffolding3_startup

Install dependencies:
pip install -r requirements.txt
Run the app:
python app.py
Open in your browser:
http://localhost:5000
Example Test URLs
https://www.gutenberg.org/files/1342/1342-0.txt
https://www.gutenberg.org/files/11/11-0.txt
https://www.gutenberg.org/files/84/84-0.txt

Screenshots (in screenshots folder)

API Endpoints
/api/clean (POST)
Input: {"url": "https://www.gutenberg.org/files/1342/1342-0.txt"}
Returns: cleaned text, statistics, and summary
/api/analyze (POST)
Input: {"text": "your text here"}
Returns: statistics only
Project Structure
app.py
starter_preprocess.py
requirements.txt
templates/index.html
screenshots/
Technologies Used
Python, Flask, Requests, HTML, CSS, JavaScript

Author
Chris Fisher
University at Buffalo – Spring 2026