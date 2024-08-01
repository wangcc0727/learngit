import os
import sys
import stat

def get_dir_size(path, depth, ino_list, path_dev = None):
    
    depth -= 1
    path_stat = os.lstat(path)
    dir_size = path_stat.st_size
    if path_dev == None:
        path_dev = path_stat.st_dev

    dirs = os.listdir(path)
    file_size = 0

    for f in dirs:
        file_path = os.path.join(path, f)
        file_path_stat = os.lstat(file_path)

        if path_dev != file_path_stat.st_dev:
                continue

        if file_path_stat.st_nlink > 1:
            file_ino = file_path_stat.st_ino
            if file_ino in ino_list:
                continue
            ino_list.add(file_ino)    

        if stat.S_ISDIR(file_path_stat.st_mode):
            sub_dir_size = get_dir_size(file_path, depth, ino_list, path_dev)
            dir_size += sub_dir_size
            if depth == 0:
                print(f"{sub_dir_size}      {file_path}")
        else:
            file_size += file_path_stat.st_size

    dir_size += file_size
    if depth >= 0:
        print(f"{dir_size}      {path}")
    return dir_size

if __name__ == "__main__":
    depth = int(sys.argv[1])
    paths = sys.argv[2:]
    ino_list = set()
    for path in paths:
        get_dir_size(path, depth, ino_list)
