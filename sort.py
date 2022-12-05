from pathlib import Path
import os
import shutil
from sys import argv


argv_path = Path(argv[1])
if not Path(argv_path).exists():
    print("Path doesn't exist, please try again")
    exit()


images, videos, documents, music, archives, unknown_files = [], [], [], [], [], []
known_extensions, unknown_extensions = set(), set()
img_ext = (".jpeg", ".jpg", ".png", "svg")
vid_ext = (".avi", ".mp4", ".mov", ".mkv")
doc_ext = (".doc", ".docx", ".txt", ".pdf", ".pptx")
music_ext = (".mp3", ".ogg", ".wav", ".amr")
arch_ext = (".zip", ".gz", ".tar")
ignore_folders = ("archives", "video", "audio", "documents", "images")


def normalize(filename):
    """ 
    Translate cyrylic symbols to latin and replace symbols to '_' if symbols are not digit/alpha
    Returns string
    """

    translate_dict = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'yo',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'y',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'h',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'shch',
        'ъ': 'y',
        'ы': 'y',
        'ь': "'",
        'э': 'e',
        'ю': 'yu',
        'я': 'ya',
        'А': 'A',
        'Б': 'B',
        'В': 'V',
        'Г': 'G',
        'Д': 'D',
        'Е': 'E',
        'Ё': 'Yo',
        'Ж': 'Zh',
        'З': 'Z',
        'И': 'I',
        'Й': 'Y',
        'К': 'K',
        'Л': 'L',
        'М': 'M',
        'Н': 'N',
        'О': 'O',
        'П': 'P',
        'Р': 'R',
        'С': 'S',
        'Т': 'T',
        'У': 'U',
        'Ф': 'F',
        'Х': 'H',
        'Ц': 'Ts',
        'Ч': 'Ch',
        'Ш': 'Sh',
        'Щ': 'Shch',
        'Ъ': 'Y',
        'Ы': 'Y',
        'Ь': "'",
        'Э': 'E',
        'Ю': 'Yu',
        'Я': 'Ya',
    }
    latin_alpha = "abcdefghijklmnopqrstuvwxyz"
    new_string = ""
    for s in filename:
        if s in translate_dict:
            new_string += translate_dict[s]
        elif s.lower() not in latin_alpha and not s.isnumeric():
            new_string += "_"
        else:
            new_string += s

    return new_string


def sorter(path=argv_path):
    """
    Recursively walks in the target folder, moves files to appropriate folders

        Parameter:
            path (str): Path to target folder

    """

    target_dir = Path(path)
    for file in target_dir.iterdir():
        # Check is file
        if file.is_file():
            # If image
            if file.suffix.lower() in img_ext:
                images.append(file.name)
                known_extensions.add(file.suffix)
                category_dir = argv_path / "images"
            # If video
            elif file.suffix.lower() in vid_ext:
                videos.append(file.name)
                known_extensions.add(file.suffix)
                category_dir = argv_path / "videos"
            # If document
            elif file.suffix.lower() in doc_ext:
                documents.append(file.name)
                known_extensions.add(file.suffix)
                category_dir = argv_path / "documents"
            # If music
            elif file.suffix.lower() in music_ext:
                music.append(file.name)
                known_extensions.add(file.suffix)
                category_dir = argv_path / "music"
            # If archive
            elif file.suffix.lower() in arch_ext:
                archives.append(file.name)
                known_extensions.add(file.suffix)
                category_dir = argv_path / "archives"
                shutil.unpack_archive(file, category_dir/file.stem)
            # If unknown
            else:
                unknown_files.append(file.name)
                unknown_extensions.add(file.suffix)
                category_dir = argv_path / "unknown"

            category_dir.mkdir(exist_ok=True)
            if category_dir.stem == "unknown":
                filename = file.stem  # No normalize if file is unknown
            else:
                # Normalize filename for known file
                filename = normalize(file.stem)
            file_ext = file.suffix
            try:
                # Move file to appropriate folder
                file.rename(category_dir.joinpath(filename+file_ext))
            except FileNotFoundError:
                pass
        # Check is directory
        elif file.is_dir():
            if file in ignore_folders:
                continue
            else:
                sorter(target_dir / file)

    # Delete empty dirs
    for p in Path(target_dir).glob('**/*'):
        if p.is_dir() and len(list(p.iterdir())) == 0:
            os.removedirs(p)

    return


sorter()
print(
    f"Images: {images}\nVideos: {videos}\nDocuments: {documents}\n"
    f"Music: {music}\nArchives: {archives}\nUnknown files: {unknown_files}\n"
    f"Known extensions: {known_extensions}\nUnknown extensions: {unknown_extensions}")
print("\nSorted finished!")
