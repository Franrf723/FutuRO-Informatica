import tkinter as tk
from tkinter import messagebox

def realizar_operacion(tipo):
    try:
        # Obtener los valores de los cuadrados de texto
        val1 = float(entry_num1.get())
        val2 = float(entry_num2.get())
        
        resultado = 0
        if tipo == "sumar":
            resultado = val1 + val2
        elif tipo == "restar":
            resultado = val1 - val2
            
        # Actualizar la etiqueta de resultado
        lbl_resultado.config(text=f"Resultado: {resultado}")
        
    except ValueError:
        # Gestión de errores si el usuario no introduce números
        messagebox.showerror("Error", "Por favor, introduce valores numéricos válidos.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Calculadora Básica")
root.geometry("400x300")

# Frame contenedor para centrar todo el contenido
frame_central = tk.Frame(root)
frame_central.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# --- Elementos de la Interfaz ---

# Primer número
tk.Label(frame_central, text="Número 1:").pack(pady=5)
entry_num1 = tk.Entry(frame_central, justify='center')
entry_num1.pack(pady=5)

# Segundo número
tk.Label(frame_central, text="Número 2:").pack(pady=5)
entry_num2 = tk.Entry(frame_central, justify='center')
entry_num2.pack(pady=5)

# Botones
# Usamos un frame adicional para poner los botones uno al lado del otro
frame_botones = tk.Frame(frame_central)
frame_botones.pack(pady=15)

btn_sumar = tk.Button(frame_botones, text="Sumar", width=10, 
                      command=lambda: realizar_operacion("sumar"))
btn_sumar.pack(side=tk.LEFT, padx=10)

btn_restar = tk.Button(frame_botones, text="Restar", width=10, 
                       command=lambda: realizar_operacion("restar"))
btn_restar.pack(side=tk.LEFT, padx=10)

# Etiqueta para mostrar el resultado
lbl_resultado = tk.Label(frame_central, text="Resultado: ", font=("Arial", 12, "bold"))
lbl_resultado.pack(pady=10)

# Bucle principal de ejecución
root.mainloop()