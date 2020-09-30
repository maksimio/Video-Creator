from json import dump
from copy import copy
from os.path import join
from time import time
from random import random, randint

def make_frame(obj_type, amount_of_obj, fr):
    default = {'type': obj_type, 'size': 1}
    objects = [copy(default) for i in range(amount_of_obj)]
    
    if amount_of_obj == 8:
        length = 3
    elif amount_of_obj == 64:
        length = 7
    elif amount_of_obj == 512:
        length = 15
    elif amount_of_obj == 4096:
        length = 31

    for index in range(0,amount_of_obj,1):
        objects[index]['id'] = obj_type + str(index)
        objects[index]['col'] = [random(), random(), random(), random()]
        objects[index]['rot'] = [random(), random(), random()]

    index = 0
    
    if fr != 0:
        for index in range(0,amount_of_obj,1):
            objects[index]['loc'] = [randint(-10,10), randint(-10,10), randint(-10,50)] # Регулировать перемещение объектов - здесь
            objects[index]['scale'] = [randint(1,2), randint(1,2), randint(1,2)]   
    else:
        for z in range(1,length+1,2):
            for y in range(1,length+1,2):
                for x in range(1,length+1,2):
                    
                    objects[index]['loc'] = [x, y, z] 
                    objects[index]['scale'] = [1, 1, 1]
                    index +=1    
    return objects

def make_anim(amount_of_frames, amount_of_obj, obj_type):
    frames = []
    frame_step = 420 # Частота ключевых кадров
    for fr in range(0,amount_of_frames,frame_step):
        frames.append({'cur_frame': fr, 'obj': make_frame(obj_type, amount_of_obj, fr)})
    return frames

if __name__ == '__main__':
    
    amount_of_frames = 1000 #Количество кадров
    amount_of_objects = 64 #Количество объектов (выбор из 8/64/512/4096)
    object_type = 'cube' #Тип объектов (выбор из "cube" - куб,"sphere" - сфера, "plane" - плоскость)

    dirpath = join('jsonfiles')
    start = time()
    frames = make_anim(amount_of_frames, amount_of_objects, object_type)
    print('Frames ready -->', round(time() - start, 3), 's')
    with open(join(dirpath, 'result.json'), 'w') as fout:
        dump(frames, fout)
    print('Dump ready -->', round(time() - start, 3), 's')