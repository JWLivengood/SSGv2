import os
import shutil
from markdown_processor import markdown_to_html, extract_title

def source_to_public(source_dir, dest_dir):
#    print(f"Deleting contents of {dest_dir}")
    shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    os.chdir(source_dir)
#    print(f"current directory = {os.getcwd()}")
#    print(f"Files in current directory:\n{os.listdir()}")
    for file in os.listdir(source_dir):
        full_file_path = os.path.join(source_dir, file)
        full_dest_path = os.path.join(dest_dir, file)
#        print(f"Testing if {full_file_path} is a directory")
        if os.path.isdir(full_file_path) is True:
#            print(f"True. Creating {file} folder in {dest_dir}")
            os.mkdir(full_dest_path)
            source_to_public(full_file_path, full_dest_path)
        else:
#            print(f"False. File = {file}")
#            print(f"Attempting to copy file to {dest_dir}")
            shutil.copy(full_file_path, dest_dir)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, 'r', encoding='utf-8') as fhand:
        fmarkdown = fhand.read()
            
    with open(template_path) as thand:
        tfile = thand.read()

#    print(f"markdown = {fmarkdown}")
#    print(f"template = {tfile}")

    html_string = markdown_to_html(fmarkdown)
    title = extract_title(fmarkdown)
#    print(f"HTML String: {html_string}")

    replaced1 = tfile.replace("{{ Title }}", title)
    new_content = replaced1.replace("{{ Content }}", html_string)

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(new_content)
#    print(f"Generated HTML: {new_content}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        full_file_path = os.path.join(dir_path_content, file)
        full_dest_path = os.path.join(dest_dir_path, file)
        #        print(f"Testing if {full_file_path} is a directory")

        if os.path.isdir(full_file_path):
            print(f"Creating Sub Folder '{file}' in {dest_dir_path}")
            os.makedirs(full_dest_path, exist_ok=True)
            generate_pages_recursive(full_file_path, template_path, full_dest_path)

        else:
            if file.endswith('.md'):
                print(f"converting {file} to {file[:-3]}.html and copying to {dest_dir_path}")
                html_path = (os.path.join(dest_dir_path, f"{file[:-3]}.html"))
#                print(html_path)
                with open(full_file_path, 'r', encoding='utf-8') as fhand:
                    fmarkdown = fhand.read()
#                print(fmarkdown) 

                with open(template_path) as thand:
                    tfile = thand.read()

#               print(f"markdown = {fmarkdown}")
#               print(f"template = {tfile}")

                html_string = markdown_to_html(fmarkdown)
                title = extract_title(fmarkdown)
#               print(f"HTML String: {html_string}")

                replaced1 = tfile.replace("{{ Title }}", title)
                new_content = replaced1.replace("{{ Content }}", html_string)

                with open(html_path, 'w') as file:
                    file.write(new_content)

            else:
                shutil.copy(full_file_path, full_dest_path)



    '''
    with open(from_path, 'r', encoding='utf-8') as fhand:
        fmarkdown = fhand.read()
            
    with open(template_path) as thand:
        tfile = thand.read()

#    print(f"markdown = {fmarkdown}")
#    print(f"template = {tfile}")

    html_string = markdown_to_html(fmarkdown)
    title = extract_title(fmarkdown)
#    print(f"HTML String: {html_string}")

    replaced1 = tfile.replace("{{ Title }}", title)
    new_content = replaced1.replace("{{ Content }}", html_string)

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(new_content)
#    print(f"Generated HTML: {new_content}")
'''
