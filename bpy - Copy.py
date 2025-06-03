bl_info = {
    "name": "H",
    "author": "Hari",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Properties > Scene > Add Named Cube",
    "description": "you can do Everything here",
    "category": "Custom",
}

import bpy
import webbrowser
import os

#bookmark adder function

#ADD FILE CHECKER
loc = ''

addons_dir = bpy.utils.user_resource('SCRIPTS', path="addons")
if os.path.isfile(addons_dir+'\Bookmarks.txt'):
    print("File exists!")
else:
    print("File does not exist.")
    with open(addons_dir+"\Bookmarks.txt", "w") as f:
        pass

loc = addons_dir+'\Bookmarks.txt'  

L = []

link = "http://www.blender.org"

global_search = ''




class H(bpy.types.Panel):
    bl_label = "TOOLS"
    bl_idname = "VIEW3D_PT_again_and_again1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Do it'
    
    def readfile(f):
        list1 = []
        with open(f,'r') as file:
            for line in file:
                list1.append(line)
        
        return list1

    def draw(self, context):
        
        
        
        
        layout = self.layout
        
        b = layout.box()
        b.label(text = "Online",icon  = "STRIP_COLOR_02")
        
        col = layout.column()
        
        
        op = b.operator('wm.url_open', text="blender.org")
        op.url = link
        
        
        b.operator("wm.my_popup", text="Google!")
        
        c = layout.box()
        c.label(text="Your Bookmarks",icon  = "STRIP_COLOR_01")
        
        row = layout.row()
        col = layout.column()
        
        row.scale_y = 2
        row.scale_x = 0.5
        
        c.operator("show.msg")
        
        global loc
        o = H.readfile(loc)
        
        
        for i in o:
            c.operator("wm.splash", text=f"{i}")
        
        
        c.operator("my_popup.bookmark",text= "+Bookmark")
        
    
        
class MSG(bpy.types.Operator):
    bl_idname = "show.msg"
    bl_label = "----Bookmarks----"
    def execute(self, context):
        self.report({'INFO'}, f"Click button to open website")
        return {'FINISHED'}
        
class MyPopupOperator(bpy.types.Operator):
    bl_idname = "wm.my_popup"
    bl_label = "Make a Google search!"

    my_string: bpy.props.StringProperty(name="Search here")
    my_toggle: bpy.props.BoolProperty(name="nvm")
    
    
        
    
    def execute(self, context):
        global global_search
        self.report({'INFO'}, f"You typed: {self.my_string}, Checked: {self.my_toggle}")
        
        link = "https://www.google.com/search?q="+self.my_string.replace(" ","+")
        webbrowser.open(link)
        
        global_search = self.my_string
        
        return {'FINISHED'}

    def invoke(self, context, event):
        
        #webbrowser.open(link)
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "my_string")
        layout.prop(self, "my_toggle")
        
class Dropdown(bpy.types.Operator):
    bl_idname = "wm.dropdown_example"
    bl_label = "--Bookmarks--"

    # Define the dropdown (enum) property
    my_options: bpy.props.EnumProperty(
        name="Choose Option",
        items=[
            ('OPT_A', "Blender.org", "Description A"),
            ('OPT_B', "Option 2", "Description B"),
            ('OPT_C', "Option 3", "Description C"),
        ],
        default='OPT_A'
    )
    
    def execute(self, context):
        self.report({'INFO'}, f"Selected: {self.my_options}")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "my_options")
        
        
class AddBookmark(bpy.types.Operator):
    bl_idname = "add.bookmark"
    bl_label = "put website"
    
    def execute(self, context):
        self.report({'INFO'}, "OPEN CHROME!")
        print("You can start coding your function here.")
        return {'FINISHED'}
    

class PopBookmark(bpy.types.Operator):
    bl_idname = "my_popup.bookmark"
    bl_label = "type in the link!"

    my_string: bpy.props.StringProperty(name="Type link")
    my_toggle: bpy.props.BoolProperty(name="add")
    
    
    #--------Add to external file
    def add_bookmark(B,self):
        
        cwd = os.getcwd()
        global L 
        
        L.append(B)
        
        
        global loc
    
        with open(loc, "a") as file:
            file.write(str(B))
            file.write('\n')
        
        self.report({'INFO'}, f"Bookmark Saved! {B}")
            
            

    def execute(self, context):
        self.report({'INFO'}, f"You Added- : {self.my_string}, Checked: {self.my_toggle}")
        
        add = self.my_string
        PopBookmark.add_bookmark(add,self)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        
        #webbrowser.open(link)
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "my_string")
        layout.prop(self, "my_toggle")


# Your new operator
#class SEARCH(bpy.types.Operator):
#    bl_idname = "google.search_button"
#    bl_label = "web search"
#
#    def execute(self, context):
#        self.report({'INFO'}, "OPEN CHROME!")
#        print("You can start coding your function here.")
#        return {'FINISHED'}


# Register both classes
classes = [H,MyPopupOperator,Dropdown,AddBookmark,PopBookmark,MSG]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    #bpy.types.Scene.text_input_props = bpy.props.PointerProperty(type=TextInputProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
    #unregister()

