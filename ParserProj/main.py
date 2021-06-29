import pandas as pd
import os
from pathlib import Path

path = os.getcwd()

dirPathIn = path
fileIn = "input.csv"
fileOut_name = "output"


def openFile_byExtension(extension, path_to_file):
    fileIn_data = None
    if extension == "xls" or extension == "xlsx":
        try:
            fileIn_data = pd.read_excel(path_to_file)
        except IOError as e:
            print("При открытии файла произошла ошибка")
            print(e)
        except ValueError as e:
            print("При открытии файла произошла ошибка, возможно несовпадение расширений")
            print(e)
    elif extension == "json":
        try:
            fileIn_data = pd.read_json(path_to_file)
        except IOError as e:
            print("При открытии файла произошла ошибка")
            print(e)
        except ValueError as e:
            print("При открытии файла произошла ошибка, возможно несовпадение расширений")
            print(e)
    else:
        try:
            fileIn_data = pd.read_csv(path_to_file)
        except IOError as e:
            print("При открытии файла произошла ошибка")
            print(e)
        except ValueError as e:
            print("При открытии файла произошла ошибка, возможно несовпадение расширений")
            print(e)

    return fileIn_data


def convertFile_byExtension(inExt, data, outExt, overwrite, outPath):
    if inExt == "json":
        if outExt == "csv":
            if os.path.exists(outPath):     # Файл существует
                if not overwrite:   # Перезапись не разрешена
                    print("Результирующий файл есть, но его нельзя перезаписать")
                    return -500

            print("Файл не существует, запись разрешена")
            fileOut_data = data.to_csv(index=False)
            f = open(outPath, "w")
            f.write(fileOut_data)
            f.close()
            return 0

        elif outExt == "xls" or outExt == "xlsx":
            if os.path.exists(outPath):     # Файл существует
                if not overwrite:   # Перезапись не разрешена
                    print("Результирующий файл есть, но его нельзя перезаписать")
                    return -500

            data.to_excel(excel_writer=outPath, index=False)
            return 0

    else:
        if os.path.exists(outPath): # Файл существует
            if not overwrite:   # Перезапись не разрешена
                print("Результирующий файл есть, но его нельзя перезаписать")
                return -500

        print("Файл не существует, запись разрешена")
        fileOut_data = data.to_json(orient="records")
        f = open(outPath, "w")
        f.write(fileOut_data)
        f.close()
        return 0

    return -1


def convert(path_to_file, result_type, input_type=None, save_to_path=None, overwrite=False) -> int:
    if not Path(fileIn_path).is_file():
        print("Входного файла не существует")
        return -404

    # Определим путь сохранения файла, если не указан, то по дефолту
    fileOut_path = "{0}/{1}.{2}".format(dirPathIn, fileOut_name, result_type)
    if save_to_path is not None:
        fileOut_path = "{0}/{1}.{2}".format(save_to_path, fileOut_name, result_type)

    # Определим расширение файла для корректной конвертации
    if input_type is None:
        name, extension = os.path.splitext(path_to_file)  # Получим расширение файла
        extension = extension.strip(".")
        fileIn_data = openFile_byExtension(extension, path_to_file)  # Открываем файл по полученному расширению
        if fileIn_data is None:  # Если при открытии файла произошла ошибка
            return -1

        # Данные получены, конвертируем в json или csv/xls/xlsx
        convertResult = convertFile_byExtension(inExt=extension, data=fileIn_data, outExt=result_type,
                                                overwrite=overwrite, outPath=fileOut_path)
        if convertResult == -1:  # Если при конвертации произошла ошибка
            return -1
        elif convertResult == -500:
            return -500

    else:
        fileIn_data = openFile_byExtension(input_type, path_to_file)  # Открываетм файл по указонному расширению
        if fileIn_data is None:  # Если при открытии файла произошла ошибка
            return -1

        # Данные получены, конвертируем в json или csv/xls/xlsx
        convertResult = convertFile_byExtension(inExt=input_type, data=fileIn_data, outExt=result_type,
                                                overwrite=overwrite, outPath=fileOut_path)
        if convertResult == -1:  # Если при конвертации произошла ошибка
            return -1
        elif convertResult == -500:
            return -500

    print("Успешно")
    return 0


if __name__ == '__main__':
    fileIn_path = "{0}/{1}".format(dirPathIn, fileIn)

    print(convert(path_to_file=fileIn_path, result_type="json", overwrite=False))
    # print(convert(path_to_file=fileIn_path, result_type="csv", overwrite=True, input_type="json"))
