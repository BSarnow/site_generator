import os
import shutil

def copying_static_content(path,path_copy):
    delet_content = os.listdir("/home/shura/workspace/github.com/BSarnow/public/")
    never_delet = ["src", "static", "main.sh", "index.html", "styles.css", "test.sh", ".gitignore", ".git", ".", ".."]
    for item in delet_content:
        if item not in never_delet:
            copy_path = os.path.join(path_copy, item)
            if os.path.exists(copy_path):
                if os.path.isfile(copy_path):
                    print(f"delet old file {copy_path}")
                    os.remove(copy_path)
                else:
                    print(f"delet old dict and all its content {copy_path}")
                    shutil.rmtree(copy_path)
    static_path = path
    content = os.listdir(static_path)
    for i in range(len(content)):
        original_path = os.path.join(static_path,content[i])
        print(original_path)
        copy_path = os.path.join(path_copy,content[i])
        print(copy_path)
        if os.path.isfile(original_path):
            shutil.copy(original_path, copy_path)
        else:
            os.mkdir(copy_path)
            copying_static_content(original_path, copy_path)

copying_static_content("/home/shura/workspace/github.com/BSarnow/public/static/", "/home/shura/workspace/github.com/BSarnow/public/")