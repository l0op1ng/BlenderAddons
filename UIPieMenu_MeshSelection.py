import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty

bl_info = {
    "name": "L0op Pie Menu for Selection",
    "author": "l0op1ng",
    "version": (0, 0, 0, 1),
    "description": "Adds Pie Menus for quick selection",
    "blender": (2, 90, 0),
    "warning": "WIP",
    "wiki_url": "",
    "category": "l0op1ng Tools"
}

# Store keymaps to remove them later
addon_keymaps = []


def add_hotkey(idName: str, category: str, key: str, ctrlStatus=False, altStatus=False, shiftStatus=False):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if not kc:
        print('Keymap Error')
        return

    km = kc.keymaps.new(name=category, space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_menu_pie', key, 'PRESS', ctrl=ctrlStatus, alt=altStatus, shift=shiftStatus)
    kmi.properties.name = idName
    addon_keymaps.append((km, kmi))


def remove_hotkeys():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


# Define Class Object Mode
class LOOP_OT_select_object(bpy.types.Operator):
    bl_idname = "select.object"
    bl_label = "l0op: Select Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="EDIT")
        else:
            bpy.ops.object.mode_set(mode="OBJECT")
        return {'FINISHED'}


# Define Class Vertex
class LOOP_OT_select_vertex(bpy.types.Operator):
    bl_idname = "loop.select_vertex"
    bl_label = "l0op: Select Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        if bpy.ops.mesh.select_mode != "EDGE, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            return {'FINISHED'}


# Define Class Edge
class LOOP_OT_select_edge(bpy.types.Operator):
    bl_idname = "loop.select_edge"
    bl_label = "l0op: Select Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        if bpy.ops.mesh.select_mode != "VERT, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            return {'FINISHED'}


# Define Class Face
class LOOP_OT_select_face(bpy.types.Operator):
    bl_idname = "loop.select_face"
    bl_label = "Select Face"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        if bpy.ops.mesh.select_mode != "VERT, EDGE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            return {'FINISHED'}


# Pie menu definition for mesh component selection
class LOOP_MT_PIE_selection_mesh(bpy.types.Menu):
    """Pie menu to change selection mode in edit mode for mesh"""
    bl_idname = 'LOOP_MT_PIE_selection_mesh'
    bl_label = 'l0op: Edit Mesh Selection'

    def draw(self, context):
        pie = self.layout.menu_pie()
        # 4 - LEFT
        pie.operator(LOOP_OT_select_vertex.bl_idname, text="Vertex", icon='VERTEXSEL')
        # 6 - RIGHT
        pie.operator(LOOP_OT_select_face.bl_idname, text="Face", icon='FACESEL')
        # 2 - BOTTOM
        pie.operator(LOOP_OT_select_edge.bl_idname, text="Edge", icon='EDGESEL')
        # 8 - TOP
        pie.operator(LOOP_OT_select_object.bl_idname, text="Edit/Object", icon='OBJECT_DATAMODE')


class LOOP_MT_PIE_selection_object(bpy.types.Menu):
    """Pie Menu to select faster in object mode"""
    bl_idname = 'LOOP_MT_PIE_selection_object'
    bl_label = 'l0op: Object Mesh Selection'

    def draw(self, context):
        pie = self.layout.menu_pie()
        obj = context.active_object
        if obj.type == 'MESH':
            # 4 - LEFT
            pie.operator(LOOP_OT_select_vertex.bl_idname, text="Vertex", icon='VERTEXSEL')
            # 6 - RIGHT
            pie.operator(LOOP_OT_select_face.bl_idname, text="Face", icon='FACESEL')
            # 2 - BOTTOM
            pie.operator(LOOP_OT_select_edge.bl_idname, text="Edge", icon='EDGESEL')
            # 8 - TOP
            pie.operator(LOOP_OT_select_object.bl_idname, text="Edit/Object", icon='OBJECT_DATAMODE')


class LOOP_addon_preferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    filepath: bpy.props.StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
    )
    number: bpy.props.IntProperty(
        name="Example Number",
        default=4,
    )
    boolean: bpy.props.BoolProperty(
        name="Example Boolean",
        default=False,
    )

    boolean2: bpy.props.BoolProperty(
        name="Example Boolean2",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "filepath")
        layout.prop(self, "number")
        layout.prop(self, "boolean")
        layout.prop(self, "boolean2")


class LOOP_OT_addon_prefs_example(bpy.types.Operator):
    """Display example preferences"""
    bl_idname = "object.addon_prefs_example"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        info = ("Path: %s, Number: %d, Boolean %r" %
                (addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(LOOP_OT_select_object)
    bpy.utils.register_class(LOOP_OT_select_vertex)
    bpy.utils.register_class(LOOP_OT_select_edge)
    bpy.utils.register_class(LOOP_OT_select_face)

    bpy.utils.register_class(LOOP_MT_PIE_selection_mesh)
    bpy.utils.register_class(LOOP_MT_PIE_selection_object)
    add_hotkey(idName=LOOP_MT_PIE_selection_mesh.bl_idname, category='Mesh', key='RIGHTMOUSE', altStatus=True)
    add_hotkey(idName=LOOP_MT_PIE_selection_object.bl_idname, category='Object Mode', key='RIGHTMOUSE', altStatus=True)

    bpy.utils.register_class(LOOP_OT_addon_prefs_example)
    bpy.utils.register_class(LOOP_addon_preferences)

def unregister():
    bpy.utils.unregister_class(LOOP_OT_select_object)
    bpy.utils.unregister_class(LOOP_OT_select_vertex)
    bpy.utils.unregister_class(LOOP_OT_select_edge)
    bpy.utils.unregister_class(LOOP_OT_select_face)

    bpy.utils.unregister_class(LOOP_MT_PIE_selection_mesh)
    bpy.utils.unregister_class(LOOP_MT_PIE_selection_object)

    bpy.utils.unregister_class(LOOP_OT_addon_prefs_example)
    bpy.utils.unregister_class(LOOP_addon_preferences)

    remove_hotkeys()


if __name__ == "__main__":
    register()

    bpy.ops.wm.call_menu_pie(name=LOOP_MT_PIE_selection_mesh.bl_idname)
