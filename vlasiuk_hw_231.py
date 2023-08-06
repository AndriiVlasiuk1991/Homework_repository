import shutil
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def process_file(file_path, sorted_folder):
    sorted_folder.mkdir(parents=True, exist_ok=True)
    shutil.move(file_path, sorted_folder / file_path.name)
    logging.info(f"Файл {file_path.name} було перенесено до папки {sorted_folder.name}")


def process_folder(path, threads_num=4):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(console_handler)

    try:
        with ThreadPoolExecutor(max_workers=threads_num) as execut:
            files = list(path.glob("*"))
            for file in files:
                if file.is_file():
                    destination_folder = path / file.suffix[1:]
                    execut.submit(process_file, file, destination_folder)
    except Exception as exc:
        logging.error(f"Помилка обробки папки {path}: {exc}")


if __name__ == '__main__':
    folder_name = input("Введіть назву папки: ")
    folder_path = Path(folder_name)
    if folder_path.exists() and folder_path.is_dir():
        process_folder(folder_path)
    else:
        print(f"Папка {folder_name} не знайдена або не є директорією.")
