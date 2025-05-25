import shutil
import os
from dask import delayed, compute

@delayed
def copy_file_to_temp(src, dest_dir):
    file_name = os.path.basename(src)
    dest_path = os.path.join(dest_dir, file_name)
    shutil.copy2(src, dest_path)
    return dest_path

@delayed
def copy_folder_to_temp(folder_path, dest_dir):
    folder_name = os.path.basename(folder_path)
    dest_path = os.path.join(dest_dir, folder_name)
    shutil.copytree(folder_path, dest_path)
    return dest_path

def prepare_temp_directory(files, folders, temp_dir):
    os.makedirs(temp_dir, exist_ok=True)
    tasks = []

    for f in files:
        tasks.append(copy_file_to_temp(f, temp_dir))

    for d in folders:
        tasks.append(copy_folder_to_temp(d, temp_dir))

    return compute(*tasks)
