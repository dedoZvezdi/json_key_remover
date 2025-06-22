# JSON Key Remover
😊A simple Python tool for removing unwanted keys from JSON files, with a clean GUI interface.

✅ User-friendly (GUI file selection) | Custom output path 

---

## 🛠 Features  

- **Easy file selection** - Graphical file picker for selecting JSON files
- **Bulk key removal** - Remove multiple predefined keys at once
- **Non-destructive cleaning** - Handles malformed JSON with special characters
- **Confirmation dialog** - Shows file info before processing
- **Lightweight** - No external dependencies beyond Python standard library
  
---

⚙️ Installation  
1. **Requirements**:  
   - Python 3.6+  
   - `tkinter` (usually included with Python).
     
2. **Install dependencies** (if needed):  
   ```bash  
   pip install tk
   ```
3. **Clone from the repository and run**
   ```bash  
    git clone https://github.com/dedoZvezdi/json_key_remover.git
    cd json_key_remover
   ```
   
---

## 🚀 Usage

1. Run the script:
   ```bash
    python json_key_remover.py
   ```
2. Select your JSON file through the file dialog
3. Confirm the operation when prompted with file details
4. The tool will process the file and notify you upon completion
---
## Customization ⚙️

To modify which keys are removed, edit the `KEYS_TO_REMOVE` list in the script:

   ```python
    KEYS_TO_REMOVE = [
    "scryfall_uri", 
    "uri",
    "released_at",
    # ... add or remove keys as needed
]
   ```
## Example 📋

### Before

   ```JSON
{
    "name": "Black Lotus",
    "scryfall_uri": "https://scryfall.com/card/lea/...",
    "prices": {
        "usd": "10000",
        "usd_foil": null
    },
    "image_status": "highres_scan"
}
   ```
### After

   ```JSON
{
    "name": "Black Lotus"
}
   ```
---

## FAQ ❓

**Q:** Is the original file overwritten?  
**A:** Yes, the tool modifies the file in-place. Make backups first.

**Q:** Can I use this with very large JSON files?  
**A:** The tool shows file size before processing. Very large files may take longer to process.

**Q:** What if my JSON has special characters?  
**A:** The tool automatically cleans non-printable characters before processing.

---
*Note: This tool was initially designed for processing Magic: The Gathering card data but works with any JSON files.*
