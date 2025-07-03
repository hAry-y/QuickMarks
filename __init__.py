bl_info = {
    "name": "QuickMarks",
    "author": "Harinarayanan P V",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "3D Viewport > Sidebar > QuickMarks",
    "description": "Quickly save and restore bookmarks of websites in Blender.",
    "category": "3D View",
    "doc_url": "https://github.com/hAry-y/QuickMarks",
    "tracker_url" : "https://github.com/hAry-y/QuickMarks"
}

import bpy
import json
import webbrowser
import os


from datetime import datetime


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

loc = addons_dir+'\Bookmarks.json'  


global_search = ''

gMessage = 'Success'

L = []
modi = []


class H2(bpy.types.Panel):
    """ open link"""
    bl_label = "search"
    bl_idname = "VIEW3D_PT_online"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QuickMarks'
    link = "http://www.blender.org"
    bl_description = "This button does something cool!"
    bl_order = -1
    
    def draw(self, context):
        
        layout = self.layout
        b = layout.box()
        col = b.column()
        row = b.row()
        
        row.operator("wm.my_popup", text="Google!",icon = "COLOR_GREEN")
        
        #op = row.operator('wm.url_open', text="blender.org", icon = "BLENDER", )
        #op.url = H2.link
        
        row.scale_y = 2
        row.scale_x = 2
    
class H3(bpy.types.Panel):
    
    bl_label = "Bookmarks"
    bl_idname = "VIEW3D_PT_bookmarks"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QuickMarks'
    link = "http://www.blender.org"
    bl_description = "This button does something cool!"
    bl_order = 0
    

    def draw(self, context):
        
        layout = self.layout
        
        
        c = layout.box()
        
        
        c.label(text="Your Bookmarks",icon  = "FILE")
        
        global loc

        
        
        row2 = c.row()
        
        row2.operator("my_popup.bookmark",text= "+Bookmark",icon = "ADD")
        
        row2.scale_y = 2
        #c.alert = True
        
        
        
        if os.path.exists(loc) and os.path.getsize(loc) > 0:
            with open(loc,"r") as file:
                    red = json.load(file)

                    if red:
                        
                        for i in red["bookL"]:
                            #if bpy.context.scene.my_checkbox == False:
                            if context.scene.my_checkbox:
                                if i[2]:
                            # Delete mode: create button to trigger ConfirmDelete
                                    c.operator("confirm.delete", text=str(i[0]), icon="FREEZE").button_id = str(i[0])
                                else:
                                    c.operator("confirm.delete", text=str(i[0]), icon="URL").button_id = str(i[0])
                            else:
                                if i[2]:
                                    c.operator("open.link", text=str(i[0]), icon="FREEZE").button_id = str(i[0])
                            # Normal mode: open link
                                else:
                                    c.operator("open.link", text=str(i[0]), icon="URL").button_id = str(i[0])
                            
        
        #c.operator("show.msg", text="Delete TOggle")
        layout.prop(context.scene, "my_checkbox")
        
class support(bpy.types.Panel):
    
    bl_label = "Support creator"
    bl_idname = "VIEW3D_PT_support"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QuickMarks'
    bl_description = "show some love through donations!"
    bl_order = 0
    
    def draw(self, context):
        layout = self.layout
        #layout.label = "support <3"
        c = layout.box()
        c.label(text="Show some love ♡",icon="RIGHTARROW")
        
        row = c.row()
        
        row.operator("open.link", text="Paypal").button_id = "coffee"
        row.operator("open.link", text="Razorpay").button_id = "razor"
        

class OPEN_LINK(bpy.types.Operator):
    
    global Tooltip
    """ Opens this bookmark link in your default browser!"""
    bl_idname = "open.link"
    bl_label = "----links----" 
    button_id: bpy.props.StringProperty(name="Button ID") 
    global gMessage
    bl_description = "Opens this bookmark link in your default browser!"
    
        
    def execute(self, context):
        
        global Delete_Toggle, loc
        if self.button_id == 'coffee':
            webbrowser.open_new_tab('https://buymeacoffee.com/hary.y')
        if self.button_id == 'razor':
            webbrowser.open_new_tab('https://razorpay.me/@hary-y')
        
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
    
    """Opens a google search on your default browser!"""
    
    bl_idname = "wm.my_popup"
    bl_label = "Make a Google search!"

    my_string: bpy.props.StringProperty(name="Search here")
    
    
    
        
    
    def execute(self, context):
        global global_search
        self.report({'INFO'}, f"Searching: {self.my_string}")
        
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
        #layout.prop(self, "my_toggle")
        

        
        
class AddBookmark(bpy.types.Operator):
    bl_idname = "add.bookmark"
    bl_label = "put website"
    
    def execute(self, context):
        self.report({'INFO'}, "OPEN CHROME!")
        return {'FINISHED'}
    

class PopBookmark(bpy.types.Operator):
    """ Add a custom Bookmark with any name and link to open the bookmark!"""

    
    bl_idname = "my_popup.bookmark"
    bl_label = "Add your Bookmark details!"

    my_string: bpy.props.StringProperty(name="Type Link")
    
    name: bpy.props.StringProperty(name="Type Name")
    
    my_toggle: bpy.props.BoolProperty(name="favorite")
    
    
    #--------Add to external file
    def add_bookmark(B,N,Fa,self):
        
        global loc,Delete_Toggle
        
        
        lwist = [B,N,Fa]
        bd = {"bookL":[]}
        
        
        
        global loc
        
        if os.path.exists(loc) and os.path.getsize(loc) > 0:
            if lwist[1] != "":
                if lwist[0] == "":
                    lwist = [N,N,Fa]
                with open(loc, "r") as f:
                    duct = json.load(f)
                    
                    if lwist[2]:
                        duct["bookL"].insert(0,lwist)
                    else:
                        duct["bookL"].append(lwist)
                with open(loc,"w") as f2:
                    json.dump(duct,f2,indent=4)
            else:
                self.report({'INFO'}, "Can't Save a Bookmark without a link!")

        else:
            with open(loc, "w") as f:
                bd["bookL"].append(lwist)
                json.dump(bd,f,indent=4)
        
        if lwist[1] != "":
            self.report({'INFO'}, f"Bookmark Saved! {B}")
            
            

    def execute(self, context):
        self.report({'INFO'}, f"You Added- : {self.my_string}")
        
        links = self.my_string
        add = self.name
        Fa = self.my_toggle
        PopBookmark.add_bookmark(add,links,Fa,self)
        
        self.my_string = ''
        self.name = ''
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
        
        

    
    
class Delete(bpy.types.Operator):
    global loc2,loc, gMessage, Delete_Toggle
    bl_idname = "delete.data"
    bl_label = "delete buttons"
    button_id: bpy.props.StringProperty(name="Button ID")
    
    
    def execute(self, context):
        gMessage = Delete_Toggle
        return {'FINISHED'}
    
    
# Register both classes
classes = [H2,H3,support,MyPopupOperator,AddBookmark,
PopBookmark,MSG,OPEN_LINK,Delete,ConfirmDelete]

def register():
    bpy.types.Scene.my_checkbox = bpy.props.BoolProperty(
        name="Enable Delete Mode",
        description="Enable to delete bookmarks or modifier groups by clicking them.",
        default=False,
        update=update_checkbox
    )
    bpy.types.Scene.my_int_slider = bpy.props.IntProperty(
        name="Minutes",
        default=0,
        min=0,
        max=1440)
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

