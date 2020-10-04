from json import dump
from copy import copy
from PIL import Image
from os.path import join
from time import time


def read_img(filepath):
    '''Возвращает словарь из объекта доступа
    к пикселям pix, width и height'''
    image = Image.open(filepath)
    width, height = image.size[0], image.size[1]
    pix = image.load()
    return {'pixels': pix, 'width': width, 'height': height}


def make_pix_frame(img_info, k_height):
    '''Возвращает массив пикселей objects - 
    одно изображение для одного кадра'''
    # Создание пустых шаблонов описаний под каждый куб-пиксель
    default = {'type': 'cube'}
    objects = [copy(default) for i in range(img_info['width']*img_info['height'])]

    x_loc, y_loc = 0.5, -0.5
    for y in range(img_info['height']):
        for x in range(img_info['width']):
            index = x + img_info['width'] * y
            r, g, b = img_info['pixels'][x, y][0]/255, img_info['pixels'][x,y][1]/255, img_info['pixels'][x, y][2]/255
            
            objects[index]['id'] = 'Cube' + str(index) # Т.к. размер изобр. не меняется, то пиксели на одних и тех же позициях получат одинаковый id
            objects[index]['col'] = [round(r, 2), round(g, 2), round(b, 2), 1]  # Округление для уменьшения размера json-файла
            objects[index]['loc'] = [x_loc, y_loc, 0]
            objects[index]['scale'] = [1, 1, round((r*r+g*g+b*b) ** (1/2) * k_height, 2)] # Здесь на позиции z можно установить любую другую функцию высоты от яркости пикселей
            objects[index]['rot'] = [0, 0, 0]

            x_loc += 1

        y_loc -= 1
        x_loc = 0.5

    return objects


def make_pix_anim(filepaths, fr_step = 300, k_height=1):
    '''Возвращает массив кадров для аддона.
    fr_step - межкадровое расстояние
    k_height - коэффициент высоты.'''
    # Чтение всех изображений
    images = [read_img(path) for path in filepaths]

    # Проверка на одинаковый размер изображений
    for img_1 in images:
        for img_2 in images:
            if img_1['width'] != img_2['width'] or img_1['height'] != img_2['height']:
                print('Image sizes are different!')
                exit()

    # Создание кадров
    frames = []
    fr_nums = [i*fr_step for i in range(len(images))]
    for img, fr_num in zip(images, fr_nums):
        frames.append({'cur_frame': fr_num, 'obj': make_pix_frame(img, k_height)})

    return frames


# Мы запускаем скрипт, находясь в папке Video-Creator (важно для путей файлов)
if __name__ == '__main__':
    dirpath = join('generators', 'pixels_inputdata') # Путь к изображениям при необходимости можно поправить
    filepaths = [join(dirpath, '1.jpg'),
                join(dirpath, '2.jpg'),
                join(dirpath, '3.jpg'),
                join(dirpath, '4.jpg'),
                join(dirpath, '5.jpg'),
                join(dirpath, '6.jpg'),
                join(dirpath, '7.jpg'),
                join(dirpath, '8.jpg'),
                join(dirpath, '9.jpg'),
                join(dirpath, '10.jpg'),
                join(dirpath, '11.jpg'),
                join(dirpath, '12.jpg'),
                join(dirpath, '13.jpg'),
                join(dirpath, '14.jpg'),
                join(dirpath, '15.jpg')]

    start = time()
    frames = make_pix_anim(filepaths, fr_step=300, k_height=6)
    print('Frames ready -->', round(time() - start, 3), 's')

    # Запись файла в json-формате с помощью стандартных функций:
    with open(join('jsonfiles', 'pixels_result.json'), 'w') as fout:
        dump(frames, fout)
    print('Dump ready -->', round(time() - start, 3), ' s')