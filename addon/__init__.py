bl_info = {
    "name" : "Video Creator",
    "author" : "Lopatin M., Savin D., Gureeva I., Briushinin A.",  
    "blender" : (2, 90, 1),
    "version" : (2, 0),
    "location" : "View3D",
    "category" : "Animation",
    "description" : "This addon can create 3D animations based on special input data",
    "wiki_url": "https://github.com/maksimio/Video-Creator"
}

import bpy

from .panel     import Main_VC_Panel 
from .operators import Video_Generation_Operator, Scene_Properties
from .operators import Set_Camera_To_View_Operator, On_Off_Camera_View_Operator
from .operators import Render_Animation_Operator

classes = (
    Main_VC_Panel,
    Video_Generation_Operator,
    Set_Camera_To_View_Operator,
    On_Off_Camera_View_Operator,
    Render_Animation_Operator,
    Scene_Properties
)

def register():
    for item in classes:
        bpy.utils.register_class(item)
    bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=Scene_Properties)

def unregister():
    for item in reversed(classes):
        bpy.utils.unregister_class(item)   
    del bpy.types.Scene.custom_props


if __name__ == "__main__":
    register()
