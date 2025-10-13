import os
import shutil
import json
import mimetypes
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

# ---------- CONFIG ----------
AI_ENDPOINT = "http://localhost:8000/sort"  # local AI API endpoint (customizable)
USE_AI = False  # toggle AI categorization
MANIFEST_FILENAME = ".organizer_manifest.json"
AUTO_FOLDERS = ["Images", "Videos", "Documents", "Audio", "Others"]
# ----------------------------

# File type mapping
CATEGORY_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
}


def detect_category(ext):
    for category, exts in CATEGORY_MAP.items():
        if ext.lower() in exts:
            return category
    return "Others"


def scan_folder(folder):
    """Scan folder and return dict {category: {extension: [files]}}"""
    data = {}
    for root, _, files in os.walk(folder):
        for file in files:
            ext = os.path.splitext(file)[1]
            category = detect_category(ext)
            data.setdefault(category, {}).setdefault(ext.upper() or "NOEXT", []).append(os.path.join(root, file))
    return data


def call_ai_sorter(file_paths):
    """Optional AI-based categorization"""
    try:
        resp = requests.post(AI_ENDPOINT, json={"files": file_paths}, timeout=30)
        return resp.json()
    except Exception as e:
        messagebox.showwarning("AI Error", f"Failed to call AI API: {e}")
        return {}


def apply_sort(folder, file_structure):
    """Move files into subfolders and record a manifest for revert"""
    manifest = {"moved": [], "timestamp": datetime.now().isoformat()}
    for category, exts in file_structure.items():
        for ext, files in exts.items():
            target_folder = os.path.join(folder, category, ext.replace(".", "").upper())
            os.makedirs(target_folder, exist_ok=True)
            for f in files:
                try:
                    dest = os.path.join(target_folder, os.path.basename(f))
                    shutil.move(f, dest)
                    manifest["moved"].append({"from": f, "to": dest})
                except Exception as e:
                    print("Error moving:", f, "->", e)
    manifest_path = os.path.join(folder, MANIFEST_FILENAME)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    return manifest_path


def cleanup_auto_folders(root_folder):
    """Remove empty auto-created folders after revert"""
    for folder in AUTO_FOLDERS:
        path = os.path.join(root_folder, folder)
        if os.path.exists(path) and not os.listdir(path):
            try:
                os.rmdir(path)
                print(f"🧹 Removed empty auto-folder: {folder}")
            except Exception as e:
                print(f"⚠️ Could not remove {path}: {e}")


def revert_changes(folder):
    """Revert moves based on manifest and cleanup empty folders"""
    manifest_path = os.path.join(folder, MANIFEST_FILENAME)
    if not os.path.exists(manifest_path):
        messagebox.showwarning("Revert", "No manifest found.")
        return
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    for move in reversed(manifest["moved"]):
        try:
            os.makedirs(os.path.dirname(move["from"]), exist_ok=True)
            shutil.move(move["to"], move["from"])
        except Exception as e:
            print("Error reverting:", e)
    cleanup_auto_folders(folder)
    messagebox.showinfo("Revert", "Changes reverted successfully!")


# ---------- UI ----------
class OrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Folder Organizer")
        self.geometry("700x500")
        self.configure(bg="#1e1e1e")
        self.folder_path = tk.StringVar()
        self.result_text = tk.StringVar()
        self.build_ui()

    def build_ui(self):
        frm = ttk.Frame(self, padding=20)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Select Folder:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        folder_frame = ttk.Frame(frm)
        folder_frame.pack(fill="x", pady=5)
        ttk.Entry(folder_frame, textvariable=self.folder_path, width=60).pack(side="left", padx=(0, 5))
        ttk.Button(folder_frame, text="Browse", command=self.select_folder).pack(side="left")

        ttk.Button(frm, text="Scan Folder", command=self.scan_folder).pack(pady=10)
        ttk.Button(frm, text="Apply Sorting", command=self.apply_sort_action).pack(pady=5)
        ttk.Button(frm, text="Revert Changes", command=self.revert_changes_action).pack(pady=5)

        self.tree = ttk.Treeview(frm, columns=("ext", "count"), show="tree headings")
        self.tree.heading("#0", text="Category / File Path")
        self.tree.heading("ext", text="Extension")
        self.tree.heading("count", text="Count")
        self.tree.pack(fill="both", expand=True, pady=10)

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)

    def scan_folder(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("Error", "Please select a folder.")
            return
        self.tree.delete(*self.tree.get_children())
        structure = scan_folder(folder)

        # Optionally call AI
        if USE_AI:
            ai_res = call_ai_sorter([f for cat in structure.values() for ext in cat.values() for f in ext])
            print("AI result:", ai_res)

        for category, exts in structure.items():
            cat_id = self.tree.insert("", "end", text=category, values=("", sum(len(v) for v in exts.values())))
            for ext, files in exts.items():
                sub_id = self.tree.insert(cat_id, "end", text=f"{ext}", values=(ext, len(files)))
                for f in files[:5]:  # show preview
                    self.tree.insert(sub_id, "end", text=f)

        self.structure = structure
        messagebox.showinfo("Scan Complete", "Folder scanned successfully!")

    def apply_sort_action(self):
        folder = self.folder_path.get()
        if not folder or not hasattr(self, "structure"):
            messagebox.showwarning("Error", "Scan folder first.")
            return
        manifest = apply_sort(folder, self.structure)
        messagebox.showinfo("Sorting Done", f"Files organized. Manifest saved at:\n{manifest}")

    def revert_changes_action(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("Error", "Please select a folder.")
            return
        revert_changes(folder)


if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()
