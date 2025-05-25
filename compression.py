import os
import zipfile
import gzip
import bz2
from pathlib import Path

def compress_zip(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, rel_path)

def compress_gzip(file_path, output_path):
    with open(file_path, 'rb') as f_in:
        with gzip.open(output_path, 'wb') as f_out:
            f_out.writelines(f_in)

def compress_bzip2(file_path, output_path):
    with open(file_path, 'rb') as f_in:
        with bz2.open(output_path, 'wb') as f_out:
            f_out.writelines(f_in)
