import bpy
from os import path
from . script_generate_video import generate_video


class Scene_Properties(bpy.types.PropertyGroup):
    # Кастомные свойства для хранения данных
    # Присваиваются каждой сцене (см register()) как custom_props

    input_filepath: bpy.props.StringProperty(
        name="Input file",
        description="Choose the input file in .json format",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
    )

    set_timeline_status: bpy.props.StringProperty(
        name="Status",
        description="This is the status of timeline at current scene",
        default="Not set",
        maxlen=16
    )

    main_camera_name: bpy.props.StringProperty(
        name="Camera",
        description="This is the main camera name",
        maxlen=64
    )

    main_light_name: bpy.props.StringProperty(
        name="Camera",
        description="This is the main camera name",
        maxlen=64
    )

    use_bezier: bpy.props.BoolProperty(
        name="Use Bezier intrepolation",
        description="By default it is linear. True - use Bezier interpolation, which is faster then linear",
        default=False
    )


class Set_Camera_To_View_Operator(bpy.types.Operator):
    bl_idname = "camera.set_location_to_view"
    bl_label = "Camera to view"
    bl_description = "Set the camera position to view. Click from camera view to exit the camera view and end stay in the current camera location"

    def execute(self, context):
        try:  # Вылетит исключение, если нажать кнопку, при уже включенном виде из камеры
            bpy.ops.view3d.camera_to_view()

            # Расчет и изменение расстояния сходимости:
            camera_loc = bpy.context.scene.objects[context.scene.custom_props.main_camera_name].location
            min_dist = float('inf')
            for obj in bpy.context.scene.objects:
                cur_dist = ((camera_loc[0] - obj.location[0]) ** 2 + (camera_loc[1] - obj.location[1]) ** 2 + (camera_loc[2] - obj.location[2]) ** 2) ** (1/2)
                if cur_dist < min_dist and obj.name != context.scene.custom_props.main_camera_name and obj.name != context.scene.custom_props.main_light_name:
                    min_dist = cur_dist
        
            bpy.data.objects[context.scene.custom_props.main_camera_name].data.stereo.convergence_distance = min_dist
            bpy.data.objects[context.scene.custom_props.main_camera_name].data.stereo.interocular_distance = min_dist * 0.03
        except RuntimeError:  # Тогда просто выходим из этого режима
            bpy.ops.view3d.view_camera()

        return {'FINISHED'}


class On_Off_Camera_View_Operator(bpy.types.Operator):
    bl_idname = "camera.on_off_camera_view"
    bl_label = "On/Off camera view"
    bl_description = "Show the camera view or exit the camera view. Remembers the previous position of the viewport"

    def execute(self, context):
        bpy.ops.view3d.view_camera()
        return {'FINISHED'}


class Render_Animation_Operator(bpy.types.Operator):
    bl_idname = "render.start_render"
    bl_label = "Render animation"
    bl_description = "Start render animation. The same as Render->Render_Animation or Ctrl+F12"

    def execute(self, context):
        # Манипуляции с именем файла
        bpy.context.scene.render.use_file_extension = False
        bpy.context.scene.render.views["left"].file_suffix = ""
        bpy.context.scene.render.views["right"].file_suffix = ""
        if bpy.context.scene.render.filepath.endswith(path.sep):
            bpy.context.scene.render.filepath += "videoCreator.mp4"
        if not bpy.context.scene.render.filepath.endswith(".mp4"):
            bpy.context.scene.render.filepath += ".mp4"

        # Сам рендер
        bpy.ops.render.render("INVOKE_DEFAULT", animation=True)
        return {'FINISHED'}


class Video_Generation_Operator(bpy.types.Operator):
    bl_idname = "anim.make_video_generation"
    bl_label = "Set objects on the timeline"
    bl_description = "Make video based on input data file. Use after open file"

    def execute(self, context):
        # Автовыставление путей с предыдущей сцены
        old_input_filepath = bpy.context.scene.custom_props.input_filepath
        old_output_path = context.scene.render.filepath

        # ---ГЕНЕРАЦИЯ ВИДЕО НА ОСНОВЕ ВХОДНЫХ ДАННЫХ---
        if not old_input_filepath.endswith('.json'):
            return {'FINISHED'}
        frame_end = generate_video(
            old_input_filepath, context.scene.custom_props.use_bezier)

        # ---НАСТРОЙКИ ПО УМОЛЧАНИЮ---
        # Кастомные настройки + выходной путь
        context.scene.custom_props.set_timeline_status = "Set"
        context.scene.custom_props.input_filepath = old_input_filepath
        context.scene.render.filepath = old_output_path

        # Настройки рендера и окна предосмотра
        context.scene.render.engine = 'BLENDER_EEVEE'
        context.space_data.shading.type = 'RENDERED'

        # Настройки качества
        context.scene.render.resolution_x = 1920
        context.scene.render.resolution_y = 1080
        context.scene.render.resolution_percentage = 100

        # Настройки кадров
        context.scene.render.fps = 60
        context.scene.render.fps_base = 1
        context.scene.frame_start = 0
        context.scene.frame_step = 1
        context.scene.frame_end = frame_end
        context.scene.frame_current = 0

        # Базовые настройки 3D
        context.scene.render.use_multiview = True  # Stereoscopy
        context.scene.render.image_settings.views_format = 'STEREO_3D'  # Views Format
        context.scene.render.image_settings.stereo_3d_format.display_mode = 'SIDEBYSIDE'  # Stereo Mode
        context.scene.render.image_settings.stereo_3d_format.use_sidebyside_crosseyed = False  # Cross-Eyed

        # Настройки формата выходного файла
        context.scene.render.image_settings.file_format = 'FFMPEG'
        context.scene.render.ffmpeg.format = 'MPEG4'

        # Добавление камеры на сцену
        bpy.ops.object.camera_add(rotation=(1, 0, 1))
        context.scene.custom_props.main_camera_name = bpy.context.object.name
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.view3d.camera_to_view_selected()
        bpy.ops.object.select_all(action='DESELECT')
        context.space_data.stereo_3d_camera = 'RIGHT'

        camera_loc = bpy.context.scene.objects[context.scene.custom_props.main_camera_name].location
        min_dist = float('inf')
        for obj in bpy.context.scene.objects:
            cur_dist = ((camera_loc[0] - obj.location[0]) ** 2 + (camera_loc[1] - obj.location[1]) ** 2 + (camera_loc[2] - obj.location[2]) ** 2) ** (1/2)
            if cur_dist < min_dist and obj.name != context.scene.custom_props.main_camera_name:
                min_dist = cur_dist
        
        bpy.data.objects[context.scene.custom_props.main_camera_name].data.stereo.convergence_distance = min_dist
        bpy.data.objects[context.scene.custom_props.main_camera_name].data.stereo.interocular_distance = min_dist * 0.03


        # Добавление света на сцену
        bpy.ops.object.light_add(type='SUN')
        context.scene.custom_props.main_light_name = bpy.context.object.name
        bpy.data.objects[context.scene.custom_props.main_light_name].rotation_euler = (
            0.279253, 0.139626, 0)
        bpy.data.objects[context.scene.custom_props.main_light_name].data.angle = 0.0349066
        bpy.data.objects[context.scene.custom_props.main_light_name].data.energy = 1
        bpy.data.objects[context.scene.custom_props.main_light_name].data.use_shadow = False

        # Добавление текстуры мира на сцену
        new_world = bpy.data.worlds.new(context.scene.name)
        new_world.use_nodes = True
        context.scene.world = new_world
        context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = (
            0.0196063, 0.0196063, 0.0196063, 1)

        return {'FINISHED'}
