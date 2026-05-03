from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def load_data():
    data = []
    with open('dataset.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route('/predict', methods=['POST'])
def predict():
    s1 = request.form.get('s1').lower()
    s2 = request.form.get('s2').lower()
    s3 = request.form.get('s3').lower()

    user_symptoms = [s1, s2, s3]

    data = load_data()
    best_match = ""
    max_score = -1

    for disease in data:
        disease_symptoms = disease["Symptoms"].split()
        score = len(set(user_symptoms) & set(disease_symptoms))

        if score > max_score:
            max_score = score
            best_match = disease["Disease"]

    # Explanation
    explanation = f"{best_match} is associated with symptoms like {', '.join(user_symptoms)}."

    # Advice
    advice = "Take rest, stay hydrated, and consult a doctor if symptoms persist."

    return render_template('result.html',
                           disease=best_match,
                           explanation=explanation,
                           advice=advice)

if __name__ == '__main__':
    app.run(debug=True)