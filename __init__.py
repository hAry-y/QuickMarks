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
Tooltip = ''

bpy.types.Scene.my_checkbox = bpy.props.BoolProperty(
    name="Delete Toggle",
    description="Enable something",
    default=False
)


def update_checkbox(self, context):
    
    """Enable to delete bookmarks or modifier groups by clicking them."""
    
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
    bl_description = "This button does something cool!"
    
    
    def readfile(f):
        list1 = []
        with open(f,'r') as file:
            for line in file:
                list1.append(line)
        
        return list1

    def draw(self, context):
        
        
        
        
        layout = self.layout
        
        
        b = layout.box()
        
        
        col = b.column()
        row = b.row()
        
        
        op = row.operator('open.link', text="blender.org", icon = "BLENDER", ).button_id = "blender.org"
        
        #,emboss=True, depress=False
        
        
        row.operator("wm.my_popup", text="Google!",icon = "COLOR_GREEN")
        
        features = layout.box()
        
        c = features.box()
        c.label(text="Your Bookmarks",icon  = "FILE")
        
        
        
        row.scale_y = 2
        row.scale_x = 0.5
        
        #c.operator("show.msg")
        
        global loc
        #o = H.readfile(loc)
        #for i in o:
        #    spl = i.split(',')
        #    c.operator("open.link", text=f"{spl[0]}",icon='WORLD').button_id = spl[0]
        
        
        row2 = c.row()
        col2 = c.column()
        row2.operator("my_popup.bookmark",text= "+Bookmark",icon = "ADD")
        row2.scale_x = .2
        row2.scale_y = 2
        #c.alert = True
        
        
        
        if os.path.exists(loc) and os.path.getsize(loc) > 0:
            with open(loc,"r") as file:
                    red = json.load(file)

                    if red:
                        
                        for i in red["bookL"]:
                            #if bpy.context.scene.my_checkbox == False:
                            if context.scene.my_checkbox:
                            # Delete mode: create button to trigger ConfirmDelete
                                c.operator("confirm.delete", text=str(i[0]), icon="URL").button_id = str(i[0])
                            else:
                            # Normal mode: open link
                                c.operator("open.link", text=str(i[0]), icon="URL").button_id = str(i[0])
                            
        
        #c.operator("show.msg", text="Delete TOggle")
        
        
        new = features.box()
        
        #new.alert = True
        #new.active = False
        new.label(text="Your Modifier groups",icon  = "BLENDER")
        
        
        if os.path.exists(loc2) and os.path.getsize(loc2) > 0:
            with open(loc2,"r") as file:
                    red = json.load(file)

                    if red:
                        
                        for i in red["modL"]:
                            label = " + ".join(i)  # Join modifier names with ' + '
                            if context.scene.my_checkbox:
                                new.operator("delete.mod",text =label,icon = "MODIFIER").button_id = str(i)
                            else:
                                new.operator("modifier.apply",text =label,icon = "MODIFIER").button_id = str(i)
                        
        
        
        
        col3 = new.column()
        col3.operator("modifier.pack",text = "RECORD MODIFIERS")
        
        features.prop(context.scene, "my_checkbox")

class OPEN_LINK(bpy.types.Operator):
    """ Opens this bookmark link in your default browser!"""
    bl_idname = "open.link"
    bl_label = "----links----" 
    button_id: bpy.props.StringProperty(name="Button ID") 
    global gMessage
    bl_description = "Opens this bookmark link in your default browser!"
    global Tooltip
        
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
        
        if self.button_id == 'blender.org':
            OPEN_LINK.bl_description = "This takes you to the Blender website!"
            webbrowser.open_new_tab('https://www.blender.org/')
            
                
        
        

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
    bl_label = "Make a Google search222!"

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
    bl_label = "Add your Bookmark details!"

    my_string: bpy.props.StringProperty(name="Type Link")
    my_toggle: bpy.props.BoolProperty(name="add")
    
    name: bpy.props.StringProperty(name="Type Name")
    
    
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
        
        #layout.prop(self, "my_toggle")
        
        
        
        
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
    "Armature": "ARMATURE",
    "Array": "ARRAY",
    "Bevel": "BEVEL",
    "Boolean": "BOOLEAN",
    "Build": "BUILD",
    "Cast": "CAST",
    "Cloth": "CLOTH",
    "Collision": "COLLISION",
    "CorrectiveSmooth": "CORRECTIVE_SMOOTH",
    "Curve": "CURVE",
    "DataTransfer": "DATA_TRANSFER",
    "Decimate": "DECIMATE",
    "Displace": "DISPLACE",
    "DynamicPaint": "DYNAMIC_PAINT",
    "EdgeSplit": "EDGE_SPLIT",
    "Explode": "EXPLODE",
    "Fluid": "FLUID",
    "GeometryNodes": "NODES",
    "Hook": "HOOK",
    "Lattice": "LATTICE",
    "LaplacianDeform": "LAPLACIANDEFORM",
    "LaplacianSmooth": "LAPLACIANSMOOTH",
    "Mask": "MASK",
    "MeshCache": "MESH_CACHE",
    "MeshDeform": "MESH_DEFORM",
    "MeshSequenceCache": "MESH_SEQUENCE_CACHE",
    "MeshToVolume": "MESH_TO_VOLUME",
    "Mirror": "MIRROR",
    "Multiresolution": "MULTIRES",
    "NormalEdit": "NORMAL_EDIT",
    "Ocean": "OCEAN",
    "ParticleInstance": "PARTICLE_INSTANCE",
    "ParticleSystem": "PARTICLE_SYSTEM",
    "Remesh": "REMESH",
    "Screw": "SCREW",
    "Shrinkwrap": "SHRINKWRAP",
    "SimpleDeform": "SIMPLE_DEFORM",
    "Skin": "SKIN",
    "Smooth": "SMOOTH",
    "SoftBody": "SOFT_BODY",
    "Solidify": "SOLIDIFY",
    "Subdivision": "SUBSURF",
    "Surface": "SURFACE",
    "SurfaceDeform": "SURFACE_DEFORM",
    "Triangulate": "TRIANGULATE",
    "UVProject": "UV_PROJECT",
    "UVWarp": "UV_WARP",
    "VertexWeightEdit": "VERTEX_WEIGHT_EDIT",
    "VertexWeightMix": "VERTEX_WEIGHT_MIX",
    "VertexWeightProximity": "WEIGHT_PROXIMITY",
    "VolumeDisplace": "VOLUME_DISPLACE",
    "VolumeToMesh": "VOLUME_TO_MESH",
    "Wave": "WAVE",
    "WeightedNormal": "WEIGHTED_NORMAL",
    "Weld": "WELD",
    "Wireframe": "WIREFRAME"
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
        description="Enable to delete bookmarks or modifier groups by clicking them.",
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

