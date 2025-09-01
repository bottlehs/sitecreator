import os
import re
from bs4 import BeautifulSoup
from tkinter import messagebox



def get_folders_in_path(path):
    folders = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            folders.append(item)
    return folders


def edit_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        html_content = re.sub(r'<!--[\s\S]*?-->', '', html_content)

        # Remove JavaScript-style comments
        html_content = re.sub(r'\/\*[\s\S]*?\*\/', '', html_content)

        html_content = re.sub(r'\{#', '{ #', html_content)

        soup = BeautifulSoup(html_content, 'html.parser')
        for element in soup.find_all(text=lambda text: '{{' in text and '}}' in text):
            # Replace the element's text with an empty string
            element.replace_with('')

        for tag in soup.find_all(href=True):
            href = tag['href']
            if "http" not in href:
                tag['href'] = "{{ url_for('static', filename='" + href + "') }}"

        for tag in soup.find_all(src=True):
            src = tag['src']
            if "http" not in src:
                tag['src'] = "{{ url_for('static', filename='" + src + "') }}"

        for center_tag in soup.find_all('center'):
            if center_tag.get_text().lower().find("free version") != -1:
                center_tag.extract()
            if center_tag.get_text().lower().find("free demo") != -1:
                center_tag.extract()

        modified_content = str(soup)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)

    except FileNotFoundError:
        print('Fine not found.')
    except Exception as e:
        print(f"An error occurred: {e}")

def clean_html(path):
    path = os.path.join(path, 'white.html')
    if os.path.exists(path):
        edit_html_file(path)
        messagebox.showinfo("성공", f"폴더 정리")