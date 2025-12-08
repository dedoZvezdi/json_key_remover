import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import logging
from typing import Dict, List, Optional, Set
import math

# Attempt to import core logic
try:
    from . import core
except ImportError:
    # Fallback for direct execution if not installed as package
    import core

class JSONKeyRemoverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JSON Key Remover Pro")
        self.geometry("800x750")
        
        # Data state
        self.json_data: Optional[core.JSONType] = None
        self.all_keys: List[str] = []
        self.check_vars: Dict[str, tk.BooleanVar] = {}
        self.keep_mode = tk.BooleanVar(value=False)
        
        # Styles
        style = ttk.Style(self)
        style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # --- File Selection ---
        self._create_file_selection_frame("Input JSON File", "browse_input", "input_entry")
        self._create_file_selection_frame("Output JSON File", "browse_output", "output_entry")

        # --- Actions ---
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        load_btn = ttk.Button(action_frame, text="Load JSON", command=self.load_file)
        load_btn.pack(side="left", padx=5)
        
        # --- Mode Selection ---
        mode_frame = ttk.LabelFrame(self, text="Processing Mode", padding=10)
        mode_frame.pack(padx=10, pady=5, fill="x")
        ttk.Radiobutton(mode_frame, text="Remove Selected Keys", variable=self.keep_mode, value=False).pack(anchor='w', padx=10)
        ttk.Radiobutton(mode_frame, text="Keep Selected Keys (Remove others)", variable=self.keep_mode, value=True).pack(anchor='w', padx=10)

        # --- Filter & Selection Controls ---
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ttk.Label(filter_frame, text="Search Keys:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_keys_display)
        entry = ttk.Entry(filter_frame, textvariable=self.search_var)
        entry.pack(side="left", fill="x", expand=True, padx=5)
        
        ttk.Button(filter_frame, text="Select All", command=self.select_all).pack(side="left", padx=2)
        ttk.Button(filter_frame, text="Deselect All", command=self.deselect_all).pack(side="left", padx=2)

        # --- Keys List (Scrollable) ---
        list_frame = ttk.LabelFrame(self, text="Keys found in JSON", padding=5)
        list_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.canvas = tk.Canvas(list_frame, bg="white")
        self.scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="white")
        
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # --- Final Process Button ---
        process_btn = ttk.Button(self, text="PROCESS AND SAVE", command=self.process_and_save)
        process_btn.pack(pady=15, ipady=5, fill='x', padx=20)

    def _create_file_selection_frame(self, title, command_name, entry_attr_name):
        frame = ttk.LabelFrame(self, text=title, padding=10)
        frame.pack(padx=10, pady=5, fill="x")
        
        entry = ttk.Entry(frame)
        entry.pack(side="left", padx=(0, 5), expand=True, fill="x")
        setattr(self, entry_attr_name, entry)
        
        btn = ttk.Button(frame, text="Browse...", command=getattr(self, command_name))
        btn.pack(side="left")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

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
            self.json_data = core.read_json_clean(path)
            self.all_keys = sorted(core.collect_all_keys(self.json_data))
            self.search_var.set("") # Reset search
            self.populate_key_checkboxes(self.all_keys)
            messagebox.showinfo("Loaded", f"Successfully loaded {len(self.all_keys)} unique keys.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON:\n{e}")

    def populate_key_checkboxes(self, keys_to_show: List[str]):
        # Clear existing widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Initialize check_vars for any new keys if not present
        for key in self.all_keys:
            if key not in self.check_vars:
                # Use default value False
                self.check_vars[key] = tk.BooleanVar(value=False)
                
        # --- Grid Layout Logic ---
        # Fixed columns for now, maybe dynamic later
        COLUMNS = 3
        # Calculate padding and expansion?
        # Actually standard grid is fine.
        
        for i, key in enumerate(keys_to_show):
            var = self.check_vars[key]
            # Use tk.Checkbutton to support 'bg' color matching the frame
            chk = tk.Checkbutton(self.scroll_frame, text=key, variable=var, bg="white", anchor="w")
            
            row = i // COLUMNS
            col = i % COLUMNS
            
            chk.grid(row=row, column=col, sticky="ew", padx=5, pady=2)
            
        # Configure grid columns to expand evenly
        for i in range(COLUMNS):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

    def filter_keys_display(self, *args):
        search_term = self.search_var.get().lower()
        if not search_term:
            filtered = self.all_keys
        else:
            filtered = [k for k in self.all_keys if search_term in k.lower()]
            
        self.populate_key_checkboxes(filtered)

    def select_all(self):
        search_term = self.search_var.get().lower()
        targets = [k for k in self.all_keys if search_term in k.lower()]
        
        for k in targets:
            self.check_vars[k].set(True)

    def deselect_all(self):
        search_term = self.search_var.get().lower()
        targets = [k for k in self.all_keys if search_term in k.lower()]
        
        for k in targets:
            self.check_vars[k].set(False)

    def process_and_save(self):
        if self.json_data is None:
            messagebox.showerror("Error", "No JSON loaded.")
            return

        selected_keys = {k for k, var in self.check_vars.items() if var.get()}
        
        if not selected_keys and self.keep_mode.get() == True:
             resp = messagebox.askyesno("Warning", "You are in 'Keep' mode but selected 0 keys. Result will be empty. Continue?")
             if not resp:
                 return
        
        if not selected_keys and self.keep_mode.get() == False:
            messagebox.showwarning("Warning", "No keys selected to remove.")
            return

        mode = 'keep' if self.keep_mode.get() else 'remove'
        
        try:
            cleaned_data = core.filter_keys(self.json_data, selected_keys, mode)
            
            out_path = self.output_entry.get().strip()
            if not out_path:
                messagebox.showerror("Error", "Please specify an output file path.")
                return

            core.write_json(cleaned_data, out_path)
            messagebox.showinfo("Success", f"JSON processed and saved to:\n{out_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON:\n{e}")

def main():
    app = JSONKeyRemoverApp()
    app.mainloop()

if __name__ == "__main__":
    main()
