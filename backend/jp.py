import tensorflow as tf 
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import load_model
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

model = load_model('C:/Users/MANUEL/Documents/CDGN_CNN.keras')
categorias= ['cataract','diabetic_retinopathy','glaucoma','normal']

def evaluar_imagen():
    ruta_imagen = filedialog.askopenfilename(filetypes = [
        ("image", ".jpeg"),("image", ".png"),("image", ".jpg")])
    if len(ruta_imagen) > 0:   
        imagen = cv2.imread(ruta_imagen)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        imagen = cv2.resize(imagen,(400,400))
        imagen = ImageTk.PhotoImage(image=Image.fromarray(imagen))

        LblImagen.configure(image=imagen)
        LblImagen.image = imagen

        img = tf.keras.preprocessing.image.load_img(ruta_imagen, target_size=((150, 150)))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        resultado = categorias[np.argmax(score)]

        resultado_label.config(text=f'Resultado: {resultado}')
        

app = tk.Tk()
app.title("Sistema inteligente basado en CNN para la detección de enfermedades oculares")
app.geometry("600x550")

LblMensaje = tk.Label(app, text="Cargar una imagen de fondo de ojo")
LblMensaje.pack()

cargar_boton = tk.Button(app, text="Cargar Imagen", 
                         command=evaluar_imagen)
cargar_boton.pack(pady=15)

LblImagen = tk.Label(app)
LblImagen.pack()

resultado_label = tk.Label(app, text="", font=("Helvetica", 14))
resultado_label.pack()

app.mainloop()