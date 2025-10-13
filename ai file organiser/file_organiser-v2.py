import os
import shutil
import json
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

# ---------- CONFIG ----------
AI_ENDPOINT = "https://unsquinting-anderson-unhogged.ngrok-free.dev"
USE_AI = True  # default enable AI; user can toggle
MANIFEST_FILENAME = ".organizer_manifest.json"
AUTO_FOLDERS = ["Images", "Videos", "Documents", "Audio", "Archives", "Others"]
# ----------------------------

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


def scan_folder_simple(folder):
    """
    Scan folder and return dict: {file_path: suggested_category} without subfolders grouping.
    We'll group later.
    """
    mapping = {}
    for root, _, files in os.walk(folder):
        for file in files:
            full = os.path.join(root, file)
            ext = os.path.splitext(file)[1]
            mapping[full] = detect_category(ext)
    return mapping


def call_ai_sorter(file_paths):
    """
    Call remote AI endpoint with list of file paths (or maybe just basenames)
    Expect response like: { "filepath1": "Images", "filepath2": "Documents", ... }
    """
    try:
        payload = {"files": file_paths}
        resp = requests.post(AI_ENDPOINT, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        messagebox.showwarning("AI Error", f"Failed to call AI API: {e}")
        return {}


def build_structure_from_mapping(mapping):
    """
    mapping: { file_path: category }
    Return nested dict: structure[category][ext_upper] = [files]
    """
    structure = {}
    for fpath, cat in mapping.items():
        ext = os.path.splitext(fpath)[1].upper() or "NOEXT"
        structure.setdefault(cat, {}).setdefault(ext, []).append(fpath)
    return structure


def apply_sort(folder, file_structure):
    """Move files and record manifest."""
    manifest = {"moved": [], "timestamp": datetime.now().isoformat()}
    for category, exts in file_structure.items():
        for ext, files in exts.items():
            # create subfolder name, e.g., folder/Images/JPG
            target_folder = os.path.join(folder, category, ext.replace(".", ""))
            os.makedirs(target_folder, exist_ok=True)
            for f in files:
                try:
                    dest = os.path.join(target_folder, os.path.basename(f))
                    shutil.move(f, dest)
                    manifest["moved"].append({"from": f, "to": dest})
                except Exception as e:
                    print("Error moving:", f, "->", e)
    manifest_path = os.path.join(folder, MANIFEST_FILENAME)
    with open(manifest_path, "w") as mf:
        json.dump(manifest, mf, indent=2)
    return manifest_path


def cleanup_auto_folders(root_folder):
    """Remove empty auto-created folders."""
    for af in AUTO_FOLDERS:
        p = os.path.join(root_folder, af)
        if os.path.exists(p) and not os.listdir(p):
            try:
                os.rmdir(p)
                print(f"Removed empty folder: {p}")
            except Exception as e:
                print(f"Could not remove {p}: {e}")


def revert_changes(folder):
    """Revert based on manifest + cleanup."""
    manifest_path = os.path.join(folder, MANIFEST_FILENAME)
    if not os.path.exists(manifest_path):
        messagebox.showwarning("Revert", "No manifest found.")
        return
    with open(manifest_path, "r") as mf:
        manifest = json.load(mf)
    # revert in reverse order
    for move in reversed(manifest.get("moved", [])):
        try:
            os.makedirs(os.path.dirname(move["from"]), exist_ok=True)
            shutil.move(move["to"], move["from"])
        except Exception as e:
            print("Error reverting:", e)
    cleanup_auto_folders(folder)
    messagebox.showinfo("Revert", "Changes reverted successfully!")


class OrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Folder Organizer")
        self.geometry("800x600")
        self.folder_path = tk.StringVar()
        self.use_ai = tk.BooleanVar(value=USE_AI)
        self.structure = None
        self.build_ui()

    def build_ui(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill="both", expand=True)

        # Folder selection
        lbl = ttk.Label(frm, text="Select Folder:")
        lbl.grid(row=0, column=0, sticky="w")
        ent = ttk.Entry(frm, textvariable=self.folder_path, width=60)
        ent.grid(row=0, column=1, padx=5, sticky="w")
        btn = ttk.Button(frm, text="Browse", command=self.select_folder)
        btn.grid(row=0, column=2, padx=5)

        # AI toggle
        chk = ttk.Checkbutton(frm, text="Use AI Server", variable=self.use_ai)
        chk.grid(row=1, column=0, sticky="w")

        # Scan / apply / revert buttons
        btn_scan = ttk.Button(frm, text="Scan", command=self.scan_action)
        btn_scan.grid(row=1, column=1, sticky="w", padx=5)
        btn_apply = ttk.Button(frm, text="Apply", command=self.apply_action)
        btn_apply.grid(row=1, column=2, sticky="w", padx=5)
        btn_revert = ttk.Button(frm, text="Revert", command=self.revert_action)
        btn_revert.grid(row=1, column=3, sticky="w", padx=5)

        # Tree preview
        self.tree = ttk.Treeview(frm, columns=("ext", "count"), show="tree headings")
        self.tree.heading("#0", text="Category / Extension / Files")
        self.tree.heading("ext", text="Ext")
        self.tree.heading("count", text="Count")
        self.tree.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)

        # Configure row/column weights
        frm.rowconfigure(2, weight=1)
        frm.columnconfigure(1, weight=1)

    def select_folder(self):
        p = filedialog.askdirectory()
        if p:
            self.folder_path.set(p)

    def scan_action(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("Error", "Please select a folder.")
            return

        # Step 1: get simple mapping by ext
        mapping = scan_folder_simple(folder)

        # Step 2: if AI enabled, override mapping with AI result
        if self.use_ai.get():
            # Send just file paths (or maybe just basenames) to AI
            paths = list(mapping.keys())
            ai_res = call_ai_sorter(paths)
            # ai_res expected: { file_path: category }
            for fpath, cat in ai_res.items():
                # override
                mapping[fpath] = cat

        # Build structure for preview / sorting
        self.structure = build_structure_from_mapping(mapping)

        # Show in tree
        self.tree.delete(*self.tree.get_children())
        for cat, exts in self.structure.items():
            parent = self.tree.insert("", "end", text=cat, values=("", sum(len(v) for v in exts.values())))
            for ext, files in exts.items():
                child = self.tree.insert(parent, "end", text=ext, values=(ext, len(files)))
                for f in files[:5]:
                    self.tree.insert(child, "end", text=os.path.basename(f))

        messagebox.showinfo("Scan Complete", "Scan & AI classification done.")

    def apply_action(self):
        folder = self.folder_path.get()
        if not folder or self.structure is None:
            messagebox.showwarning("Error", "Scan first.")
            return
        manifest = apply_sort(folder, self.structure)
        messagebox.showinfo("Done", f"Files moved. Manifest saved at:\n{manifest}")

    def revert_action(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("Error", "Select folder first.")
            return
        revert_changes(folder)


if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()
