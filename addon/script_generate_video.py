import bpy
import json

def add_object(name, verts, faces, edges=[], col_name='Video_col.1'):
    '''
    Добавление пользовательского объекта
    '''
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get(col_name)
    col.objects.link(obj)
    #bpy.context.view_layer.objects.active = obj
    mesh.from_pydata(verts, edges, faces)
    return obj

def add_basic_object(obj, counter, edges=[], col_name='Video_col.1'):
    '''
    Добавление базового объекта
    '''
    verts_c = [(0.5, 0.5, -0.5),
             (0.5, -0.5, -0.5),
             (-0.5, -0.5, -0.5),
             (-0.5, 0.5, -0.5),
             (0.5, 0.5, 0.5),
             (0.5, -0.5, 0.5),
             (-0.5, -0.5, 0.5),
             (-0.5, 0.5, 0.5)]
    faces_c = [(0, 1, 2, 3),
             (4, 7, 6, 5),
             (0, 4, 5, 1),
             (1, 5, 6, 2),
             (2, 6, 7, 3),
             (4, 0, 3, 7)] 

    verts_p = [(-0.5, -0.5, 0),
                (0.5, -0.5, 0),
                (-0.5, 0.5, 0),
                (0.5, 0.5, 0)]
    faces_p = [(0, 1, 3, 2)]

    if (obj['type'].lower() == 'cube') or (obj['type'].lower() == 'paral'):
        # Добавляем куб или параллелепипед
        #bpy.ops.mesh.primitive_cube_add(size=obj['size'], enter_editmode=False, location=(0, 0, 0))
        ob = add_object(obj['id']+'.'+counter, verts_c, faces_c, edges, col_name)
    
    elif obj['type'].lower() == 'sphere':
        # Добавляем сферу
        bpy.ops.mesh.primitive_uv_sphere_add(radius=obj['scale'][0], enter_editmode=False, location=(0, 0, 0))
        bpy.context.active_object.name = obj['id']+'.'+counter
        bpy.ops.object.shade_smooth()
        ob = bpy.data.objects[obj['id']+'.'+counter]
        ob.data.name = obj['id']+'.'+counter
        for obj in ob.users_collection[:]:
            obj.objects.unlink(ob)
        col = bpy.data.collections.get(col_name)
        col.objects.link(ob)
    elif obj['type'].lower() == 'plane':
        # Добавляем плоскость
        ob = add_object(obj['id']+'.'+counter, verts_p, faces_p, edges, col_name)
    return ob

def animated_material(obj, color, cur_frame):
    '''
    Анимация цвета
    '''
    bpy.context.scene.frame_set(cur_frame) #!!!
    
    if obj.name in bpy.data.materials:
        if bpy.data.materials[obj.name].diffuse_color == color:
            return
        else:
            bpy.data.materials[obj.name].diffuse_color = color
            bpy.data.materials[obj.name].keyframe_insert(data_path='diffuse_color')              
    else:
        new_material = bpy.data.materials.new(name= obj.name)
        new_material.diffuse_color = color
        bpy.data.objects[obj.name].data.materials.append(new_material)
        new_material.keyframe_insert(data_path='diffuse_color')
        
def hide_object(obj, fr):
    '''
    Скрытие объекта
    '''
    obj.hide_viewport = True
    obj.keyframe_insert(data_path="hide_viewport", frame=fr)
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_render", frame=fr)

def uncover_object(obj, fr):
    '''
    Проявление объекта
    '''
    obj.hide_viewport = False
    obj.keyframe_insert(data_path="hide_viewport", frame=fr)
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_render", frame=fr)

def generate_video(input_filepath, use_bezier):
    with open(input_filepath, 'r') as f:
        move = json.load(f)

    # Создание сцены и объекта
    counter = 1
    for i in list(bpy.data.scenes.keys()):
        a = i.split('.')
        if (a[0] == 'Video Creator'):
            counter +=1
    counter = str(counter)
    bpy.context.window.scene = bpy.data.scenes.new(name='Video Creator.'+counter) 
    newCol = bpy.data.collections.new('Video_col.'+counter)
    bpy.context.window.scene.collection.children.link(newCol)
    # ------

    be = [] # Список существующих объектов
    basic_objects = ['cube', 'plane', 'sphere', 'paral']

    # Расставляем объекты на сцене и прячем
    for time_frame in move:
        for obj in time_frame['obj']:
            if obj['id'] not in be:
                if obj['type'].lower() in basic_objects:
                    ob = add_basic_object(obj, counter, edges=[], col_name=newCol.name)
                else:
                    ob = add_object(obj['id']+'.'+counter, obj['size']['verts'], obj['size']['faces'],
                                    edges=[], col_name=newCol.name)
                be.append(obj['id'])
                hide_object(ob, 0)
    #-------

    for time_frame in move:
        fr = time_frame['cur_frame']
        be_now = [] # Список существующих объектов в данный момент
        for obj in time_frame['obj']:
            ob = bpy.data.objects[obj['id']+'.'+counter]
            be_now.append(obj['id'])

            uncover_object(ob, fr)
            animated_material(ob, obj['col'], fr)

            ob.location = (obj['loc'][0], obj['loc'][1], obj['loc'][2])
            ob.rotation_euler.x = obj['rot'][0]
            ob.rotation_euler.y = obj['rot'][1]
            ob.rotation_euler.z = obj['rot'][2]
            scale_x = obj['scale'][0]
            if len(obj['scale']) == 1:
                scale_y = scale_x
                scale_z = scale_x
            elif len(obj['scale']) == 2:
                scale_y = obj['scale'][1]
                scale_z = 0
            else:
                scale_y = obj['scale'][1]
                scale_z = obj['scale'][2]
            ob.scale = (scale_x, scale_y, scale_z)
            

            ob.keyframe_insert(data_path="location", frame=fr, index=-1)
            ob.keyframe_insert("rotation_euler", frame=fr)
            ob.keyframe_insert("scale", frame=fr)

            #/\/\/\/\/\/\ Линейная Интерполяция (у всего кроме цвета!!!) /\/\/\/\/\/\/\/\/\/\/\/\
            fc = ob.animation_data.action.fcurves
            for index in range(2,11):
                fc[index].keyframe_points[-1].interpolation = 'LINEAR'
            #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
            
        set_be_now = set(be_now)
        set_be = set(be)
        hide_objects = set_be - set_be_now
        for obj in bpy.context.window.scene.objects:
            name = obj.name.split('.')
            if name[0] in hide_objects:
                hide_object(obj, fr)

    return fr