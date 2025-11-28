# JSON Key Remover

A simple Python tool for removing or keeping specific keys in JSON files — with a clean and intuitive GUI.

GUI-based file selection | Custom output path and filename | Supports malformed JSON

---

## Features

- **Graphical interface** – No coding required. Select files and keys via GUI
- **Flexible key filtering** – Choose whether to *remove* or *keep* selected keys
- **Input + Output file control** – Manually enter or browse input file and output destination
- **Non-destructive cleaning** – Handles and auto-fixes malformed JSON with invalid characters
- **Lightweight & dependency-free** – Built using only Python standard libraries

---

## Installation

1. **Requirements**:
   - Python 3.6+  
   - `tkinter` (usually included with Python)

2. **Install manually (optional)**:
   ```bash
   pip install tk
   ```
3. **Clone from the repository and run**
   ```bash  
    git clone https://github.com/dedoZvezdi/json_key_remover.git
    cd json_key_remover
    python json_gui.py
   ```
   
---

## Usage

**1.** Run the script:
   ```bash
    python json_key_remover_gui.py
   ```
**2.** In the app:

  - Enter or browse to select the input JSON file
  - Enter or browse to choose the output location + filename
  - Click "Load JSON" to see all keys
  - Select which keys to remove or keep (choose mode)
  - Click "Process and Save" to export the filtered JSON
---

## Example 

### Before

   ```JSON
{
    "name": "Ivan",
    "age": "22",
    "kids": {
        "boys": "1",
        "girls": null
    },
    "job": "devops"
}
   ```
### After (if `age`, `kids`, and `job` are removed)

   ```JSON
{
    "name": "Ivan"
}
   ```
---

## FAQ 

 **Q:** Is the original file overwritten?  
  **A:** No, the output file is saved separately. You specify its location and filename.

 **Q:** What if my JSON contains invalid or special characters?  
  **A:** The app automatically cleans such characters before processing.

 **Q:** Can I use this on nested JSON structures?  
  **A:** Yes, keys are collected recursively and can be filtered regardless of depth.

 **Q:** Can I keep only specific keys and discard all others?  
  **A:** Yes — choose "Keep selected keys" mode before saving.
