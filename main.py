import glob
import json
import os
import re
import ffmpeg


class FileAlgous:
    def __init__(self, path):
        self.path = path
        self.files = self.scan_directory()

    def scan_directory(self) -> list[str]:
        """Cканирует директорию и возвращает список всех объектов .jpg"""

        files_in_dir = glob.glob(self.path + '/**/*.jpg', recursive=True)
        # directory_path/     the dir
        # **/       every file and dir under my_path
        # *.txt     every file that ends with '.jpg'

        return files_in_dir

    # files1 = scan_directory("C:/Users/vlad/Desktop/work/Test_algous/source")

    # print(files1)

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

    # a = 'C:/Users/vlad/Desktop/work/Test_algous/source\\flag\\rain_v01\\rain_v01_001080.jpg'
    # b = "C:/Users/vlad/Desktop/work/Test_algous/source\\fire\\one\\two\\tree\\fire_long\\fire.00007897.jpg"
    # c = [a, b]
    # print(split_path_name_to_sequence_and_padding(c))

    # print(re.split("\.|_|/", b))

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
            # если имя секвенции уже в словаре, добавляем в список по значению этого словаря путь до файла
            dict_of_sequence[name_sequence_length] = list_files_sequence + [name_sequence, padding_sequence]

        for name_seq, list_path in dict_of_sequence.items():
            with open(f"{name_seq}.txt", 'a') as file:
                file.write(f"file {name_sequence}\n")
        os.system(f"ffmpeg -framerate 24 -start_number 1001 -i 'flag_%04d.jpg' flag_test1.mov")

    def union_jpg_to_video_foo(self):
        """Функция объединяющая jpg в видео"""
        for k, v in self.choice_sequence().items():
            for path in v:
                os.system(f"ffmpeg -framerate 24 - i {k}_%{v} - pix_fmt yuv420p {k}.mp4")


test = FileAlgous("C:/Users/vlad/Desktop/work/Test_algous/source")
test.choice_sequence()
#
# os.system(f"ffmpeg - i flag_%04.jpg output.mp4")
# ffmpeg -framerate 24 -start_number 1001 -i "flag_%04d.jpg" flag_test1.mov