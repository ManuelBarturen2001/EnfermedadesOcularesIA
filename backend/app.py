from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import tensorflow as tf

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})

# Cargar el modelo
model = load_model('C:/Users/MANUEL/Documents/CDGN_CNN.keras')  # Cambia esta ruta a la ubicación de tu modelo

# Mapeo de clases
classes = ['Catarata', 'Retinopatía Diabética', 'Glaucoma', 'Ojo Normal']

@app.route('/predict', methods=['POST'])
def predict():
    print("Recibida solicitud de predicción")
    if 'file' not in request.files:
        print("No se encontró archivo en la solicitud")
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    print(f"Archivo recibido: {file.filename}")

    try:
        # Cargar la imagen
        img = Image.open(file.stream)
        img = img.resize((150, 150))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)

        # Realizar la predicción
        predictions = model.predict(img_array)[0]

        # Mapea las probabilidades a las clases
        results = {classes[i]: float(predictions[i]) for i in range(len(classes))}  # Convertir a float

        # Obtener la clase con la mayor probabilidad
        predicted_class = classes[np.argmax(predictions)]
        confidence = float(np.max(predictions))  # Convertir a float

        print(f"Predicción: {results}")
        return jsonify({
            'predicted_class': predicted_class,
            'confidence': confidence,
            'all_probabilities': results
        })
    except Exception as e:
        print(f"Error durante la predicción: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
