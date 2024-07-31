import os
import sys
import stat

def get_size(path, ino_list):
    size = 0
    path_stat = os.lstat(path)
    size += path_stat.st_size
    for f in os.listdir(path):
        abspath = os.path.join(path, f)
        abspath_stat = os.lstat(abspath)

#       if stat.S_ISLNK(abspath_stat.st_mode):
#            size += abspath_stat.st_size
#            continue
        
        if path_stat.st_dev != abspath_stat.st_dev:
            continue
        if path_stat.st_ino == abspath_stat.st_ino:
            continue
        
        if abspath_stat.st_nlink > 1:
            f_ino = abspath_stat.st_ino
            if f_ino in ino_list:
                continue

        if not stat.S_ISDIR(abspath_stat.st_mode):
            size += abspath_stat.st_size
            if abspath_stat.st_nlink > 1:
                ino_list.add(f_ino)
        elif stat.S_ISDIR(abspath_stat.st_mode):
            size += get_size(abspath, ino_list)

    return size

def get_dir_size(path, depth):
    depth -= 1
    dirs = os.listdir(path)
    ino_list = set()
    path_stat = os.lstat(path)
    file_size = 0
    dir_size = path_stat.st_size

    for f in dirs:
        file_path = os.path.join(path, f)
        file_path_stat = os.lstat(file_path)
        
        if path_stat.st_dev != file_path_stat.st_dev:
                continue
        if path_stat.st_ino == file_path_stat.st_ino:
                continue

        if file_path_stat.st_nlink > 1:
            file_ino = file_path_stat.st_ino
            if file_ino in ino_list:
                continue

        if not stat.S_ISDIR(file_path_stat.st_mode):
            
            file_size += file_path_stat.st_size
            if file_path_stat.st_nlink > 1:
                ino_list.add(file_ino)
        
        elif depth <= 0:
            sub_dir_size = get_size(file_path, ino_list)
            dir_size += sub_dir_size
            print(f"{sub_dir_size}      {file_path}")
        else:
            sub_dir_size = get_dir_size(file_path, depth)
            dir_size += sub_dir_size

    dir_size += file_size
    print(f"{dir_size}      {path}")
    return dir_size

if __name__ == "__main__":
    depth = int(sys.argv[1])
    paths = sys.argv[2:]
    for path in paths:
        get_dir_size(path, depth)
