# Voice-Based Distribution Plotter

This project allows users to **speak the name of a probability distribution** (e.g., Gaussian, Poisson, Binomial, etc.), and it generates and displays the **PDF and CDF plots** of that distribution on a webpage.

Built using **Python**, **Flask**, **Matplotlib**, **SpeechRecognition**, and **SciPy**.

---

## Features

-  **Voice Recognition**: Recognizes spoken distribution names via microphone.
-  **Plotting**: Dynamically generates PDF and CDF plots for:
  - Gaussian
  - Laplacian
  - Uniform
  - Rayleigh
  - Binomial
  - Poisson
-  **Web Interface**: Plots rendered and displayed on a simple web page.
-  Plots styled using `matplotlib` and embedded as images.

---

##  Project Structure

Voice-Distribution-Plotter/
├── app.py # Main Flask application
├── Templates/
│ └── index.html # Frontend HTML file
├── Static/
│ └── script.js
│ └── style.css
├── requirements.txt # Python dependencies
└── README.md # Project documentation
└── Demo.mp4

## Getting Started

- Clone the Repository
- Install the dependencies : pip install -r requirements.txt
- Run the app : python app.py

## How It Works

-  The app uses the SpeechRecognition library with Google Speech API to recognize spoken distribution names.
-  The identified distribution is passed to a function that generates its PDF and CDF using matplotlib and scipy.stats.
-  The result is encoded as a base64 PNG image and sent back to the browser via JSON.

## Example Commands

Try saying:
- "Gaussian"
- "Laplacian"
- "Rayleigh"
- "Binomial"
- "Poisson"
- "Uniform"

Aliases like "poison", "gajan", "binom", "raili", "really", "lapla"  are also supported.

## Notes

- Requires a microphone to be connected for speech input.

## Requirements

- See requirements.txt

