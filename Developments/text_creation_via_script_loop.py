import bpy

cur_frame = 0
bpy.context.scene.frame_set(cur_frame)

#Первый способ:
#bpy.ops.object.text_add()
#ob = bpy.context.object
#ob.data.body = "my text"

#Второй способ:
for object_text in bpy.data.scenes['Video Creator.1'].collection.all_objects[:]:
   
    if (object_text.name != 'Sun') and (object_text.name != 'Camera') and (object_text.name != 'Camera.001'):
        new_font_curve = bpy.data.curves.new(type="FONT",name=object_text.name + '_curve')
        new_font_obj = bpy.data.objects.new(object_text.name + '_obj',new_font_curve)
        new_font_obj.data.body = object_text.name

        new_font_obj.rotation_euler[0] = 1.5708
        
        new_font_obj.location[0] = 0
        new_font_obj.location[0] = 0
        
        #new_font_obj.location[0] = object_text.location[0]
        #new_font_obj.location[1] = object_text.location[1]
        new_font_obj.location[2] = (object_text.dimensions[2]+object_text.dimensions[2]+object_text.dimensions[2])/3

        new_font_obj.data.extrude = 0.04
        new_font_obj.data.bevel_depth = 0.015
        col = bpy.data.collections.get('Video_col.1')
        col.objects.link(new_font_obj)
        
        #bpy.context.collection.objects.link(new_font_obj)

        #new_font_obj.select_set(True)
        #bpy.ops.object.convert(target='MESH') # Возможно, если не переводить текст в объект можно будет
                                       # его изменять в течении анимации!

        #bpy.ops.object.editmode_toggle() #Переключение с объектного режима в режим редактирования и наоборот
        
        new_font_obj.parent = object_text

        #bpy.data.curves['new_font_curve'].keyframe_insert("size", -1, frame = 20)


