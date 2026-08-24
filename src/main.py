import os
import shutil
import sys

from textnode_funcs import markdown_to_html_node

DIR_BASE_PATH = "/"
DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./docs"
DIR_PATH_CONTENT = "./content"
TEMPLATE_PATH = "./template.html"

def generate_page(base_path: str,from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(template_path, 'r') as template_file:
        template = template_file.read()

    with open(from_path, 'r') as from_file:
        content = from_file.read()

    html = markdown_to_html_node(content).to_html()

    title = extract_title(content)

    final_html = template.replace(
        "{{ Title }}", title
    ).replace(
        "{{ Content }}", html
    ).replace(
        "href=\"/", f"href=\"{base_path}"
    ).replace(
        "src=\"/", f"src=\"{base_path}"
    )

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(final_html)
    
def extract_title(markdown: str):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown content. Title should be the first line starting with '# '")

def copy_files(source_dir=DIR_PATH_STATIC, dest_dir=DIR_PATH_PUBLIC):
    # delete all contents in dest_dir
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir, exist_ok=True)

    # Copy all file and subdirectories, nested files, etc.
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(dest_dir, item)
        if os.path.isdir(s):
            print(f"Copying directory: {s} to {d}")
            copy_files(s, d)
        else:
            print(f"Copying file: {s} to {d}")
            shutil.copy2(s, d)

def generate_page_recursive(base_path=DIR_BASE_PATH, dir_path_content=DIR_PATH_CONTENT, template_path=TEMPLATE_PATH, dir_path_public=DIR_PATH_PUBLIC):
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dir_path_public, relative_path[:-3] + ".html")
                generate_page(base_path, from_path, template_path, dest_path)

if __name__ == "__main__":
    basepath = DIR_BASE_PATH

    if len(sys.argv) > 1 and sys.argv[1] is not None:
        basepath = sys.argv[1]

    if basepath[-1] != '/':
        basepath += '/'

    copy_files(DIR_PATH_STATIC, DIR_PATH_PUBLIC)
    generate_page_recursive(basepath, DIR_PATH_CONTENT, TEMPLATE_PATH, DIR_PATH_PUBLIC)