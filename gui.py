import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.filedialog import asksaveasfilename
import dropbox
import os

from compression_dask import compress_all_to_one
from encryption_dask import encrypt_file_dask, decrypt_file_dask  # Asegúrate de tener esta función

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SIRC")
        self.root.geometry("1080x720")
        self.root.configure(bg="#f0f0f0")

        self.files = []
        self.folders = []
        self.compression_type = tk.StringVar(value="zip")
        self.encrypt = tk.BooleanVar(value=False)
        self.password = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="SIRC Backup System", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)

        tk.Button(self.root, text="Select Files", command=self.select_files).pack(pady=5)
        tk.Button(self.root, text="Select Folders", command=self.select_folders).pack(pady=5)

        self.path_label = tk.Label(self.root, text="No files or folders selected", bg="#f0f0f0")
        self.path_label.pack()

        tk.Label(self.root, text="Compression Type:", bg="#f0f0f0").pack(pady=(20, 0))
        tk.OptionMenu(self.root, self.compression_type, "zip", "gzip", "bzip2").pack()

        tk.Checkbutton(self.root, text="Encrypt backup", variable=self.encrypt, bg="#f0f0f0", command=self.toggle_password).pack(pady=10)
        self.password_entry = tk.Entry(self.root, textvariable=self.password, show="*", state="disabled")
        self.password_entry.pack()

        tk.Button(self.root, text="Run Backup", command=self.run_backup, bg="#007acc", fg="white").pack(pady=20)
        tk.Button(self.root, text="Decrypt File", command=self.run_decrypt, bg="#444", fg="white").pack(pady=5)

    def toggle_password(self):
        self.password_entry.config(state="normal" if self.encrypt.get() else "disabled")

    def select_files(self):
        files = filedialog.askopenfilenames()
        if files:
            self.files = list(files)
            self.update_path_label()

    def select_folders(self):
        folders = []
        while True:
            folder = filedialog.askdirectory()
            if not folder:
                break
            folders.append(folder)
        if folders:
            self.folders = folders
            self.update_path_label()

    def update_path_label(self):
        all_paths = self.files + self.folders
        if all_paths:
            display_text = "\n".join(all_paths[:5])
            if len(all_paths) > 5:
                display_text += f"\n(+{len(all_paths)-5} more)"
            self.path_label.config(text=display_text)
        else:
            self.path_label.config(text="No files or folders selected")

    def run_backup(self):
        targets = self.files + self.folders
        if not targets:
            messagebox.showerror("Error", "Please select at least one file or folder.")
            return

        # Elegir la ruta de guardado
        save_path = asksaveasfilename(defaultextension=f".{self.compression_type.get()}",
                                       filetypes=[("All files", "*.*")])
        if not save_path:
            messagebox.showinfo("Canceled", "No save path selected.")
            return

        try:
            compress_all_to_one(targets, save_path, self.compression_type.get())

            if self.encrypt.get():
                encrypted_file = save_path + ".enc"
                encrypt_file_dask(save_path, encrypted_file, self.password.get())
                os.remove(save_path)
                save_path = encrypted_file
                final_message = f"Backup created and encrypted: {save_path}"
            else:
                final_message = f"Backup created: {save_path}"

            messagebox.showinfo("Success", final_message)

            upload = messagebox.askyesno("Dropbox", "¿Quieres subir este backup a Dropbox?")
            if upload:
                try:
                    self.upload_to_dropbox(save_path, "/backups/" + os.path.basename(save_path), token="___")
                    messagebox.showinfo("Dropbox", "Backup subido exitosamente.")
                except Exception as e:
                    messagebox.showerror("Error al subir", str(e))

        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")

    def run_decrypt(self):
        encrypted_path = filedialog.askopenfilename(title="Select Encrypted File")
        if not encrypted_path:
            return

        decrypted_path = asksaveasfilename(title="Save Decrypted File As")
        if not decrypted_path:
            return

        if not self.password.get():
            messagebox.showerror("Error", "Please enter the password to decrypt.")
            return

        try:
            decrypt_file_dask(encrypted_path, decrypted_path, self.password.get())
            messagebox.showinfo("Success", f"File decrypted successfully:\n{decrypted_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")

    def upload_to_dropbox(self, local_path, dropbox_path, token):
        dbx = dropbox.Dropbox(token)
        with open(local_path, "rb") as f:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
