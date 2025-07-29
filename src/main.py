import tkinter as tk
from tkinter import messagebox, ttk

root = tk.Tk()
root.title("Simulador de relações de Mercado")
root.geometry("1400x900")


main_frame = tk.Frame(root) 
main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)


title_label = tk.Label(main_frame, 
                       text="SIMULADOR DE RELAÇÕES DE MERCADO", 
                       font=("Arial", 24), 
                       fg="black")
title_label.pack(pady=(0,15))





meses_simular_label = tk.Label(main_frame, 
                                text="Meses para simular:",
                                font=("Arial", 16),
                                fg="black")
meses_simular_label.pack(side=tk.LEFT, padx=(0, 15), pady=(0, 625))
meses_entry = tk.Entry(main_frame, 
                                font=("Arial", 16), 
                                width=5)


meses_entry.pack(side=tk.LEFT, padx=(0, 15), pady=(0, 625))
meses_entry.insert(0, "1")

def iniciar_simulacao():
    try:
        meses = int(meses_entry.get())
        if meses <= 0:
            messagebox.showerror("Erro", "O número de meses deve ser maior que zero!")
            return
        messagebox.showinfo("Simulação", f"Simulação iniciada para {meses} meses!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido de meses!")

simular_button = tk.Button(main_frame, 
                          text="Simular",
                          font=("Arial", 16),
                          command=iniciar_simulacao)
simular_button.pack(side=tk.LEFT, padx=(0, 15), pady=(0, 625))

# Notebook para as abas
notebook = ttk.Notebook(main_frame)
notebook.pack(fill=tk.BOTH, expand=True)
       
# Aba das categorias
categoria_frame = tk.Frame(notebook)
notebook.add(categoria_frame, text="Categorias")



root.mainloop()