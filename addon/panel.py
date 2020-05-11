import bpy


class Main_VC_Panel(bpy.types.Panel):
    bl_idname = "Main_VC_Panel"
    bl_label = "Video Creator"
    bl_category = "Video Creator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        st_rend_sets = context.scene.render
        layout = self.layout

        # -+-+-+-+-+-+-+-+-+-+-+-+ MAIN SETTINGS:
        b_1 = layout.split()
        c_1 = b_1.column()
        c_1.label(text='MAIN SETTINGS:')

        c_1.prop(context.scene.custom_props, 'input_filepath')
        c_1.separator(factor=0.2)
        
        c_1.prop(context.scene.custom_props, 'use_bezier')

        s_r_c11_1 = c_1.row()
        ss_c_src11_1 = s_r_c11_1.row()
        ss_c_src11_1.label(text='Status:')
        not_enable = ss_c_src11_1.split()
        not_enable.prop(context.scene.custom_props,
                        'set_timeline_status', text='')
        not_enable.enabled = False

        ss_c_src11_2 = s_r_c11_1.row()
        ss_c_src11_2.operator(
            'anim.make_video_generation', icon='MODIFIER_ON')
        ss_c_src11_2.scale_x = 2.15

        c_1.separator(factor=0.2)
        c_1.prop(st_rend_sets, 'filepath')

        if context.scene.custom_props.set_timeline_status == 'Set':
            layout.operator('render.start_render', icon='RENDER_ANIMATION')
            layout.separator(factor=0.8)

        # -+-+-+-+-+-+-+-+-+-+-+-+ RENDER SETTINGS:
            b_2 = layout.split()
            c_2_1 = b_2.column()
            c_2_1.separator(factor=1)
            c_2_1.label(text='RENDER SETTINGS:')

            s_r_c21_1 = c_2_1.row()
            ss_c_src211_1 = s_r_c21_1.column()
            ss_c_src211_1.label(text='Resolution:')

            ss_c_src211_2 = s_r_c21_1.column()
            sss_c_sscsrc2112 = ss_c_src211_2.column()
            local_col_left = sss_c_sscsrc2112
            local_col_left.label(text='X')
            local_col_left.label(text='Y')
            local_col_left.scale_x = 0.4

            sss_c_sscsrc2112_2 = s_r_c21_1.column()
            local_col_right = sss_c_sscsrc2112_2
            local_col_right.prop(st_rend_sets, 'resolution_x', text='')
            local_col_right.prop(st_rend_sets, 'resolution_y', text='')
            local_col_right.scale_x = 2.6

            local_row = c_2_1.row()
            local_row.label(text='Side-by-Side video:')
            local_row.prop(st_rend_sets.image_settings.stereo_3d_format,
                           'use_sidebyside_crosseyed')

            layout.separator(factor=0.8)

        # -+-+-+-+-+-+-+-+-+-+-+-+ CAMERA SETTINGS:
            b_3 = layout.split()
            c_3_1 = b_3.column()
            c_3_1.label(text='CAMERA SETTINGS:')

            s_r_c31 = c_3_1.row()
            s_r_c31.operator('camera.set_location_to_view')
            s_r_c31.operator('camera.on_off_camera_view')
            c_3_1.separator(factor=0.5)

            c_3_1.prop(bpy.context.space_data, 'stereo_3d_camera')
            s_r_c31_2 = c_3_1.row()
            s_r_c31_2.label(text='Convergence Plane Distance')
            s_r_c31_2.prop(
                bpy.data.objects[context.scene.custom_props.main_camera_name].data.stereo, 'convergence_distance', text='')

            s_r_c31_3 = c_3_1.row()
            s_r_c31_3.label(text='Interocular Distance')
            s_r_c31_3.prop(
                bpy.data.objects[context.scene.custom_props.main_camera_name].data.stereo, 'interocular_distance', text='')
            layout.separator(factor=0.8)

        # -+-+-+-+-+-+-+-+-+-+-+-+ LIGHT SETTINGS:
            b_4 = layout.split()
            c_4_1 = b_4.column()
            c_4_1.separator(factor=1)
            c_4_1.label(text='LIGHT SETTINGS:')

            s_r_c41_1 = c_4_1.row()
            ss_c_rc41_1 = s_r_c41_1.column()

            ss_c_rc41_1.prop(
                bpy.data.objects[context.scene.custom_props.main_light_name].data, 'use_shadow', text='Shadow')
            ss_c_rc41_1.prop(
                bpy.data.objects[context.scene.custom_props.main_light_name], 'rotation_euler', text='Sun rotation')

            ss_c_rc41_2 = s_r_c41_1.column()
            ss_c_rc41_2.prop(
                bpy.data.objects[context.scene.custom_props.main_light_name].data, 'energy', text='Power light')
            ss_c_rc41_2.prop(
                bpy.data.objects[context.scene.custom_props.main_light_name].data, 'angle')
            ss_c_rc41_2.separator(factor=2.65)
            ss_c_rc41_2.prop(
                context.scene.world.node_tree.nodes['Background'].inputs[0], 'default_value', text='World color')
