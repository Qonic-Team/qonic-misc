# this file defines the addon that the user uses to control the rotation calculator in the veiwport 
import bpy
from bpy.props import IntProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty
from math import pi
from time import sleep
from mathutils import Matrix
import threading
import os
import pip
# python script to rotate the vector by the input args

class Rot_vec_blend():

    path_rotated = "./rotated.png" # path to where the renders will be saved
    path_init = "./init.png"

    # boolean that determines if the vector will be reset after being rendered
    reset_after = True
    
    def __init__(self, context): # default constructor
        # check to see if opencv-python is installed as it needed for the image processing
        try:
            __import__('opencv-python')
        except ImportError: # if it is not installed, install it
            pip.main(['install', 'opencv-python'])
        global cv2
        import cv2
        
        self.context = context
        # define the vector object in the scene
        self.vector = context.scene.objects["Vector"]
                
    def rot_vec (self, rot_x, rot_y, rot_z):
        # function must be run on a separate thread if the user needs to be able to see the rotation
        print("Rotating the vector by: " + str([rot_x, rot_y, rot_z]) + "...")
        
        # loop to interpolate the rotation so that it plays out in real time
        steps = 50
        time = 3 # time in seconds
        for i in range(steps):
            # rotate the vector by the inputs
            mat_rot_x = Matrix.Rotation(rot_x/steps, 4, 'X')
            mat_rot_y = Matrix.Rotation(rot_y/steps, 4, 'Y')
            mat_rot_z = Matrix.Rotation(rot_z/steps, 4, 'Z')
            
            self.vector.matrix_world = mat_rot_z @ self.vector.matrix_world
            self.vector.matrix_world = mat_rot_y @ self.vector.matrix_world
            self.vector.matrix_world = mat_rot_x @ self.vector.matrix_world
            
            self.vector.rotation_euler = self.vector.matrix_world.to_euler()
            sleep(time/steps)
        
    def reset (self, init_x, init_y, init_z): # function to reset the vector
        print("Resetting vector...")
        self.vector.rotation_euler = (init_x, init_y, init_z)
        
    def capture (self, rot_x, rot_y, rot_z): # function that automatically captures an image of the rotated vector
        # render the initial orientation
        bpy.context.scene.render.filepath = self.path_init
        bpy.ops.render.render(write_still=True, use_viewport=True)
        
        # rotate the vector
        self.rot_vec(rot_x, rot_y, rot_z)
        
        # render the rotated vector
        bpy.context.scene.render.filepath = self.path_rotated
        bpy.ops.render.render(write_still=True, use_viewport=True)
        
        # stack the rendered image with the render of the inital orientation on top
        rotated = cv2.imread(self.path_rotated)
        init = cv2.imread(self.path_init)
        comparison = cv2.vconcat([init, rotated])
        
        # remove temp renders
        os.remove(self.path_rotated) 
        os.remove(self.path_init) 
        
        cv2.imwrite('./rotation.png', comparison)
        
    def operation (self, rot_x, rot_y, rot_z, reset, init_x, init_y, init_z):
        try:
            self.vector.rotation_euler = (init_x, init_y, init_z)
            self.capture(rot_x, rot_y, rot_z)
            
            if reset:
                self.reset(init_x, init_y, init_z)      
        except:
            pass # just end function if an exception happens, as it is likely caused by blender being closed before the thread running this function has fully executed           


bl_info = {
    "name": "Rotation Calculator",
    "category": "Object",
    "blender": (2, 80, 0),
}


class RotationCalculator(bpy.types.Operator):
    bl_idname = "object.rotation_calc"
    bl_label = "Rotate Vector Object By [X, Y, Z]"
    bl_options = {'REGISTER', 'UNDO'}
    
    radians = BoolProperty(name="Radians: ", description="reads angle values in radians if set to True, and degrees if set to False", default=True)
     
    init_orientation_x = FloatProperty(name="Initial Orientation X: ", description="the initial rotation of the vector around the x axis relative to the z axis", default=0, min=-180, max=180)
    init_orientation_y = FloatProperty(name="Initial Orientation Y: ", description="the initial rotation of the vector around the y axis relative to the z axis", default=0, min=-180, max=180)
    init_orientation_z = FloatProperty(name="Initial Orientation Z: ", description="the initial rotation of the vector around the z axis relative to the z axis", default=0, min=-180, max=180)
   
    rot_as_str_list = StringProperty(name="Rotation List [X, Y, Z] as String: ", description="string storing the rotations of the vector as a list of form [X, Y, Z]", default="[0, 0, 0]")
    rot_x = FloatProperty("Rotation of Vector around X Axis: ", description="rotation around x axis", default=0, min=-180, max=180)
    rot_y = FloatProperty("Rotation of Vector around Y Axis: ", description="rotation around y axis", default=0, min=-180, max=180)
    rot_z = FloatProperty("Rotation of Vector around Z Axis: ", description="rotation around z axis", default=0, min=-180, max=180)
   
    reset_after = BoolProperty(name="Reset Vector after Rotation: ", description="reset the orientation of the vector to the initial orientation after the rotation", default=True)
    
    def invoke(self, context, event):
        #Popup a dialog the user can interact with.
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self,context):
        layout = self.layout
        layout.prop(self,"radians")
        layout.separator()
        layout.prop(self,"init_orientation_x")
        layout.separator()
        layout.prop(self,"init_orientation_y")
        layout.separator()
        layout.prop(self,"init_orientation_z")
        layout.separator()
        layout.prop(self,"rot_as_str_list")
        layout.separator()
        layout.prop(self,"rot_x")
        layout.separator()
        layout.prop(self,"rot_y")
        layout.separator()
        layout.prop(self,"rot_z")
        layout.separator()
        layout.prop(self,"reset_after")
        layout.separator()
    
    def execute(self, context): # called when operator is called
        # check to see if rot_as_str_list has been modified
        if (self.rot_as_str_list != '[0, 0, 0]'):
            rots = [float(i) for i in self.rot_as_str_list.replace('[', '').replace(']', '').split(",")]
        else:
            rots = [self.rot_x, self.rot_y, self.rot_z]
            
        inits = [self.init_orientation_x, self.init_orientation_y, self.init_orientation_z]
            
        if (not self.radians):
            rots = [0.0174533*i for i in rots] # convert to degrees
            inits = [0.0174533*i for i in inits]
        
        r = Rot_vec_blend(context)
        t = threading.Thread(target=r.operation, args=(rots[0], rots[1], rots[2], self.reset_after, inits[0], inits[1], inits[2],))
        t.start()
            
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(RotationCalculator.bl_idname)
def register():
    bpy.utils.register_class(RotationCalculator)
    bpy.types.VIEW3D_MT_object.append(menu_func)
def unregister():
    bpy.utils.unregister_class(RotationCalculator)
    
    
if __name__ == "__main__":
    register()