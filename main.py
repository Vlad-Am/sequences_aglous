import glob
import os
import time
import re


def scan_directory(directory_path: str) -> list[str]:
    """Cканирует каталог и возвращает список всех объектов .jpg"""

    files_in_dir = glob.glob(directory_path + '/**/*.jpg', recursive=True)
    # directory_path/     the dir
    # **/       every file and dir under my_path
    # *.txt     every file that ends with '.jpg'

    return files_in_dir


files1 = scan_directory("C:/Users/vlad/Desktop/work/Test_algous/source")


# print(files1)


def split_name_sequence_and_padding(path_name: str) -> tuple[str, str]:
    """"""
    # разделяем путь на атомарные элементы
    parts = os.path.normpath(path_name).split(os.sep)
    # разделяем наименование секвенции и последний элемент секвенции
    name_sequence_with_padding = parts[-1].rsplit('.', 1)[0][::-1]
    name_sequence_reversed, padding_sequence_reversed = re.split(pattern="_|\.",
                                                                 string=name_sequence_with_padding,
                                                                 maxsplit=1)
    name_sequence, padding_sequence = padding_sequence_reversed[::-1], name_sequence_reversed[::-1]

    return name_sequence, padding_sequence


a = 'C:/Users/vlad/Desktop/work/Test_algous/source\\flag\\rain_v01\\rain_v01_001080.jpg'
b = "C:/Users/vlad/Desktop/work/Test_algous/source\\fire\\one\\two\\tree\\fire_long\\fire.00007897.jpg"
c = [a, b]
print(choice_sequence(c))
# print(re.split("\.|_|/", b))
