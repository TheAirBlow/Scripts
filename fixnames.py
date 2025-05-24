# 1. fixes broken unicode filenames and directory names e.g. mojibale from incorrectly extracted archives
# 2. fixes uppercase extensions and forces them to lowercase to make sure everything works correctly with e.g. scompress
# 3. renames .jpe and .jfif to .jpeg for better compatibility

import uuid
import os

for root, dirs, files in os.walk(b'.', topdown=False):
    for filename in files:
        original_path = os.path.join(root, filename)
        try:
            filename.decode('utf-8')
        except UnicodeDecodeError:
            _, ext = os.path.splitext(filename)
            new_filename = str(uuid.uuid4()).encode() + ext
            new_path = os.path.join(root, new_filename)
            print(f"{filename} -> {new_filename}")
            os.rename(original_path, new_path)
            filename = new_filename
            original_path = new_path

        name, ext = os.path.splitext(filename)

        lower_ext = ext.lower()
        if lower_ext in [b'.jpe', b'.jfif']:
            new_ext = b'.jpeg'
        else:
            new_ext = lower_ext

        if ext != new_ext:
            new_filename = name + new_ext
            new_path = os.path.join(root, new_filename)
            print(f"{filename} -> {new_filename}")
            os.rename(original_path, new_path)

    for dirname in dirs:
        try:
            dirname.decode('utf8')
        except:
            new = str(uuid.uuid4()).encode()
            old_path = os.path.join(root, dirname)
            new_path = os.path.join(root, new)
            print(dirname, '->', new)
            os.rename(old_path, new_path)
