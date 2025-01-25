import os
import shutil


# from os.path import isdir
def check_src_dir(src: str):
    full_src_path = os.path.join(".", src)
    # Check if the src path exists
    if not os.path.exists(full_src_path):
        raise Exception(f"source path '{full_src_path}' does not exist")

    # Check if the src is a directory
    if not os.path.isdir(full_src_path):
        raise Exception(f"The provided source is not a directory")


def check_dest_dir(dest: str):
    full_dest_path = os.path.join(".", dest)
    # if dest path exists and is a directory
    if os.path.exists(full_dest_path) and os.path.isdir(full_dest_path):
        # delete the existing dest folder
        shutil.rmtree(full_dest_path)

    # create the dest folder
    os.mkdir(full_dest_path)


def copy_files(src: str, dest: str):
    check_src_dir(src)
    check_dest_dir(dest)

    src_dir_path = os.path.join(".", src)

    for entry in os.listdir(src_dir_path):
        src_item = os.path.join(src_dir_path, entry)
        if os.path.isfile(src_item):
            src_file_path = src_item
            dest_file_path = src_file_path.replace(src, dest)
            print(f"  Copy file: '{src_file_path}' -> '{dest_file_path}'")
            shutil.copy(src_file_path, dest_file_path)
        else:
            src_dir = src_item
            dest_dir = src_item.replace(src, dest)
            print(f"Copy directory: '{src_dir}' => '{dest_dir}'")
            os.makedirs(dest_dir, exist_ok=True)
            copy_files(src_dir, dest_dir)
