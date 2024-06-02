import glob
import os
import re

from dotenv import load_dotenv


class FileAlgous:
    def __init__(self, path):
        self.path = path
        self.files = self.scan_directory()

    def scan_directory(self) -> list[str]:
        """Cканирует директорию и возвращает путь до всех объектов от папки входа список всех объектов .jpg"""

        files_in_dirs = glob.glob(self.path + '/**/*.jpg', recursive=True)
        # directory_path/     the dir
        # **/       every file and dir under my_path
        # *.txt     every file that ends with '.jpg'

        return files_in_dirs





    @staticmethod
    def split_path_name_to_sequence_and_padding(path_name) -> tuple[str, str]:
        """Разделяем путь до файла на название секвенции и номер элемента секвенции"""
        # разделяем путь на атомарные элементы
        parts = os.path.normpath(path_name).split(os.sep)
        # разделяем наименование секвенции и последний элемент секвенции
        name_sequence_with_padding = parts[-1].rsplit('.', 1)[0][::-1]
        name_sequence_reversed, padding_sequence_reversed = re.split(pattern="_|\.| ",
                                                                     string=name_sequence_with_padding,
                                                                     maxsplit=1)
        name_sequence, padding_sequence = padding_sequence_reversed[::-1], name_sequence_reversed[::-1]

        return name_sequence, padding_sequence

    def choice_sequence(self) -> dict[str, list[str]]:
        """Функция определяющая к какой секвенции отнести изображение"""
        dict_of_sequence = {}

        for file in self.files:
            # разделяем путь до файла на название секвенции и номер элемента секвенции
            name_sequence, padding_sequence = self.split_path_name_to_sequence_and_padding(file)
            # добавляем к названию секвенции длину номера кадра
            name_sequence_length = name_sequence + str(len(padding_sequence))
            # если секвенция с именем name_sequence_length уже была, значение по ключу name_sequence - существующий
            # список, если секвенции с таким именем не было берем дефолтное значение []
            list_files_sequence = dict_of_sequence.get(name_sequence_length, [])
            # добавляем в список по значению ключа путь до файла
            dict_of_sequence[name_sequence_length] = list_files_sequence + [name_sequence, padding_sequence]

        for name_seq, list_path in dict_of_sequence.items():
            os.system(
                f"""ffmpeg -framerate 24 -start_number {int(list_path[1])} -i '{name_seq[0:-1]}_%0{len(list_path[1])}d.jpg' {name_seq}.mov""")


if __name__ == '__main__':

    load_dotenv()
    FileAlgous(os.environ.get('PATH_TO_IMAGES')).choice_sequence()

