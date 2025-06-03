bl_info = {
    "name": "H",
    "author": "Hari",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Properties > Scene > Add Named Cube",
    "description": "you can do Everything here (Mostly)",
    "category": "Custom",
}

import bpy
import webbrowser
import os

#bookmark adder function
#some changes


L = []

link = "http://www.blender.org"

global_search = ''


class H(bpy.types.Panel):
    """
    Main panel for the H Tools addon.
    
    This panel provides a user interface in the 3D Viewport's N-panel (sidebar)
    that includes various tools and utilities such as:
    - Quick access to blender.org
    - Google search functionality
    - Bookmark management system
    - Dropdown menu for saved bookmarks
    
    The panel is located in the 'Do it' tab of the 3D Viewport sidebar.
    """
    bl_label = "TOOLS"
    bl_idname = "VIEW3D_PT_again_and_again1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Do it'

    def draw(self, context):
        """
        Draw the panel UI elements.
        
        Args:
            context: Blender context object containing scene and UI information
        """
        
        
        
        
        layout = self.layout
        col = layout.column()
        
        
        op = col.operator('wm.url_open', text="blender.org")
        op.url = link
        
        
        layout = self.layout
        layout.operator("wm.my_popup", text="Google!")
        
        
        splash_box = layout.box()
        splash_box.label(text="Splash!",icon  = "INFO")
        splash_box.operator("wm.splash")
        splash_box.label(text="Bookmarks in development, coming soon!!")
        splash_box.operator("google.search_button")
        
        
        row = layout.row()
        col = layout.column()
        row.scale_y = 2
        row.scale_x = 0.5
        row.operator("wm.dropdown_example")
        col.operator("my_popup.bookmark",text= "+Bookmark")
        col.scale_x = -0.5
    
        
        
        
class MyPopupOperator(bpy.types.Operator):
    """
    Popup operator for Google search functionality.
    
    This operator creates a popup dialog that allows users to enter search terms
    and perform Google searches directly from within Blender. The search query
    is processed and opened in the default web browser.
    
    Properties:
        my_string (StringProperty): The search query entered by the user
        my_toggle (BoolProperty): A boolean toggle (currently labeled "nvm")
    """
    bl_idname = "wm.my_popup"
    bl_label = "Make a Google search!"

    my_string: bpy.props.StringProperty(name="Search here")
    my_toggle: bpy.props.BoolProperty(name="nvm")

    def execute(self, context):
        """
        Execute the Google search operation.
        
        Processes the user's search query, formats it for Google search URL,
        and opens it in the default web browser. Also stores the search term
        in a global variable for potential future use.
        
        Args:
            context: Blender context object
            
        Returns:
            dict: {'FINISHED'} to indicate successful completion
        """
        global global_search
        self.report({'INFO'}, f"You typed: {self.my_string}, Checked: {self.my_toggle}")
        
        link = "https://www.google.com/search?q="+self.my_string.replace(" ","+")
        webbrowser.open(link)
        
        global_search = self.my_string
        
        return {'FINISHED'}

    def invoke(self, context, event):
        """
        Invoke the popup dialog.
        
        Args:
            context: Blender context object
            event: The event that triggered this operator
            
        Returns:
            The result of invoking the properties dialog
        """
        
        #webbrowser.open(link)
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        """
        Draw the popup dialog UI.
        
        Creates the user interface elements for the search popup,
        including the search input field and toggle option.
        
        Args:
            context: Blender context object
        """
        layout = self.layout
        layout.prop(self, "my_string")
        layout.prop(self, "my_toggle")
        
class Dropdown(bpy.types.Operator):
    """
    Dropdown menu operator for bookmark selection.
    
    This operator provides a dropdown menu interface for selecting from
    predefined bookmarks. Currently contains hardcoded options but is
    designed to eventually integrate with the bookmark management system.
    
    Properties:
        my_options (EnumProperty): Dropdown selection with predefined bookmark options
    """
    bl_idname = "wm.dropdown_example"
    bl_label = "Bookmarks"

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
        """
        Execute the bookmark selection.
        
        Currently reports the selected option. In future implementations,
        this could open the selected bookmark or perform related actions.
        
        Args:
            context: Blender context object
            
        Returns:
            dict: {'FINISHED'} to indicate successful completion
        """
        self.report({'INFO'}, f"Selected: {self.my_options}")
        return {'FINISHED'}

    def invoke(self, context, event):
        """
        Invoke the dropdown dialog.
        
        Args:
            context: Blender context object
            event: The event that triggered this operator
            
        Returns:
            The result of invoking the properties dialog
        """
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        """
        Draw the dropdown dialog UI.
        
        Creates the user interface for the bookmark dropdown selection.
        
        Args:
            context: Blender context object
        """
        layout = self.layout
        layout.prop(self, "my_options")
        
        
class AddBookmark(bpy.types.Operator):
    """
    Basic bookmark addition operator.
    
    This is a placeholder operator for bookmark functionality.
    Currently only reports a message and prints to console.
    Intended for future development of bookmark management features.
    """
    bl_idname = "add.bookmark"
    bl_label = "put website"
    
    def execute(self, context):
        """
        Execute the bookmark addition operation.
        
        Currently a placeholder that reports a message and prints to console.
        Future implementations should handle actual bookmark addition logic.
        
        Args:
            context: Blender context object
            
        Returns:
            dict: {'FINISHED'} to indicate successful completion
        """
        self.report({'INFO'}, "OPEN CHROME!")
        print("You can start coding your function here.")
        return {'FINISHED'}
    

class PopBookmark(bpy.types.Operator):
    """
    Popup operator for adding bookmarks to external file.
    
    This operator provides a popup dialog for users to input website URLs
    that will be saved as bookmarks to an external text file. The bookmarks
    are stored in the Blender addons directory for persistence.
    
    Properties:
        my_string (StringProperty): The URL/link to be bookmarked
        my_toggle (BoolProperty): Boolean toggle for bookmark addition confirmation
    """
    bl_idname = "my_popup.bookmark"
    bl_label = "type in the link!"

    my_string: bpy.props.StringProperty(name="Type link")
    my_toggle: bpy.props.BoolProperty(name="add")
    
    
    #--------Add to external file
    def add_bookmark(B,self):
        """
        Add a bookmark to external file storage.
        
        Saves the provided bookmark URL to a text file located in the
        Blender addons directory. Also adds the bookmark to a global list
        for runtime access.
        
        Args:
            B: The bookmark URL/link to be saved
            self: Reference to the operator instance for reporting
        """
        
        cwd = os.getcwd()
        global L 
        
        L.append(B)
        addons_dir = bpy.utils.user_resource('SCRIPTS', path="addons")
        
        DATA_PATH = addons_dir+'\Bookmarks.txt'

    
        with open(DATA_PATH, "w") as file:
            file.write(str(B))
            file.write('\n')
        
        self.report({'INFO'}, f"Bookmark Saved! {B}")
            
            

    def execute(self, context):
        """
        Execute the bookmark addition process.
        
        Takes the user input from the popup dialog and processes it
        through the bookmark addition system.
        
        Args:
            context: Blender context object
            
        Returns:
            dict: {'FINISHED'} to indicate successful completion
        """
        self.report({'INFO'}, f"You Added- : {self.my_string}, Checked: {self.my_toggle}")
        
        add = self.my_string
        PopBookmark.add_bookmark(add,self)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        """
        Invoke the bookmark addition popup dialog.
        
        Args:
            context: Blender context object
            event: The event that triggered this operator
            
        Returns:
            The result of invoking the properties dialog
        """
        
        #webbrowser.open(link)
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        """
        Draw the bookmark addition popup UI.
        
        Creates the user interface elements for the bookmark addition dialog,
        including URL input field and confirmation toggle.
        
        Args:
            context: Blender context object
        """
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
classes = [H,MyPopupOperator,Dropdown,AddBookmark,PopBookmark]

def register():
    """
    Register all addon classes with Blender.
    
    This function is called when the addon is enabled and registers
    all the operator and panel classes with Blender's class system.
    """
    for cls in classes:
        bpy.utils.register_class(cls)
    #bpy.types.Scene.text_input_props = bpy.props.PointerProperty(type=TextInputProperties)

def unregister():
    """
    Unregister all addon classes from Blender.
    
    This function is called when the addon is disabled and removes
    all the registered classes from Blender's class system.
    The classes are unregistered in reverse order to avoid dependency issues.
    """
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
    #unregister()
