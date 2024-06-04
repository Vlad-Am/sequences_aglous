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
        files_in_dirs = sorted(glob.glob(self.path + '/**/*.jpg', recursive=True))
        # directory_path/     the dir
        # **/       every file and dir under my_path
        # *.txt     every file that ends with '.jpg'

        return files_in_dirs

    @staticmethod
    def split_path_name_to_sequence_and_padding(path_name: object) -> tuple[str, str, str]:
        """Разделяем путь до файла на название секвенции и номер элемента секвенции и разделитель"""
        # разделяем путь на атомарные элементы
        parts = os.path.normpath(path_name).split(os.sep)
        # разделяем наименование секвенции и последний элемент секвенции
        name_sequence_with_padding = parts[-1].rsplit('.', 1)[0][::-1]
        name_sequence_reversed, padding_sequence_reversed = re.split(pattern="_|\.| ",
                                                                     string=name_sequence_with_padding,
                                                                     maxsplit=1)
        name_sequence, padding_sequence = padding_sequence_reversed[::-1], name_sequence_reversed[::-1]
        # получаем разделитель между наименованием секвенции и номером кадра
        delimiter = name_sequence_with_padding.lstrip(padding_sequence).rstrip(name_sequence)
        # костыльная проверка, но схема рабочая
        if delimiter == '':
            if name_sequence.find("_"):
                delimiter = '_'
            else:
                delimiter = ' '

        return name_sequence, padding_sequence, delimiter

    def choice_sequence(self) -> dict[str, list[str]]:
        """Функция определяющая к какой секвенции отнести изображение"""
        dict_of_sequence = {}

        for file in self.files:
            # отделяем от пути до файла папку в которой лежат все папки с секвенциями
            new_file = file.strip(self.path)
            # определяем папку в которой лежит секвенция
            head = os.path.split(new_file)[0]
            # если секвенция с именем head уже была, значение словаря по ключу head - существующий список,
            # если секвенции с таким именем не было берем дефолтное значение []
            list_files_sequence = dict_of_sequence.get(head, [])
            # добавляем в список по значению ключа абсолютный путь до файла
            dict_of_sequence[head] = list_files_sequence + [file]
        return dict_of_sequence

    def make_mov_file(self):
        dict_of_sequence = self.choice_sequence()
        for path_name_seq, list_path in dict_of_sequence.items():
            name_sequence, padding_sequence, delimiter = self.split_path_name_to_sequence_and_padding(list_path[0])
            # print((name_sequence, padding_sequence, delimiter))
            os.system(
                f"""ffmpeg -framerate 24 -start_number {int(padding_sequence)} -i '{self.path}\\{path_name_seq}\\
                    {name_sequence}{delimiter}%0{len(padding_sequence)}d.jpg' '{name_sequence}.mov' """)
            # тут с путями уже путаюсь, не понимаю в каком формате передать атрибуту -input файл - с абсолютным путём?
            # или локальным от папки входа? или непосредственно сам файл, а он сам найдет?(((((не найдет)))))

            # os.system( f"""ffmpeg -framerate 24 -start_number {int(padding_sequence)} -i '{name_sequence}{delimiter}
            # %0{len(padding_sequence)}d.jpg' '{name_sequence}.mov' """)

            # os.system(f"""ffmpeg -framerate 24 -start_number {int(padding_sequence)} -i '{path_name_seq}
            # \\{name_sequence}{delimiter}%0{len(padding_sequence)}d.jpg' '{name_sequence}.mov' """)


if __name__ == '__main__':
    load_dotenv()
    FileAlgous(os.environ.get('PATH_TO_IMAGES')).make_mov_file()
# print(FileAlgous(os.environ.get('PATH_TO_IMAGES')).choice_sequence())
