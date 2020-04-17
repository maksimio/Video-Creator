import bpy
import json

def interpolation_type(obj, inter_type = 'LINEAR'):
    '''
    Интерполяция (по стандарту - линейная)
    '''
    fc_loc = obj.animation_data.action.fcurves
    for i in range(3):
        fc_loc_i = fc_loc.find('location', index = i)
        for keyframe in fc_loc_i.keyframe_points:
            keyframe.interpolation = inter_type
    fc_mat = bpy.data.materials[obj.name].node_tree.animation_data.action.fcurves
    for i in range(4):
        fc_mat_i = fc_mat[i]
        for keyframe in fc_mat_i.keyframe_points:
            keyframe.interpolation = inter_type
    
    return

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

def add_basic_object(obj, counter, col_name='Video_col.1'):
    '''
    Добавление базового объекта
    '''
    if obj['type'].lower() == 'cube':
        # Добавляем куб
        bpy.ops.mesh.primitive_cube_add(size=obj['size'], enter_editmode=False, location=(0, 0, 0))
        bpy.context.active_object.name = obj['id']+'.'+counter
        ob = bpy.data.objects[obj['id']+'.'+counter]
        ob.data.name = obj['id']+'.'+counter
        for obj in ob.users_collection[:]:
            obj.objects.unlink(ob)
        col = bpy.data.collections.get(col_name)
        col.objects.link(ob)
    elif obj['type'].lower() == 'parallelepiped': # Пока в разработке
        # Добавляем параллелепипед
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(0, 0, 0))
        bpy.context.active_object.name = obj['id']+'.'+counter
        ob = bpy.data.objects[obj['id']+'.'+counter]
        ob.scale= (obj['scale'][0], obj['scale'][1], obj['scale'][2])
        ob.data.name = obj['id']+'.'+counter
        for obj in ob.users_collection[:]:
            obj.objects.unlink(ob)
        col = bpy.data.collections.get(col_name)
        col.objects.link(ob)
    elif obj['type'].lower() == 'sphere':
        # Добавляем сферу
        bpy.ops.mesh.primitive_uv_sphere_add(radius=obj['size'], enter_editmode=False, location=(0, 0, 0))
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
        bpy.ops.mesh.primitive_plane_add(size=obj['size'], enter_editmode=False, location=(0, 0, 0))
        bpy.context.active_object.name = obj['id']+'.'+counter
        ob = bpy.data.objects[obj['id']+'.'+counter]
        ob.data.name = obj['id']+'.'+counter
        for obj in ob.users_collection[:]:
            obj.objects.unlink(ob)
        col = bpy.data.collections.get(col_name)
        col.objects.link(ob)
    return ob

def animated_material(obj, color, cur_frame):
    '''
    Анимация цвета
    '''
    #color.append(1)
    if obj.name in bpy.data.materials:
        if bpy.data.materials[obj.name].node_tree.nodes['Diffuse BSDF'].inputs[0].default_value == color:
            return
        else:
            bpy.data.materials[obj.name].node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = color
            bpy.data.materials[obj.name].node_tree.nodes['Diffuse BSDF'].inputs[0].keyframe_insert("default_value", frame= cur_frame)
    else:
        new_material = bpy.data.materials.new( name= obj.name)
        new_material.use_nodes = True
        new_material.node_tree.nodes.remove(new_material.node_tree.nodes.get('Principled BSDF'))
        material_output = new_material.node_tree.nodes.get('Material Output')
        material_output.location = (400,0)
        diffuse_node = new_material.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
        diffuse_node.location = (200,0)
        diffuse_node.inputs[0].default_value = color
        diffuse_node.inputs[0].keyframe_insert("default_value", frame= cur_frame)
        new_material.node_tree.links.new(diffuse_node.outputs[0], material_output.inputs[0])
        #bpy.context.object.active_material = new_material
        bpy.data.objects[obj.name].data.materials.append(bpy.data.materials[obj.name])

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

def generate_video(input_filepath):
    with open(input_filepath, 'r') as f:
        move = json.load(f)

    # Создание сцены и объекта
    counter = 1
    for i in list(bpy.data.scenes.keys()):
        a = i.split('.')
        if (a[0] == 'videoCreator'):
            counter +=1
    counter = str(counter)
    bpy.context.window.scene = bpy.data.scenes.new(name='videoCreator.'+counter) 
    newCol = bpy.data.collections.new('Video_col.'+counter)
    bpy.context.window.scene.collection.children.link(newCol)
    # ------

    be = [] # Список существующих объектов
    basic_objects = ['cube', 'plane', 'sphere', 'parallelepiped']

    # Расставляем объекты на сцене и прячем
    for time_frame in move:
        for obj in time_frame['objects']:
            if obj['id'] not in be:
                if obj['type'].lower() in basic_objects:
                    ob = add_basic_object(obj, counter, col_name=newCol.name)
                else:
                    ob = add_object(obj['id']+'.'+counter, obj['size']['verts'], obj['size']['faces'],
                                    edges=[], col_name=newCol.name)
                be.append(obj['id'])
                hide_object(ob, 0)
    #-------

    for time_frame in move:
        fr = time_frame['cur_frame']
        be_now = [] # Список существующих объектов в данный момент
        for obj in time_frame['objects']:
            ob = bpy.data.objects[obj['id']+'.'+counter]
            be_now.append(obj['id'])

            uncover_object(ob, fr)
            animated_material(ob, obj['color'], fr)

            ob.location = (obj['location']['x'], obj['location']['y'], obj['location']['z'])
            ob.rotation_euler.x = obj['rotation']['x']
            ob.rotation_euler.y = obj['rotation']['y']
            ob.rotation_euler.z = obj['rotation']['z']
            ob.keyframe_insert(data_path="location", frame=fr, index=-1)
            ob.keyframe_insert("rotation_euler", frame=fr)
            ob.scale = (obj['scale'][0], obj['scale'][1], obj['scale'][2])
            ob.keyframe_insert("scale", frame=fr)
            interpolation_type(ob) # Интерполяция
        
        set_be_now = set(be_now)
        set_be = set(be)
        hide_objects = set_be - set_be_now
        for obj in bpy.context.window.scene.objects:
            name = obj.name.split('.')
            if name[0] in hide_objects:
                hide_object(obj, fr)

    return fr