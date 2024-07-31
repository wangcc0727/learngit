import os

def get_dir_size(dir_path, ino_list):
    size = 0
    for root, dirs, files in os.walk(dir_path):

        size += os.path.getsize(root)
        for f in files:
            f_path = os.path.join(root, f)
            if os.path.islink(f_path):
                size += os.lstat(f_path).st_size
                continue
            if os.path.ismount(f_path):
                continue
            f_ino = os.stat(f_path).st_ino
            if f_ino in ino_list:
                continue
            size += os.path.getsize(f_path)
            ino_list.add(f_ino)

        for d in dirs:
            dir_path = os.path.join(root, d)
            if os.path.islink(dir_path):
                size += os.lstat(dir_path).st_size

    return size

def get_files(path):
    file_list = os.listdir(path)
    files = [fl for fl in file_list if os.path.isfile(os.path.join(path, fl))]
    return files

def get_dirs(path):
    dir_list = os.listdir(path)
    dirs = [dr for dr in dir_list if os.path.isdir(os.path.join(path, dr))]
    return dirs

def main(path):
    dirs = get_dirs(path)
    files = get_files(path)
    ino_list = set()
    
    total_size = 0
    for dr in dirs:
        dir_path = os.path.join(path, dr)
        if os.path.islink(dir_path):
            dir_size += os.lstat(dir_path).st_size
            continue
        if os.path.ismount(dir_path):
            continue
        dir_ino = os.stat(dir_path).st_ino
        if dir_ino in ino_list:
            continue
        dir_size = get_dir_size(dir_path, ino_list)
        ino_list.add(dir_ino)
        total_size += dir_size
        print(f"{dir_size}      {dir_path}")
    
    file_size = 0
    for fl in files:
        file_path = os.path.join(path, fl)
        if os.path.islink(file_path):
            file_size += os.lstat(file_path).st_size
            continue
        if os.path.ismount(file_path):
            continue
        file_ino = os.stat(file_path).st_ino
        if file_ino in ino_list:
            continue
        file_size += os.path.getsize(file_path)
        ino_list.add(file_ino)
    file_size += os.path.getsize(path)
    print(f"{file_size + total_size}      {path}")
    return 0

if __name__ == "__main__":
    print("input path:")
    path = input().strip()
    main(path)
#    print(ino_list)
