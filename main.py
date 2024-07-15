import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import google.generativeai as genai
import whisper
import json
import threading
import pygame
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.tooltip import ToolTip
import random
import speech_recognition as sr
from ttkbootstrap.widgets import Scale
import os
from datetime import datetime

pygame.mixer.init()
click_sound = pygame.mixer.Sound("click.mp3")
success_sound = pygame.mixer.Sound("success.wav")

global selected_transcription_model
selected_transcription_model = "medium"  # Valor predeterminado

def save_api_key(api_key):
    with open('api_key.txt', 'w') as f:
        f.write(api_key)

def load_api_key():
    if os.path.exists('api_key.txt'):
        with open('api_key.txt', 'r') as f:
            return f.read().strip()
    return ""
def show_loading_screen():
    loading_window = tk.Toplevel(root)
    loading_window.title("Cargando")
    loading_window.geometry("300x180")
    loading_window.configure(bg='#2c3e50')

    canvas = tk.Canvas(loading_window, width=100, height=100, bg='#2c3e50', highlightthickness=0)
    canvas.pack(pady=10)

    loading_label = ttk.Label(loading_window, text="Transcribiendo audio, por favor espere...",
                              foreground='white', background='#2c3e50')
    loading_label.pack(pady=10)

    def animate_loading(angle):
        if loading_window.winfo_exists():
            canvas.delete("all")
            canvas.create_arc(10, 10, 90, 90, start=angle, extent=60, fill="#3498db")
            loading_window.after(50, animate_loading, (angle + 10) % 360)

    animate_loading(0)
    return loading_window


def transcribe_with_google_speech(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="es-ES")
    except sr.UnknownValueError:
        return "Google Speech Recognition no pudo entender el audio"
    except sr.RequestError as e:
        return f"No se pudo solicitar resultados del servicio de Google Speech Recognition; {e}"


def update_state_label(value):
    if value == 0:
        state_label.config(text="Rápido")
        return "Google Speech Recognition"
    elif value == 1:
        state_label.config(text="Preciso")
        return "medium"
    else:
        state_label.config(text="Exacto")
        return "large"

def update_model(value):
    global selected_transcription_model
    selected_transcription_model = update_state_label(int(float(value)))

def transcribe_audio_file():
    global selected_transcription_model
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        loading_window = show_loading_screen()

        def transcribe_thread():
            try:
                if selected_transcription_model == "Google Speech Recognition":
                    text = transcribe_with_google_speech(file_path)
                else:
                    model = whisper.load_model(selected_transcription_model)
                    result = model.transcribe(file_path)
                    text = result["text"]

                # Dializar el texto transcrito
                dialized_text = tafi(text)

                # Pulir la transcripción dializada
                polished_text = pulidor_de_transcripcion(dialized_text)
                # Insertar el texto pulido en entry_user_input
                entry_user_input.delete("1.0", tk.END)
                entry_user_input.insert(tk.END, polished_text)

            except Exception as e:
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, f"Error en la transcripción: {e}")
            finally:
                loading_window.destroy()
                success_sound.play()

        thread = threading.Thread(target=transcribe_thread)
        thread.start()
def tafi(text):
    api_key = entry_api_key.get().strip()
    if not api_key:
        return "Por favor, ingresa tu API Key."

    genai.configure(api_key=api_key)

    try:
        with open('content.json', 'r', encoding='utf-8') as file:
            content = json.load(file)
    except FileNotFoundError:
        return "El archivo 'content.json' no se encontró."
    except json.JSONDecodeError:
        return "El archivo 'content.json' no tiene un formato JSON válido."
    except IOError:
        return "Hubo un error al leer el archivo 'content.json'."
    content.append(f"input:{text}")
    content.append("output: ")

    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="Eres un sistema de dializacion, evita ponerle titulo a la dializacion y evita el uso de negritas"
    )
    print(content)
    response = model.generate_content(content)
    return response.text


def generate_text(api_key, user_input, rubros_calidad):
    genai.configure(api_key=api_key)

    try:
        with open('content2.json', 'r', encoding='utf-8') as file:
            content = json.load(file)
    except FileNotFoundError:
        return "El archivo 'content2.json' no se encontró."
    except json.JSONDecodeError:
        return "El archivo 'content2.json' no tiene un formato JSON válido."
    except IOError:
        return "Hubo un error al leer el archivo 'content2.json'."
    content.append(f"input: {user_input}")
    content.append(f"Rubros de calidad a evaluar:\n{rubros_calidad}")
    content.append("output: ")
    print(content)
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="Eres un sistema de que evalua el desempeño de los agentes en un call center, SIEMPRE agregas una PUTUACION al final de tus evaluaciones y te limitas unicamente a decir si o no en base a cada uno de las preguntas de la rubrica"
    )

    response = model.generate_content(content)
    return response.text


def on_generate_click():
    api_key = entry_api_key.get().strip()
    save_api_key(api_key)
    api_key = entry_api_key.get().strip()
    user_input = entry_user_input.get("1.0", tk.END).strip()
    rubros_calidad = entry_rubros_calidad.get("1.0", tk.END).strip()
    if not api_key:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Por favor, ingresa tu API Key.")
        return

    if not user_input:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Por favor, ingresa el texto de la conversación.")
        return

    if not rubros_calidad:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Por favor, ingresa los Rubros de calidad.")
        return

    try:
        generated_text = generate_text(api_key, user_input, rubros_calidad)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, generated_text)
    except Exception as e:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error: {str(e)}")
    finally:
        success_sound.play()
        notebook.select(result_frame)


def tafo():
    click_sound.play()
    text = entry_user_input.get("1.0", tk.END).strip()

    if not text:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Error: El campo de entrada está vacío.")
        return

    try:
        # Paso 1: Dializar con tafi
        processed_text = tafi(text)

        # Paso 2: Pulir la transcripción
        polished_text = pulidor_de_transcripcion(processed_text)

        # Actualizar el campo de entrada con el texto pulido
        entry_user_input.delete("1.0", tk.END)
        entry_user_input.insert(tk.END, polished_text)

        print(polished_text)  # Si quieres mantener la impresión en consola

    except Exception as e:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error en el procesamiento: {e}")


def pulidor_de_transcripcion(text):
    api_key = entry_api_key.get().strip()
    if not api_key:
        return "Por favor, ingresa tu API Key."

    genai.configure(api_key=api_key)

    try:
        with open('proff.json', 'r', encoding='utf-8') as file:
            content = json.load(file)
    except FileNotFoundError:
        return "El archivo 'proff.json' no se encontró."
    except json.JSONDecodeError:
        return "El archivo 'proff.json' no tiene un formato JSON válido."
    except IOError:
        return "Hubo un error al leer el archivo 'proff.json'."

    content.append(f"input:{text}")
    content.append("output: ")
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="Eres un sistema que busca el contexto de la llamada y el nombre de la empresa, modifica las palabras que se salen de este contexto para que esten en sintonia con el resto de la llamada, tambien agregas simobolos de pregunta y puntuaciones ¿? . ,"
    )
    print("Texto enviado al modelo para pulir:", content)
    response = model.generate_content(content)
    return response.text


def save_rubros():
    rubros = entry_rubros_calidad.get("1.0", tk.END).strip()
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(rubros)


def load_rubros():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            rubros = file.read()
            entry_rubros_calidad.delete("1.0", tk.END)
            entry_rubros_calidad.insert(tk.END, rubros)


def create_animated_button(parent, text, command):
    def command_with_sound():
        click_sound.play()
        command()

    btn = ttk.Button(parent, text=text, command=command_with_sound, style="Accent.TButton")

    def on_enter(e):
        btn.state(['active'])

    def on_leave(e):
        btn.state(['!active'])

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return btn


def create_gradient(canvas, color1, color2):
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()
    for i in range(height):
        r1, g1, b1 = root.winfo_rgb(color1)
        r2, g2, b2 = root.winfo_rgb(color2)
        r = (r1 + int((r2 - r1) * i / height)) & 0xff00
        g = (g1 + int((g2 - g1) * i / height)) & 0xff00
        b = (b1 + int((b2 - b1) * i / height)) & 0xff00
        color = f'#{r:04x}{g:04x}{b:04x}'
        canvas.create_line(0, i, width, i, fill=color)


def export_results():
    result = result_text.get("1.0", tk.END).strip()
    if not result:
        messagebox.showwarning("Advertencia", "No hay resultados para exportar.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".html",
        filetypes=[("HTML files", "*.html")],
        title="Guardar resultados como"
    )

    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                html_content = f"""
                <!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Resultados de Evaluación</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            max-width: 800px;
                            margin: 0 auto;
                            padding: 20px;
                        }}
                        h1 {{
                            color: #2c3e50;
                            border-bottom: 2px solid #3498db;
                            padding-bottom: 10px;
                        }}
                        .result-container {{
                            background-color: #f9f9f9;
                            border: 1px solid #ddd;
                            border-radius: 5px;
                            padding: 20px;
                            margin-top: 20px;
                        }}
                        .timestamp {{
                            color: #7f8c8d;
                            font-size: 0.9em;
                            margin-top: 20px;
                        }}
                    </style>
                </head>
                <body>
                    <h1>Resultados de Evaluación</h1>
                    <div class="result-container">
                        <pre>{result}</pre>
                    </div>
                    <p class="timestamp">Generado el: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
                </body>
                </html>
                """
                file.write(html_content)

            messagebox.showinfo("Éxito", f"Resultados exportados exitosamente a:\n{file_path}")

            # Abrir el archivo HTML en el navegador predeterminado
            os.startfile(file_path)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al exportar los resultados:\n{str(e)}")


# Configuración de la ventana principal
root = ttk.Window(themename="darkly")
root.title("Evaluador de Calidad de Agentes de Call Center")
root.geometry("1000x700")

# Crear un estilo personalizado
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12), padding=5)
style.configure("TEntry", font=("Helvetica", 12), padding=5)
style.configure("Treeview", font=("Helvetica", 11))
style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"))

# Crear un notebook para organizar las secciones
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True, padx=20, pady=20)

# Pestaña de entrada
input_frame = ttk.Frame(notebook, padding=20)
notebook.add(input_frame, text="Entrada de Datos")

# Crear un marco para la API Key
api_frame = ttk.LabelFrame(input_frame, text="Configuración de API", padding=10)
api_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")

label_api_key = ttk.Label(api_frame, text="API Key:")
label_api_key.grid(row=0, column=0, pady=5, padx=5, sticky="w")

# Cargar la API key guardada
saved_api_key = load_api_key()
entry_api_key = ttk.Entry(api_frame, width=50)
entry_api_key.grid(row=0, column=1, pady=5, padx=5, sticky="we")
entry_api_key.insert(0, saved_api_key)  # Insertar la API key guardada
#entry_api_key.insert(0, "AIzaSyA7XVmI4d26T2KsS50fCWf75eC2Gta3z0E")

# Marco para la conversación
conversation_frame = ttk.LabelFrame(input_frame, text="Conversación", padding=10)
conversation_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="nsew")

entry_user_input = ScrolledText(conversation_frame, width=60, height=10)
entry_user_input.pack(fill=BOTH, expand=True)

# Frame para contener el botón de transcribir y el selector de modelo
transcribe_frame = ttk.Frame(conversation_frame)
transcribe_frame.pack(fill=X, pady=(10, 0))

button_transcribe = create_animated_button(transcribe_frame, "Transcribir Audio", transcribe_audio_file)
button_transcribe.pack(side=tk.LEFT, padx=(0, 10))

# Etiqueta para "Precisión:"
precision_label = ttk.Label(transcribe_frame, text="Precisión:")
precision_label.pack(side=tk.LEFT, padx=(10, 5))

# Crear la barra deslizante
transcription_slider = Scale(transcribe_frame, from_=0, to=2, value=1, length=200,
                             command=lambda v: update_model(v))
transcription_slider.pack(side=tk.LEFT, padx=5)

# Etiqueta para mostrar el estado actual
state_label = ttk.Label(transcribe_frame, text="Preciso")
state_label.pack(side=tk.LEFT, padx=5)


button_dializar = create_animated_button(transcribe_frame, "Dializar", tafo)
button_dializar.pack(side=tk.RIGHT)

# Marco para los rubros de calidad
rubros_frame = ttk.LabelFrame(input_frame, text="Rubros de Calidad", padding=10)
rubros_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20), sticky="nsew")

entry_rubros_calidad = ScrolledText(rubros_frame, width=60, height=5)
entry_rubros_calidad.pack(side=tk.LEFT, fill=BOTH, expand=True)

# Botones para guardar y cargar rubros
button_frame = ttk.Frame(rubros_frame)
button_frame.pack(side=tk.RIGHT, padx=(10, 0))

button_save_rubros = create_animated_button(button_frame, "Guardar", save_rubros)
button_save_rubros.pack(pady=2)

button_load_rubros = create_animated_button(button_frame, "Cargar", load_rubros)
button_load_rubros.pack(pady=2)

button_generate = create_animated_button(input_frame, "Generar Evaluación", on_generate_click)
button_generate.grid(row=3, column=0, columnspan=2, pady=10)

# Pestaña de resultado
result_frame = ttk.Frame(notebook, padding=20)
notebook.add(result_frame, text="Resultado")

result_text = ScrolledText(result_frame, wrap=tk.WORD, width=80, height=20)
result_text.pack(fill=BOTH, expand=True)

# Agregar el botón de exportar
button_export = create_animated_button(result_frame, "Exportar Resultados", export_results)
button_export.pack(pady=10)

# Configurar el peso de las filas y columnas
input_frame.columnconfigure(0, weight=1)
input_frame.rowconfigure(1, weight=1)
input_frame.rowconfigure(2, weight=1)

# Configurar tooltips
ToolTip(button_transcribe, "Transcribe el audio seleccionado")
ToolTip(button_dializar, "Procesa el texto ingresado")
ToolTip(button_generate, "Genera evaluación basada en la entrada")
ToolTip(button_save_rubros, "Guarda los rubros de calidad")
ToolTip(button_load_rubros, "Carga rubros de calidad guardados")
ToolTip(transcription_slider, "Selecciona el modelo de transcripción a utilizar")
ToolTip(button_export, "Exporta los resultados en formato HTML")

update_model(1)  # 1 corresponde a "Preciso" o "medium"
# Iniciar la interfaz
root.mainloop()