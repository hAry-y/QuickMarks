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
import json
import webbrowser
import os
from bpy.types import Menu


Delete_Toggle = False

bpy.types.Scene.my_checkbox = bpy.props.BoolProperty(
    name="Delete Toggle",
    description="Enable something",
    default=False
)


def update_checkbox(self, context):
    global Delete_Toggle
    if context.scene.my_checkbox:
        # Switch to Edit Mode if checkbox is ticked
        if Delete_Toggle == False:
            Delete_Toggle = True
    else:
        # Optionally, switch back to Object Mode if unchecked
        if Delete_Toggle == True:
            Delete_Toggle = False




#bookmark adder function

#ADD FILE CHECKER
loc = ''
loc2=''

#ADD KEYWORDS FILE
addons_dir = bpy.utils.user_resource('SCRIPTS', path="addons")
if os.path.isfile(addons_dir+'\Bookmarks.json'):
    print("File exists!")
else:
    if os.path.exists(addons_dir+'\Bookmarks.json') and os.path.getsize(addons_dir+'\Bookmarks.json') > 0:
        with open(addons_dir+'\Bookmarks.json',"w") as f:
            json.dump([], f, indent=4)
            
    else:
        pass


#ADD MODIFIER FILE   
if os.path.isfile(addons_dir+'\Modifiers.json'):
    print("File exists!")
else:
    if os.path.exists(addons_dir+'\Modifiers.json') and os.path.getsize(addons_dir+'\Modifiers.json') > 0:
        with open(addons_dir+"\Modifiers.json", "w") as f:
            json.dump([], f, indent=4)
            
    else:
        pass
        

loc = addons_dir+'\Bookmarks.json'  
loc2 = addons_dir+'\Modifiers.json'  




global_search = ''

gMessage = 'Success'

L = []
modi = []

class H(bpy.types.Panel):
    """ open link"""
    bl_label = "TOOLS"
    bl_idname = "VIEW3D_PT_again_and_again1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Do it'
    link = "http://www.blender.org"
    
    
    def readfile(f):
        list1 = []
        with open(f,'r') as file:
            for line in file:
                list1.append(line)
        
        return list1

    def draw(self, context):
        
        
        
        
        layout = self.layout
        
        
        b = layout.box()
        b.label(text = "Online",icon  = "NONE")
        
        col = layout.column()
        
        
        op = b.operator('wm.url_open', text="blender.org")
        op.url = H.link
        
        
        b.operator("wm.my_popup", text="Google!")
        
        c = layout.box()
        c.label(text="Your Bookmarks",icon  = "BLENDER")
        
        row = layout.row()
        col = layout.column()
        
        row.scale_y = 2
        row.scale_x = 0.5
        
        #c.operator("show.msg")
        
        global loc
        #o = H.readfile(loc)
        #for i in o:
        #    spl = i.split(',')
        #    c.operator("open.link", text=f"{spl[0]}",icon='WORLD').button_id = spl[0]
        
        c.operator("my_popup.bookmark",text= "+Bookmark")
        
        
        
        if os.path.exists(loc) and os.path.getsize(loc) > 0:
            with open(loc,"r") as file:
                    red = json.load(file)

                    if red:
                        
                        for i in red["bookL"]:
                            #if bpy.context.scene.my_checkbox == False:
                            if context.scene.my_checkbox:
                            # Delete mode: create button to trigger ConfirmDelete
                                c.operator("confirm.delete", text=str(i[0]), icon="WORLD").button_id = str(i[0])
                            else:
                            # Normal mode: open link
                                c.operator("open.link", text=str(i[0]), icon="WORLD").button_id = str(i[0])
                            
        c.prop(context.scene, "my_checkbox")
        #c.operator("show.msg", text="Delete TOggle")
        
        
        new = layout.box()
        
        
        if os.path.exists(loc2) and os.path.getsize(loc2) > 0:
            with open(loc2,"r") as file:
                    red = json.load(file)

                    if red:
                        
                        for i in red["modL"]:
                            if context.scene.my_checkbox:
                                new.operator("delete.mod",text =str(i)).button_id = str(i)
                            else:
                                new.operator("modifier.apply",text =str(i)).button_id = str(i)
                        
        
        
        
        
        new.operator("modifier.pack",text = "RECORD MODIFIER PACK")

class OPEN_LINK(bpy.types.Operator):
    """ Opens this bookmark link in your default browser!"""
    bl_idname = "open.link"
    bl_label = "----links----" 
    button_id: bpy.props.StringProperty(name="Button ID") 
    global gMessage
        
    def execute(self, context):
        
        global Delete_Toggle, loc
        
        if bpy.context.scene.my_checkbox == False:
            global loc
            if os.path.exists(loc) and os.path.getsize(loc) > 0:
                with open(loc,"r") as file:
                        red = json.load(file)





            for i in red["bookL"]:
                spl = str(i[0])
                if spl == self.button_id:
                    linkk = i[1]
                    if not linkk.startswith(("http://", "https://")):
                        linkk = "https://" + linkk
                    #webbrowser.get("chromium")
                    webbrowser.open_new_tab(linkk)



                    self.report({'INFO'}, f"{linkk}")
        else:
            #bpy.ops.confirm.delete()
            return {'FINISHED'}
            
                
        
        

        return {'FINISHED'}
        
class MSG(bpy.types.Operator):
    
    global gMessage
    
    bl_idname = "show.msg"
    bl_label = "print_message"
    def execute(self, context):
        self.report({'INFO'}, f"{gMessage}")
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
    
    name: bpy.props.StringProperty(name="type name")
    
    
    #--------Add to external file
    def add_bookmark(B,N,self):
        
        global loc,Delete_Toggle
        
        
        lwist = [B,N]
        bd = {"bookL":[]}
        
        
        
        global loc
        
        if os.path.exists(loc) and os.path.getsize(loc) > 0:
            with open(loc, "r") as f:
                duct = json.load(f)
                duct["bookL"].append(lwist)
            with open(loc,"w") as f2:
                json.dump(duct,f2,indent=4)
                
        else:
            with open(loc, "w") as f:
                bd["bookL"].append(lwist)
                json.dump(bd,f,indent=4)
        
        self.report({'INFO'}, f"Bookmark Saved! {B}")
            
            

    def execute(self, context):
        self.report({'INFO'}, f"You Added- : {self.my_string}, Checked: {self.my_toggle}")
        
        links = self.my_string
        add = self.name
        PopBookmark.add_bookmark(add,links, self)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        
        #webbrowser.open(link)
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "my_string")
        
        layout.prop(self, "name")
        
        layout.prop(self, "my_toggle")
        
        
        
        
class ConfirmDelete(bpy.types.Operator):
    
    button_id: bpy.props.StringProperty(name="Button ID")
    bl_idname = "confirm.delete"
    bl_label = "confirm delete!"
    
    bookname = 'Confirm Delete This Bookmark?'
    
    confirm: bpy.props.BoolProperty(name="Confirm delete this Bookmark")

    def delete_confirm(self):
        
        
        global loc,Delete_Toggle
        if os.path.exists(loc) and os.path.getsize(loc) > 0:
                
                with open(loc, "r") as f:
                    duct = json.load(f)
                    
                for i in duct["bookL"]:
                    spl = str(i[0])
                    ConfirmDelete.bookname = spl[0]
                    if spl == self.button_id:
                        duct["bookL"].remove(i)
                        
                self.report({'INFO'}, f"Deleted Bookmark {i[0]}")
                
                
                
                with open(loc,"w") as f2:
                    json.dump(duct,f2,indent=4)
        #confirm: bpy.props.BoolProperty(name=f"{spl[0]}")
    
    def execute(self, context):
        
        #self.invoke(context)
        self.delete_confirm()
        
        
        return {'FINISHED'}

    def invoke(self, context, event):
        
        #webbrowser.open(link)
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.label(text=f"{ConfirmDelete.bookname}")
        

class DeleteMod(bpy.types.Operator):
    
    button_id: bpy.props.StringProperty(name="Button ID")
    bl_idname = "delete.mod"
    bl_label = "confirm delete modifier!"
    
    bookname = 'Confirm Delete This Modifier group?'
    
    confirm: bpy.props.BoolProperty(name="Confirm delete this Modifier")

    def delete_confirmmod(self):
        
        
        global loc2,Delete_Toggle
        if os.path.exists(loc2) and os.path.getsize(loc2) > 0:
            with open(loc2, "r") as f:
                dict = json.load(f)
                for i in dict['modL']:
                    
                    if str(i) == self.button_id:
                        dict['modL'].remove(i)
                        self.report({'INFO'}, f"Deleted Modifier group {str(i)}")
                        with open(loc2,"w") as f2:
                            json.dump(dict,f2,indent=4)
    
    def execute(self, context):
        
        #self.invoke(context)
        self.delete_confirmmod()
        
        
        return {'FINISHED'}

    def invoke(self, context, event):
        
        #webbrowser.open(link)
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.label(text=f"{ConfirmDelete.bookname}")
        
        

    
class Modifier(bpy.types.Operator):
    bl_idname = "modifier.pack"
    bl_label = "modifier"
    
    global loc2
    def execute(self, context):
        result = ''
        ml = []
        
        global modi, loc2
        obj = bpy.context.active_object
        if obj and obj.modifiers:
            for mod in obj.modifiers:
                
                l1 = []
                
                dic = {"modL":[]}
                result = str(mod).split('"')[1]
                modi.append(result)
                
                
                self.report({'INFO'}, f"{result}")
                
                base_name = result.split(".")[0]
                
                ml.append(base_name)
                
                
                
        if os.path.exists(loc2) and os.path.getsize(loc2) > 0 and ml:
            with open(loc2, "r") as f:
                dict = json.load(f)
                dict["modL"].append(ml)
            with open(loc2,"w") as f2:
                json.dump(dict,f2,indent=4)
                
        else:
            if ml:
                with open(loc2, "w") as f:
                    dict = {"modL":[ml]}
                    json.dump(dict,f,indent=4)

        
            


        return {'FINISHED'}
    
class apply(bpy.types.Operator):
    global modi,loc2
    bl_idname = "modifier.apply"
    bl_label = "modifier"
    button_id: bpy.props.StringProperty(name="Button ID")
    
    
    def execute(self, context):
        modifier_dict = {
    "Subdivision": "SUBSURF",
    "Bevel": "BEVEL",
    "Mirror": "MIRROR",
    "Solidify": "SOLIDIFY",
    "Array": "ARRAY",
    "Boolean": "BOOLEAN",
    "Displace": "DISPLACE",
    "Shrinkwrap": "SHRINKWRAP",
    "SimpleDeform": "SIMPLE_DEFORM",
    "Lattice": "LATTICE",
    "Cast": "CAST",
    "Wave": "WAVE",
    "Build": "BUILD",
    "Decimate": "DECIMATE",
    "EdgeSplit": "EDGE_SPLIT",
    "Skin": "SKIN",
    "Triangulate": "TRIANGULATE",
    "Weld": "WELD",
    "Remesh": "REMESH",
    "Multiresolution": "MULTIRES",
    "Screw": "SCREW",
    "MeshSequenceCache": "MESH_SEQUENCE_CACHE",
    "DataTransfer": "DATA_TRANSFER",
    "NormalEdit": "NORMAL_EDIT",
    "WeightProximity": "WEIGHT_PROXIMITY",
    "VertexWeightEdit": "VERTEX_WEIGHT_EDIT"
}
        
        obj = bpy.context.active_object
        
        if bpy.context.scene.my_checkbox == False:
            if os.path.exists(loc2) and os.path.getsize(loc2) > 0:
                with open(loc2,"r") as file:
                        r = json.load(file)
                if obj:
                    for i in r["modL"]:
                        if str(i) == self.button_id:

                            for j in i:
                                base_name = j.split(".")[0]

                                s = obj.modifiers.new(name=base_name,type = modifier_dict[base_name])

            


        return {'FINISHED'}
    
    
class Delete(bpy.types.Operator):
    global loc2,loc, gMessage, Delete_Toggle
    bl_idname = "delete.data"
    bl_label = "delete buttons"
    button_id: bpy.props.StringProperty(name="Button ID")
    
    
    def execute(self, context):
        gMessage = Delete_Toggle


        return {'FINISHED'}
    
    
# Register both classes
classes = [H,MyPopupOperator,AddBookmark,
PopBookmark,MSG,OPEN_LINK,Modifier,apply,Delete,ConfirmDelete,DeleteMod]

def register():
    bpy.types.Scene.my_checkbox = bpy.props.BoolProperty(
        name="Delete Toggle",
        description="Toggle to enter Delete mod",
        default=False,
        update=update_checkbox
    )
    for cls in classes:
        bpy.utils.register_class(cls)
    #bpy.types.Scene.text_input_props = bpy.props.PointerProperty(type=TextInputProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    if hasattr(bpy.types.Scene, "my_checkbox"):
        del bpy.types.Scene.my_checkbox

if __name__ == "__main__":
    register()
    #unregister()

