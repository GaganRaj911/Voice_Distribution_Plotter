from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend
import matplotlib.pyplot as plt
import io
import base64
from scipy.stats import binom, poisson, norm
import speech_recognition as sr

app = Flask(__name__)

def generate_pdf_cdf(distribution):
    plt.figure(figsize=(10, 5))

    if distribution == "uniform":
        a, b = 0, 5
        x = np.linspace(a - 2, b + 2, 400)
        pdf = np.where((x >= a) & (x <= b), 1 / (b - a), 0)
        cdf = np.where(x < a, 0, np.where(x > b, 1, (x - a) / (b - a)))
    
    elif distribution == "rayleigh":
        sigma = 2
        x = np.linspace(0, 10, 400)
        pdf = (x / sigma**2) * np.exp(-x**2 / (2 * sigma**2))
        cdf = 1 - np.exp(-x**2 / (2 * sigma**2))
    
    elif distribution == "binomial":
        n, p = 20, 0.5
        x = np.arange(0, n + 1)
        pdf = binom.pmf(x, n, p)
        cdf = binom.cdf(x, n, p)
        plt.bar(x, pdf, label="Binomial PDF", alpha=0.6, color='g')
        plt.step(x, cdf, where='mid', label="Binomial CDF", color='r')
    
    elif distribution == "poisson":
        mu = 5
        x = np.arange(0, 20)
        pdf = poisson.pmf(x, mu)
        cdf = poisson.cdf(x, mu)
        plt.bar(x, pdf, label="Poisson PDF", alpha=0.6, color='b')
        plt.step(x, cdf, where='mid', label="Poisson CDF", color='r')
    
    elif distribution == "laplacian":
        mu, b = 0, 1
        x = np.linspace(-10, 10, 400)
        pdf = (1 / (2 * b)) * np.exp(-np.abs(x - mu) / b)
        cdf = 0.5 + 0.5 * np.sign(x - mu) * (1 - np.exp(-np.abs(x - mu) / b))
    
    elif distribution == "gaussian":
        mu, sigma = 0, 1
        x = np.linspace(-10, 10, 400)
        pdf = norm.pdf(x, loc=mu, scale=sigma)
        cdf = norm.cdf(x, loc=mu, scale=sigma)
    
    else:
        plt.close()
        return None
    
    if distribution in ["uniform", "rayleigh", "laplacian", "gaussian"]:
        plt.plot(x, pdf, label=f"{distribution.capitalize()} PDF", color='b')
        plt.fill_between(x, pdf, alpha=0.3, color='b')
        plt.plot(x, cdf, label=f"{distribution.capitalize()} CDF", color='r')
    
    plt.xlabel("X")
    plt.ylabel("Probability")
    plt.title(f"{distribution.capitalize()} Distribution")
    plt.legend()
    plt.grid()
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def recognize_distribution():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening for distribution name...")
            audio = recognizer.listen(source)
        
        print("Recognizing...")
        text = recognizer.recognize_google(audio).lower()
        print(f"Recognized: {text}")
        
        # Mapping of aliases to standard distribution names
        alias_map = {
            "uniform": "uniform",
            "rayleigh": "rayleigh",
            "really": "rayleigh",  # Alias for "rayleigh"
            "raili":"rayleigh",
            "binomial": "binomial",
            "binom":"binomial",
            "poisson": "poisson",
            "pois":"poisson",
            "poison": "poisson",  # Alias for "poisson"
            "laplace": "laplacian",
            "lapla":"laplacian",
            "laplacian": "laplacian",  # Alias for "laplace"
            "gaussian": "gaussian",
            "gajan":"gaussian"
        }
        
        # Find if any alias is in the recognized text
        for alias, standard_name in alias_map.items():
            if alias in text:
                return standard_name  # Return the correct function name

        return None  # If no valid distribution is found
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")
        return None
    except OSError:
        print("No microphone found. Please connect a microphone and try again.")
        return None


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_pdf', methods=['POST'])
def get_pdf():
    data = request.json
    distribution = data.get("distribution", "").lower()
    image_data = generate_pdf_cdf(distribution)
    if image_data:
        return jsonify({"image": image_data})
    return jsonify({"error": "Invalid distribution"})

@app.route('/speech_to_pdf', methods=['GET'])
def speech_to_pdf():
    distribution = recognize_distribution()
    if distribution:
        image_data = generate_pdf_cdf(distribution)
        if image_data:
            return jsonify({"image": image_data, "distribution": distribution})
    return jsonify({"error": "Could not recognize a valid distribution name."})

if __name__ == '__main__':
    app.run(debug=True)