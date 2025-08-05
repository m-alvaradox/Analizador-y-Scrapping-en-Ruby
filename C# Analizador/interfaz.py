import tkinter as tk
import datetime
import os
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
from analizador import analisis_lexico, analisis_sintactico, analisis_semantico

class AnalizadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("C# Shark - Analizador")
        self.root.geometry("1170x685")
        self.root.configure(bg="#121212")

        # === CONTENEDOR PRINCIPAL ===
        main_frame = tk.Frame(root, bg="#121212")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === COLUMNA IZQUIERDA ===
        izquierda = tk.Frame(main_frame, bg="#121212")
        izquierda.pack(side=tk.LEFT, fill=tk.Y, padx=25, pady=10)

        # Logo
        try:
            logo_img = Image.open("cshark_logo.png")
            logo_img = logo_img.resize((100, 100), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(izquierda, image=self.logo, bg="#121212")
            logo_label.pack(pady=5)
        except Exception as e:
            print("Logo no cargado:", e)

        # Título
        titulo_label = tk.Label(
            izquierda,
            text="Analizador de Código C#",
            fg="#ffffff",
            bg="#121212",
            font=("Arial", 14, "bold")
        )
        titulo_label.pack(pady=5)

        # Caja de código con scrollbar
        self.crear_etiqueta(izquierda, "Pega tu código C#:")
        self.codigo_text = self.crear_caja_scroll_con_lineas(izquierda, height=25)

        # Botones
        btn_frame = tk.Frame(izquierda, bg="#121212")
        btn_frame.pack(pady=10)

        self.boton_personalizado(btn_frame, "Analizar", self.analizar).grid(row=0, column=0, padx=10)
        self.boton_personalizado(btn_frame, "Limpiar", self.limpiar).grid(row=0, column=1, padx=10)
        self.boton_personalizado(btn_frame, "Guardar Logs", self.guardar_logs).grid(row=0, column=2, padx=10)

        # === COLUMNA DERECHA ===
        derecha = tk.Frame(main_frame, bg="#121212")
        derecha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.lexico_text = self.crear_resultado(derecha, "Análisis Léxico")
        self.sintactico_text = self.crear_resultado(derecha, "Análisis Sintáctico")
        self.semantico_text = self.crear_resultado(derecha, "Análisis Semántico")

    def crear_etiqueta(self, parent, texto):
        etiqueta = tk.Label(parent, text=texto, fg="#ffffff", bg="#121212", font=("Arial", 11, "bold"))
        etiqueta.pack(anchor="w", pady=(5, 2))

    def crear_caja_scroll_con_lineas(self, parent, height=10):
        contenedor = tk.Frame(parent, bg="#121212")
        contenedor.pack(pady=5, fill=tk.BOTH, expand=False)

        # Canvas para los números de línea
        lineas_canvas = tk.Canvas(contenedor, width=40, bg="#1E1E1E", highlightthickness=0)
        lineas_canvas.pack(side=tk.LEFT, fill=tk.Y)

        # Scrollbar vertical
        scrollbar = tk.Scrollbar(contenedor)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar horizontal
        scrollbar_x = tk.Scrollbar(contenedor, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Text widget
        text_widget = tk.Text(
            contenedor,
            height=height, width=80, font=("Consolas", 10),
            bg="#2D033B", fg="#ffffff",
            insertbackground="white", wrap="none",
            yscrollcommand=lambda *args: (
                scrollbar.set(*args),
                self.actualizar_numeros_linea(lineas_canvas, text_widget)
            ),
            xscrollcommand=scrollbar_x.set
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=lambda *args: (
            text_widget.yview(*args),
            self.actualizar_numeros_linea(lineas_canvas, text_widget)
        ))
        scrollbar_x.config(command=text_widget.xview)

        # Vincular eventos
        text_widget.bind("<KeyRelease>", lambda e: self.actualizar_numeros_linea(lineas_canvas, text_widget))
        text_widget.bind("<MouseWheel>", lambda e: self.actualizar_numeros_linea(lineas_canvas, text_widget))
        text_widget.bind("<ButtonRelease-1>", lambda e: self.actualizar_numeros_linea(lineas_canvas, text_widget))

        # Inicial
        self.actualizar_numeros_linea(lineas_canvas, text_widget)

        return text_widget

    def crear_caja_scroll(self, parent, height=10):
        frame = tk.Frame(parent, bg="#121212")
        frame.pack(pady=5, fill=tk.BOTH, expand=False)

        # Scrollbar horizontal
        scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        text_widget = tk.Text(
            frame, height=height, width=60, bg="#2D033B", fg="#ffffff",
            insertbackground="white", wrap="none", font=("Consolas", 10),
            xscrollcommand=scrollbar_x.set
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar_x.config(command=text_widget.xview)

        return text_widget

    def actualizar_numeros_linea(self, canvas, text_widget):
        canvas.delete("all")
        i = text_widget.index("@0,0")
        while True:
            dline = text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linea = str(i).split(".")[0]
            canvas.create_text(35, y, anchor="ne", text=linea, fill="#aaaaaa", font=("Consolas", 10))
            i = text_widget.index(f"{i}+1line")

    def crear_resultado(self, parent, titulo):
        self.crear_etiqueta(parent, titulo)
        return self.crear_caja_scroll(parent, height=10)

    def boton_personalizado(self, parent, texto, comando):
        return tk.Button(
            parent, text=texto, command=comando,
            bg="#7B2CBF", fg="#ffffff", activebackground="#9D4EDD",
            font=("Arial", 11, "bold"), padx=15, pady=5, bd=0
        )

    def analizar(self):
        codigo = self.codigo_text.get("1.0", tk.END).strip()
        if not codigo:
            messagebox.showwarning("Advertencia", "Por favor ingresa código C#.")
            return

        self.lexico_text.delete("1.0", tk.END)
        self.lexico_text.insert(tk.END, analisis_lexico(codigo))

        self.sintactico_text.delete("1.0", tk.END)
        self.sintactico_text.insert(tk.END, analisis_sintactico(codigo))

        self.semantico_text.delete("1.0", tk.END)
        self.semantico_text.insert(tk.END, analisis_semantico(codigo))

    def limpiar(self):
        self.codigo_text.delete("1.0", tk.END)
        self.lexico_text.delete("1.0", tk.END)
        self.sintactico_text.delete("1.0", tk.END)
        self.semantico_text.delete("1.0", tk.END)

    def guardar_logs(self):
        nombre = simpledialog.askstring("Guardar Logs", "Ingresa tu nombre:")
        if not nombre:
            messagebox.showwarning("Advertencia", "Debes ingresar un nombre para guardar los archivos.")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        carpeta_logs = "logs"

        # Crear carpeta si no existe
        os.makedirs(carpeta_logs, exist_ok=True)

        lexico = self.lexico_text.get("1.0", tk.END).strip()
        sintactico = self.sintactico_text.get("1.0", tk.END).strip()
        semantico = self.semantico_text.get("1.0", tk.END).strip()

        try:
            with open(os.path.join(carpeta_logs, f"lexico-{nombre}-{timestamp}.txt"), "w", encoding="utf-8") as f:
                f.write(lexico)
            with open(os.path.join(carpeta_logs, f"sintactico-{nombre}-{timestamp}.txt"), "w", encoding="utf-8") as f:
                f.write(sintactico)
            with open(os.path.join(carpeta_logs, f"semantico-{nombre}-{timestamp}.txt"), "w", encoding="utf-8") as f:
                f.write(semantico)
            messagebox.showinfo("Éxito", f"Logs guardados en carpeta '{carpeta_logs}'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los archivos:\n{e}")


    

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalizadorGUI(root)
    root.mainloop()

