import json
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def select_file(title="Choose JSON file"):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title=title,
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    return file_path

def remove_specified_keys(data, keys_to_remove):
    if isinstance(data, dict):
        return {
            k: remove_specified_keys(v, keys_to_remove)
            for k, v in data.items()
            if k not in keys_to_remove
        }
    elif isinstance(data, list):
        return [remove_specified_keys(item, keys_to_remove) for item in data]
    return data


def remove_keys_from_file(file_path, keys_to_remove):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            raw_text = file.read()
        clean_text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', raw_text)
        data = json.loads(clean_text)
        cleaned_data = remove_specified_keys(data, keys_to_remove)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(cleaned_data, file, indent=4, ensure_ascii=False)

        return True
    except Exception as e:
        messagebox.showinfo("Error", "Error during the execution.")
        return False

if __name__ == "__main__":
    KEYS_TO_REMOVE = [
        "scryfall_uri", "uri", "released_at", "highres_image",
        "image_status", "games", "reserved", "game_changer",
        "foil", "nonfoil", "finishes", "oversized", "promo",
        "reprint", "variation", "set_id", "set_name", "set_type",
        "set_uri", "set_search_uri", "scryfall_set_uri", "rulings_uri",
        "prints_search_uri", "digital", "card_back_id", "artist",
        "artist_ids", "illustration_id", "border_color", "frame",
        "full_art", "textless", "booster", "story_spotlight",
        "prices", "related_uris", "purchase_uris", "arena_id",
        "tcgplayer_id", "layout", "set", "collector_number", "rarity",
        "edhrec_rank", "penny_rank", "cardmarket_id", "printed_text", "preview"
    ]

    input_path = select_file()

    if not input_path:
        messagebox.showinfo("Error", "File was not chosen")
        exit()

    file_size_mb = os.path.getsize(input_path) / (1024 * 1024)
    confirm = messagebox.askyesno(
        "Confirmation",
        f"File: {os.path.basename(input_path)}\n"
        f"Size: {file_size_mb:.2f} MB\n"
        f"Will remove {len(KEYS_TO_REMOVE)} keys.\nDo you agree?",
        icon='warning'
    )

    if confirm:
        success = remove_keys_from_file(input_path, KEYS_TO_REMOVE)
        if success:
            messagebox.showinfo("Success", "The file was successfuly redacted.")
        else:
            messagebox.showinfo("Error", "Error during the execution.")
    else:
        messagebox.showinfo("Error","The operation was declaned")
