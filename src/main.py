import os
import shutil
from functions import generate_page, generate_page_recursiv

def copying_static_content(path=None,path_copy=None):
    if path == None:
        path = "/home/shura/workspace/github.com/BSarnow/site_generator/static/"
    if path_copy == None:
        path_copy = "/home/shura/workspace/github.com/BSarnow/site_generator/public/"
    delet_content = os.listdir("/home/shura/workspace/github.com/BSarnow/site_generator/public")
    never_delet = ["src", "static", "main.sh", "styles.css", "test.sh", ".gitignore", ".git", ".", ".."]
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
        copy_path = os.path.join(path_copy,content[i])
        if os.path.isfile(original_path):
            print(f"copy file from {original_path} to {copy_path}")
            shutil.copy(original_path, copy_path)
        else:
            print(f"copy dict from {original_path} to {copy_path}")
            os.mkdir(copy_path)
            copying_static_content(original_path, copy_path)
copying_static_content()
#generate_page("/home/shura/workspace/github.com/BSarnow/site_generator/content/index.md","/home/shura/workspace/github.com/BSarnow/site_generator/template.html","/home/shura/workspace/github.com/BSarnow/site_generator/public/index.html")
generate_page_recursiv("/home/shura/workspace/github.com/BSarnow/site_generator/content/","/home/shura/workspace/github.com/BSarnow/site_generator/template.html","/home/shura/workspace/github.com/BSarnow/site_generator/public/")