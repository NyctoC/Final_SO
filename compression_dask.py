import shutil
import tarfile
import zipfile
import dask
from dask import delayed, compute
import os
import tempfile

@delayed
def compress_zip(source_dir, output_file):
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, source_dir)
                zf.write(full_path, arcname)

@delayed
def compress_tar(source_dir, output_file, mode='w:gz'):
    with tarfile.open(output_file, mode) as tf:
        tf.add(source_dir, arcname=".")

def run_compression(source_dir, method, output_file):
    if method == 'zip':
        return compute(compress_zip(source_dir, output_file))
    elif method == 'gzip':
        return compute(compress_tar(source_dir, output_file, 'w:gz'))
    elif method == 'bzip2':
        return compute(compress_tar(source_dir, output_file, 'w:bz2'))
    else:
        raise ValueError("Unsupported compression method")

@delayed
def _copy_to_temp(path, temp_dir):
    base_name = os.path.basename(path)
    dest = os.path.join(temp_dir, base_name)
    if os.path.isdir(path):
        shutil.copytree(path, dest)
    else:
        shutil.copy2(path, dest)
    return dest

def compress_all_to_one(paths, output_file, method):
    with tempfile.TemporaryDirectory() as temp_dir:
        tasks = [_copy_to_temp(path, temp_dir) for path in paths]
        dask.compute(*tasks)

        if method == "zip":
            with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        abs_path = os.path.join(root, file)
                        rel_path = os.path.relpath(abs_path, temp_dir)
                        zipf.write(abs_path, arcname=rel_path)

        elif method in ["gzip", "bzip2"]:
            # Limita a un solo archivo concatenado
            concat_path = os.path.join(temp_dir, "concatenated")
            with open(concat_path, "wb") as f_out:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        with open(os.path.join(root, file), "rb") as f_in:
                            shutil.copyfileobj(f_in, f_out)

            if method == "gzip":
                with open(concat_path, "rb") as f_in, gzip.open(output_file, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            elif method == "bzip2":
                with open(concat_path, "rb") as f_in, bz2.open(output_file, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
        else:
            raise ValueError("Unsupported compression method")