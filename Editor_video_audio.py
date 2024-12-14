import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

class EditorVideoAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Bienvenido al editor de video y audio David y Clark")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)  # La ventana no puede ser redimensionada

        self.ruta_video = None
        self.ruta_audio = None
        self.ruta_guardado = None

        # Componentes de la interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Botones de selección de archivos
        tk.Button(self.root, text="Seleccionar Video", command=self.cargar_video).pack(pady=10)
        tk.Button(self.root, text="Seleccionar Audio", command=self.cargar_audio).pack(pady=10)

        # Línea de tiempo
        self.linea_tiempo = tk.Canvas(self.root, bg="gray", height=200)
        self.linea_tiempo.pack(fill="x", pady=10)
        self.linea_tiempo.create_text(50, 100, text="Línea de tiempo (Video y Audio)", fill="white")

        # Botones de edición
        tk.Button(self.root, text="Seleccionar Carpeta de Guardado", command=self.seleccionar_carpeta_guardado).pack(pady=5)
        tk.Button(self.root, text="Cortar Video", command=lambda: self.ejecutar_en_hilo(self.cortar_video)).pack(pady=5)
        tk.Button(self.root, text="Agregar Audio", command=lambda: self.ejecutar_en_hilo(self.agregar_audio)).pack(pady=5)

        # Botón para colaborar
        tk.Button(self.root, text="Colaborar", command=self.colaborar).pack(pady=20)

        # Etiqueta de estado
        self.etiqueta_estado = tk.Label(self.root, text="¡Bienvenido al editor de video y audio!", fg="blue")
        self.etiqueta_estado.pack(pady=5)

    def cargar_video(self):
        self.ruta_video = filedialog.askopenfilename(filetypes=[("Archivos MP4", "*.mp4")])
        if self.ruta_video:
            self.etiqueta_estado.config(text=f"Video cargado: {os.path.basename(self.ruta_video)}")
        else:
            self.etiqueta_estado.config(text="No se seleccionó ningún video.")

    def cargar_audio(self):
        self.ruta_audio = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.mp3;*.wav")])
        if self.ruta_audio:
            self.etiqueta_estado.config(text=f"Audio cargado: {os.path.basename(self.ruta_audio)}")
        else:
            self.etiqueta_estado.config(text="No se seleccionó ningún audio.")

    def seleccionar_carpeta_guardado(self):
        self.ruta_guardado = filedialog.askdirectory()
        if self.ruta_guardado:
            self.etiqueta_estado.config(text=f"Carpeta seleccionada: {self.ruta_guardado}")
        else:
            self.etiqueta_estado.config(text="No se seleccionó ninguna carpeta.")

    def cortar_video(self):
        if not self.ruta_video:
            messagebox.showerror("Error", "Por favor, carga un video primero.")
            return

        tiempo_inicio = simpledialog.askfloat("Cortar Video", "Ingresa el tiempo de inicio en segundos:")
        tiempo_fin = simpledialog.askfloat("Cortar Video", "Ingresa el tiempo de fin en segundos:")

        if tiempo_inicio is not None and tiempo_fin is not None:
            try:
                video = VideoFileClip(self.ruta_video).subclip(tiempo_inicio, tiempo_fin)
                if self.ruta_guardado:
                    ruta_guardado = os.path.join(self.ruta_guardado, "video_cortado.mp4")
                    video.write_videofile(ruta_guardado)
                    self.etiqueta_estado.config(text=f"Video guardado en {ruta_guardado}")
                else:
                    messagebox.showerror("Error", "Selecciona una carpeta de guardado antes de cortar el video.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cortar el video: {e}")

    def agregar_audio(self):
        if not self.ruta_video or not self.ruta_audio:
            messagebox.showerror("Error", "Por favor, carga un video y un archivo de audio.")
            return

        try:
            video = VideoFileClip(self.ruta_video)
            audio = AudioFileClip(self.ruta_audio)

            tiempo_inicio = simpledialog.askfloat("Agregar Audio", "Ingresa el tiempo de inicio en segundos:")
            if tiempo_inicio is None:
                return

            audio = audio.set_start(tiempo_inicio)
            audio_final = video.audio.overlay(audio, position=tiempo_inicio)
            video = video.set_audio(audio_final)

            if self.ruta_guardado:
                ruta_guardado = os.path.join(self.ruta_guardado, "video_con_audio.mp4")
                video.write_videofile(ruta_guardado)
                self.etiqueta_estado.config(text=f"Video con audio agregado guardado en {ruta_guardado}")
            else:
                messagebox.showerror("Error", "Selecciona una carpeta de guardado antes de agregar audio.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el audio: {e}")

    def colaborar(self):
        resultado = messagebox.askyesno("Colaborar", "¿Te gustaría contribuir con 500 pesos \nAlias: davidask611 ?")
        if resultado:
            messagebox.showinfo("Gracias", "¡Gracias por tu apoyo!")
        else:
            messagebox.showinfo("No hay problema", "¡Siéntete libre de usar la aplicación!")

    def ejecutar_en_hilo(self, funcion):
        hilo = threading.Thread(target=funcion)
        hilo.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = EditorVideoAudio(root)
    root.mainloop()
