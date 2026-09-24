import tkinter as tk
from tkinter import messagebox
import random
import time
import os

# Obsidian Neon
COLOR_BG_DARK = "#0A0A0C"       # Preto 
COLOR_BG_PANEL = "#16181D"      # Preto menos preto para painéis
COLOR_BTN_PRIMARY = "#1F2937"   # Cinza escuro 
COLOR_BTN_HOVER = "#00E5FF"     # CIANO, MUITO CIANO
COLOR_BAR_DEFAULT = "#374151"   # Chumbo 
COLOR_BAR_SORTED = "#00E5FF"    # CIANO PARA AS BARRAS ORDENADAS 
COLOR_TEXT_LIGHT = "#F9FAFB"    # Branco 
COLOR_TEXT_MUTED = "#9CA3AF"    # Cinza claro 

SLEEP_TIME = 0.04

# --- Botões  ---
class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text="", radius=8, btn_color=COLOR_BTN_PRIMARY, text_color=COLOR_TEXT_LIGHT, hover_color=COLOR_BTN_HOVER, command=None, width=105, height=38, **kwargs):
        super().__init__(master, width=width, height=height, bg=master["bg"], highlightthickness=0, **kwargs)
        self.command = command
        self.btn_color = btn_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.default_text_color = text_color
        self.text = text
        self.radius = radius
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        
        self.draw_button(self.btn_color, self.text_color)
        
    def draw_button(self, color, t_color):
        self.delete("all")
        w = int(self["width"])
        h = int(self["height"])
        r = self.radius
        
        self.create_oval(0, 0, 2*r, 2*r, fill=color, outline=color)
        self.create_oval(w-2*r, 0, w, 2*r, fill=color, outline=color)
        self.create_oval(0, h-2*r, 2*r, h, fill=color, outline=color)
        self.create_oval(w-2*r, h-2*r, w, h, fill=color, outline=color)
        self.create_rectangle(r, 0, w-r, h, fill=color, outline=color)
        self.create_rectangle(0, r, w, h-r, fill=color, outline=color)
        
        self.create_text(w/2, h/2, text=self.text, fill=t_color, font=("Segoe UI", 9, "bold"))
        
    def on_enter(self, event):
        if self.btn_color == COLOR_BTN_PRIMARY:
            self.draw_button(COLOR_BTN_HOVER, COLOR_BG_DARK)
        else:
            self.draw_button(self.hover_color, self.text_color)
        
    def on_leave(self, event):
        self.draw_button(self.btn_color, self.default_text_color)
        
    def on_press(self, event):
        pass
        
    def on_release(self, event):
        if self.command:
            self.command()

# --- Aplicação Principal ---
class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("920x700")
        self.root.config(bg=COLOR_BG_DARK)
        self.root.resizable(True, True)

        self.data = []
        self.original_data = []
        self.times = {"Bubble Sort": -1.0, "Quick Sort": -1.0, "Merge Sort": -1.0}

        self.setup_ui()

    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg=COLOR_BG_DARK)
        header_frame.pack(pady=(20, 10))

        tk.Label(header_frame, text="ALGORITMO DE ORDENAÇÃO", bg=COLOR_BG_DARK, fg=COLOR_BTN_HOVER, font=("Segoe UI", 16, "bold")).pack()
        tk.Label(header_frame, text="Compare o desempenho e a execução visual dos métodos de ordenação", bg=COLOR_BG_DARK, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 10)).pack()

        container = tk.Frame(self.root, bg=COLOR_BG_DARK)
        container.pack(pady=10)

        control_frame = tk.Frame(container, bg=COLOR_BG_PANEL, padx=20, pady=15)
        control_frame.pack()

        inputs_frame = tk.Frame(control_frame, bg=COLOR_BG_PANEL)
        inputs_frame.pack(pady=(0, 12))

        tk.Label(inputs_frame, text="Tamanho do Array (1-150):", bg=COLOR_BG_PANEL, fg=COLOR_TEXT_LIGHT, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=8)
        
        self.size_entry = tk.Entry(inputs_frame, width=8, font=("Segoe UI", 11), bg=COLOR_BG_DARK, fg=COLOR_BTN_HOVER, insertbackground=COLOR_BTN_HOVER, relief=tk.FLAT, justify="center")
        self.size_entry.insert(0, "30")
        self.size_entry.pack(side=tk.LEFT, padx=8, ipady=3)

        buttons_frame = tk.Frame(control_frame, bg=COLOR_BG_PANEL)
        buttons_frame.pack(pady=5)

        # --- Botões de Ação ---
        RoundedButton(buttons_frame, text="Gerar Array", command=self.generate_array, width=105).pack(side=tk.LEFT, padx=5)
        RoundedButton(buttons_frame, text="Bubble Sort", command=self.run_bubble, width=105).pack(side=tk.LEFT, padx=5)
        RoundedButton(buttons_frame, text="Quick Sort", command=self.run_quick, width=105).pack(side=tk.LEFT, padx=5)
        RoundedButton(buttons_frame, text="Merge Sort", command=self.run_merge, width=105).pack(side=tk.LEFT, padx=5)
        RoundedButton(buttons_frame, text="Resultados", command=self.show_results, btn_color=COLOR_BTN_HOVER, text_color=COLOR_BG_DARK, width=105).pack(side=tk.LEFT, padx=5)
        RoundedButton(buttons_frame, text="Histórico", command=self.show_history, btn_color=COLOR_BTN_PRIMARY, text_color=COLOR_BTN_HOVER, width=105).pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.root, text="Pronto para iniciar. Gere um array.", bg=COLOR_BG_DARK, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 10), width=80, anchor="center")
        self.status_label.pack(pady=10)

        canvas_container = tk.Frame(self.root, bg=COLOR_BG_PANEL, padx=2, pady=2)
        canvas_container.pack(pady=5)
        
        self.canvas = tk.Canvas(canvas_container, width=850, height=400, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack()

    def generate_array(self):
        try:
            size = int(self.size_entry.get())
            if size <= 0 or size > 150: raise ValueError
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Insira um número inteiro entre 1 e 150.")
            return

        self.original_data = [random.randint(10, 100) for _ in range(size)]
        self.data = self.original_data.copy()
        
        self.times = {"Bubble Sort": -1.0, "Quick Sort": -1.0, "Merge Sort": -1.0}
        self.status_label.config(text=f"Novo array gerado com {size} elementos.")
        
        self.draw_data(self.data, [COLOR_BAR_DEFAULT for _ in range(len(self.data))])

    def draw_data(self, data, color_array):
        self.canvas.delete("all")
        c_height = 400
        c_width = 850
        x_width = c_width / (len(data) + 1)
        offset = 10
        spacing = max(1, 25 // len(data)) 

        max_val = max(data) if data else 1
        normalized_data = [i / max_val for i in data]

        for i, height in enumerate(normalized_data):
            x0 = i * x_width + offset + spacing
            y0 = c_height - (height * 340) - 25
            x1 = (i + 1) * x_width + offset
            y1 = c_height - 15
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i], width=0)
            
            if len(data) <= 30:
                self.canvas.create_text(
                    x0 + (x1 - x0) / 2, y0 - 8, 
                    text=str(data[i]), 
                    fill=COLOR_TEXT_LIGHT, 
                    font=("Segoe UI", 7, "bold")
                )

        self.root.update_idletasks()

    def prepare_sort(self):
        if not self.original_data:
            messagebox.showwarning("Aviso", "Gere um array primeiro!")
            return False
        self.data = self.original_data.copy()
        self.draw_data(self.data, [COLOR_BAR_DEFAULT for _ in range(len(self.data))])
        return True

# =--- Bubble Sort ---
    def run_bubble(self):
        if not self.prepare_sort(): return
        self.status_label.config(text="Executando Bubble Sort...")
        start = time.perf_counter()
        
        n = len(self.data)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    colors = [COLOR_BTN_HOVER if x == j or x == j+1 else COLOR_BAR_DEFAULT for x in range(n)]
                    self.draw_data(self.data, colors)
                    time.sleep(SLEEP_TIME)
                    
        self.times["Bubble Sort"] = time.perf_counter() - start
        self.draw_data(self.data, [COLOR_BAR_SORTED for _ in range(len(self.data))])
        self.status_label.config(text=f"Bubble Sort concluído em {self.times['Bubble Sort']:.4f} segundos.")

#--- Quick Sort ---
    def run_quick(self):
        if not self.prepare_sort(): return
        self.status_label.config(text="Executando Quick Sort...")
        
        start = time.perf_counter()
        self.quick_sort(0, len(self.data) - 1)
        self.times["Quick Sort"] = time.perf_counter() - start
        
        self.draw_data(self.data, [COLOR_BAR_SORTED for _ in range(len(self.data))])
        self.status_label.config(text=f"Quick Sort concluído em {self.times['Quick Sort']:.4f} segundos.")

#--- Quick Sort Helper Functions ---
    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)

    def partition(self, low, high):
        pivot = self.data[high]
        i = low - 1
        for j in range(low, high):
            if self.data[j] < pivot:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
                self.draw_data(self.data, [COLOR_BTN_HOVER if x == i or x == j else COLOR_BAR_DEFAULT for x in range(len(self.data))])
                time.sleep(SLEEP_TIME)
        
        self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
        self.draw_data(self.data, [COLOR_BTN_HOVER if x == i + 1 or x == high else COLOR_BAR_DEFAULT for x in range(len(self.data))])
        time.sleep(SLEEP_TIME)
        return i + 1
    
#--- Merge Sort ---
    def run_merge(self):
        if not self.prepare_sort(): return
        self.status_label.config(text="Executando Merge Sort...")
        
        start = time.perf_counter()
        self.merge_sort(0, len(self.data) - 1)
        self.times["Merge Sort"] = time.perf_counter() - start
        
        self.draw_data(self.data, [COLOR_BAR_SORTED for _ in range(len(self.data))])
        self.status_label.config(text=f"Merge Sort concluído em {self.times['Merge Sort']:.4f} segundos.")

    def merge_sort(self, l, r):
        if l < r:
            m = l + (r - l) / 2
            # Correção de divisão inteira em Python
            m = int(m)
            self.merge_sort(l, m)
            self.merge_sort(m + 1, r)
            self.merge(l, m, r)

    def merge(self, l, m, r):
        L = self.data[l:m + 1]
        R = self.data[m + 1:r + 1]
        i = j = 0
        k = l

        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                self.data[k] = L[i]
                i += 1
            else:
                self.data[k] = R[j]
                j += 1
            k += 1
            self.draw_data(self.data, [COLOR_BTN_HOVER if l <= x <= r else COLOR_BAR_DEFAULT for x in range(len(self.data))])
            time.sleep(SLEEP_TIME)

        while i < len(L):
            self.data[k] = L[i]
            i += 1
            k += 1
            self.draw_data(self.data, [COLOR_BTN_HOVER if l <= x <= r else COLOR_BAR_DEFAULT for x in range(len(self.data))])
            time.sleep(SLEEP_TIME)

        while j < len(R):
            self.data[k] = R[j]
            j += 1
            k += 1
            self.draw_data(self.data, [COLOR_BTN_HOVER if l <= x <= r else COLOR_BAR_DEFAULT for x in range(len(self.data))])
            time.sleep(SLEEP_TIME)

#--- Salva no arquivo resultado.txt ---
    def save_to_file(self, winner):
        try:
            with open("resultado.txt", "a", encoding="utf-8") as f:
                f.write("----------------------------------------\n")
                f.write(f"Data/Hora: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Tamanho do Array: {len(self.original_data)}\n")
                f.write(f"Bubble Sort : {self.times['Bubble Sort']:.6f} s\n")
                f.write(f"Quick Sort  : {self.times['Quick Sort']:.6f} s\n")
                f.write(f"Merge Sort  : {self.times['Merge Sort']:.6f} s\n")
                f.write(f"Vencedor    : {winner}\n")
                f.write("----------------------------------------\n\n")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")

    def show_results(self):
        for name, time_val in self.times.items():
            if time_val == -1.0:
                messagebox.showwarning("Atenção", f"Execute o algoritmo {name} primeiro!")
                return

        winner = min(self.times, key=self.times.get)
        self.save_to_file(winner)

        result_window = tk.Toplevel(self.root)
        result_window.title("Relatório de Performance")
        result_window.geometry("440x400")
        result_window.config(bg=COLOR_BG_DARK)
        result_window.resizable(False, False)
        
        result_window.update_idletasks()
        w, h = 440, 400
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        result_window.geometry(f"{w}x{h}+{x}+{y}")

        result_window.transient(self.root)
        result_window.grab_set()

        tk.Label(result_window, text="RELATÓRIO DE DESEMPENHO", bg=COLOR_BG_DARK, fg=COLOR_BTN_HOVER, font=("Segoe UI", 13, "bold")).pack(pady=(25, 5))
        tk.Label(result_window, text=f"Tamanho do Array Analisado: {len(self.original_data)} itens", bg=COLOR_BG_DARK, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9)).pack(pady=(0, 15))

        frame_tempos = tk.Frame(result_window, bg=COLOR_BG_PANEL, padx=25, pady=15)
        frame_tempos.pack(pady=5, fill=tk.X, padx=30)

        for name, time_val in self.times.items():
            color = COLOR_BTN_HOVER if name == winner else COLOR_TEXT_LIGHT
            texto = f"{name}: {time_val:.6f} s"
            if name == winner:
                texto += "  ★ (Mais Rápido)"
                
            tk.Label(frame_tempos, text=texto, bg=COLOR_BG_PANEL, fg=color, font=("Segoe UI", 10, "bold" if name == winner else "normal")).pack(anchor="w", pady=5)

        RoundedButton(result_window, text="Fechar", command=result_window.destroy, btn_color=COLOR_BTN_HOVER, text_color=COLOR_BG_DARK, width=130, height=35).pack(pady=20)

#--- Histórico de Execuções ---
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Histórico de Execuções")
        history_window.geometry("500x450")
        history_window.config(bg=COLOR_BG_DARK)
        history_window.resizable(False, False)

        history_window.update_idletasks()
        w, h = 500, 450
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        history_window.geometry(f"{w}x{h}+{x}+{y}")

        history_window.transient(self.root)
        history_window.grab_set()

        tk.Label(history_window, text="HISTÓRICO DE RESULTADOS", bg=COLOR_BG_DARK, fg=COLOR_BTN_HOVER, font=("Segoe UI", 13, "bold")).pack(pady=(20, 10))

        # Caixa de texto com barra de rolagem para o histórico
        text_frame = tk.Frame(history_window, bg=COLOR_BG_PANEL, padx=10, pady=10)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_area = tk.Text(text_frame, bg=COLOR_BG_PANEL, fg=COLOR_TEXT_LIGHT, font=("Consolas", 9), yscrollcommand=scrollbar.set, relief=tk.FLAT)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_area.yview)

        # Lê o arquivo resultado.txt se ele existir
        if os.path.exists("resultado.txt"):
            try:
                with open("resultado.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                    text_area.insert(tk.END, content)
            except Exception as e:
                text_area.insert(tk.END, f"Erro ao ler o arquivo: {e}")
        else:
            text_area.insert(tk.END, "Nenhum histórico encontrado ainda.\nExecute os três algoritmos e clique em 'Resultados' para registrar.")

        text_area.config(state=tk.DISABLED) # Impede edição manual

        RoundedButton(history_window, text="Fechar", command=history_window.destroy, btn_color=COLOR_BTN_HOVER, text_color=COLOR_BG_DARK, width=130, height=35).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()