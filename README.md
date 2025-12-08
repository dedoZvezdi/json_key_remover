# JSON Key Remover

<p align="center">
  <b>A professional, high-performance tool for managing JSON datasets.</b>
  <br>
  Filter, clean, and restructure your JSON files with ease.
</p>

---

## Overview

**JSON Key Remover** is a robust desktop application designed for developers and data analysts who need to sanitize or restructure JSON data. Whether you are removing sensitive fields, cleaning up API responses, or simplifying large datasets, this tool offers a secure and user-friendly solution.

## Key Features

- **Intuitive "Grid View" Interface**: View and manage hundreds of keys efficiently with a modern multi-column layout.
- **Smart Filtering**: 
  - **Search**: Instantly find keys with real-time text filtering.
  - **Batch Operations**: "Select All" and "Deselect All" for rapid workflow.
- **Flexible Processing Modes**:
  - **Remove Mode**: Strip out unwanted keys.
  - **Keep Mode**: Whitelist specific keys and discard the rest.
- **Data Safety**:
  - **Non-destructive**: Your original files are never overwritten.
  - **Auto-Cleaning**: Automatically handles and sanitizes control characters in malformed JSON.
- **Professional Standard**: Built with type-safe Python code and full unit test coverage.

## Installation

### Prerequisites
- Python 3.6 or higher.
- `tkinter` (Standard with Python installations).

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/dedoZvezdi/json_key_remover.git
   cd json_key_remover
   ```

2. Run the application:
   ```bash
   python run.py
   ```

## Usage

1. **Load Data**: Click **Browse** to select your input JSON file. The tool will parse and list all unique keys found recursively in the file.
2. **Select Keys**:
   - Use the **Search Bar** to filter keys by name.
   - Check the boxes for keys you wish to target.
   - Use **Select All** to check all currently visible keys.
3. **Choose Action**:
   - **Remove Selected Keys**: Deletes the checked keys from the structure.
   - **Keep Selected Keys**: Preserves ONLY the checked keys and removes everything else.
4. **Process**: Click **Process and Save** to write the cleaned JSON to your output path.

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

---

## Development & Testing

The project is structured as a standard Python package.

```bash
# Run unit tests
python -m unittest discover tests
```

---

*Copyright (c) 2025 Svetlin Ivanov. Licensed under the MIT License.*
