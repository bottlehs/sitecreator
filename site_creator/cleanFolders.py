import os
import uuid
import shutil

def get_folders_in_path(path):
    folders = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            folders.append(item)
    return folders


def move_files_to_static(source_dir, target_dir):
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            target_item = os.path.join(target_dir, item)

            if os.path.isfile(source_item):
                if item == 'index.html':
                    continue
                shutil.move(source_item, target_item)
            elif os.path.isdir(source_item):
                shutil.copytree(source_item, target_item)


        for item in os.listdir(os.path.dirname(target_dir)):
            if os.path.isdir(
                    os.path.join(os.path.dirname(target_dir), item)) and item not in target_dir and item != 'index.html':
                shutil.rmtree(os.path.join(os.path.dirname(target_dir), item))

        os.rename(target_dir, os.path.join(os.path.dirname(target_dir), 'static'))


    except FileNotFoundError:
        print("Source directory not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def clean_folder(path):
    if os.path.exists(os.path.join(path, 'white.html')):
        print("❌ 이미 진행 완료")

    else:
        move_files_to_static(path, os.path.join(path, str(uuid.uuid4())))
        static_path = os.path.join(path, 'static')
        shutil.make_archive(static_path, 'zip', static_path)

        index_path = os.path.join(path, 'index.html')
        white_path = os.path.join(path, 'white.html')
        if os.path.exists(index_path):
            os.rename(index_path, white_path)
        print("✅ 폴더 정리 완료")