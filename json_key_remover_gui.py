import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json_key_remover_core

class JSONKeyRemoverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JSON Key Remover")
        self.geometry("500x650")
        self.json_data = None
        self.all_keys = []
        self.check_vars = {}
        self.input_path = None
        self.output_path = None
        self.keep_mode = tk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self, text="Input JSON File", padding=10)
        input_frame.pack(padx=10, pady=5, fill="x")
        
        self.input_entry = ttk.Entry(input_frame, width=50)
        self.input_entry.pack(side="left", padx=(0, 5), expand=True, fill="x")
        input_browse = ttk.Button(input_frame, text="Browse...", command=self.browse_input)
        input_browse.pack(side="left")
        
        output_frame = ttk.LabelFrame(self, text="Output JSON File", padding=10)
        output_frame.pack(padx=10, pady=5, fill="x")
        
        self.output_entry = ttk.Entry(output_frame, width=50)
        self.output_entry.pack(side="left", padx=(0, 5), expand=True, fill="x")
        output_browse = ttk.Button(output_frame, text="Browse...", command=self.browse_output)
        output_browse.pack(side="left")
        
        load_btn = ttk.Button(self, text="Load JSON", command=self.load_file)
        load_btn.pack(pady=10)
        
        mode_frame = ttk.LabelFrame(self, text="Mode", padding=10)
        mode_frame.pack(padx=10, pady=5, fill="x")
        ttk.Radiobutton(mode_frame, text="Remove Selected Keys", variable=self.keep_mode, value=False).pack(anchor='w', padx=10)
        ttk.Radiobutton(mode_frame, text="Keep Selected Keys", variable=self.keep_mode, value=True).pack(anchor='w', padx=10)
        
        self.scroll_frame = ttk.Frame(self)
        self.scroll_frame.pack(padx=10, pady=5, fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.scroll_frame)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        process_btn = ttk.Button(self, text="Process and Save", command=self.process_and_save)
        process_btn.pack(pady=10)

    def browse_input(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, path)

    def browse_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)

    def load_file(self):
        path = self.input_entry.get().strip()
        if not path:
            messagebox.showerror("Error", "Please specify an input JSON file.")
            return
        try:
            self.json_data = json_key_remover_core.read_json_clean(path)
            self.all_keys = sorted(json_key_remover_core.collect_all_keys(self.json_data))
            self.populate_key_checkboxes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON:\n{e}")

    def populate_key_checkboxes(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.check_vars.clear()
        for key in self.all_keys:
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(self.inner_frame, text=key, variable=var)
            chk.pack(anchor="w")
            self.check_vars[key] = var

    def process_and_save(self):
        if self.json_data is None:
            messagebox.showerror("Error", "No JSON loaded.")
            return

        selected_keys = [k for k, var in self.check_vars.items() if var.get()]
        if not selected_keys:
            messagebox.showwarning("Warning", "No keys selected.")
            return

        mode = 'keep' if self.keep_mode.get() else 'remove'
        cleaned_data = json_key_remover_core.filter_keys(self.json_data, selected_keys, mode)

        out_path = self.output_entry.get().strip()
        if not out_path:
            messagebox.showerror("Error", "Please specify an output file path.")
            return

        try:
            json_key_remover_core.write_json(cleaned_data, out_path)
            messagebox.showinfo("Success", f"JSON saved to:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON:\n{e}")

if __name__ == "__main__":
    app = JSONKeyRemoverApp()
    app.mainloop()
