import bpy
from bpy.types import Menu

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
class ClassObject(bpy.types.Operator):
    bl_idname = "class.object"
    bl_label = "Class Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="EDIT")
        else:
            bpy.ops.object.mode_set(mode="OBJECT")
        return {'FINISHED'}


# Define Class Vertex
class ClassVertex(bpy.types.Operator):
    bl_idname = "class.vertex"
    bl_label = "Class Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        if bpy.ops.mesh.select_mode != "EDGE, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            return {'FINISHED'}


# Define Class Edge
class ClassEdge(bpy.types.Operator):
    bl_idname = "class.edge"
    bl_label = "Class Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        if bpy.ops.mesh.select_mode != "VERT, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            return {'FINISHED'}


# Define Class Face
class ClassFace(bpy.types.Operator):
    bl_idname = "class.face"
    bl_label = "Class Face"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        if bpy.ops.mesh.select_mode != "VERT, EDGE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            return {'FINISHED'}


# Pie menu definition for mesh component selection
class PieMenuSelectionMesh(Menu):
    # tips : never put capital letters in the bl_idname
    bl_idname = 'l0op.selection_mesh'
    bl_label = 'l0op: Mesh Component Selection'

    def draw(self, context):
        pie = self.layout.menu_pie()
        #pie.operator_enum("mesh.select_mode", "type")
        # 4 - LEFT
        pie.operator("class.vertex", text="Vertex", icon='VERTEXSEL')
        # 6 - RIGHT
        pie.operator("class.face", text="Face", icon='FACESEL')
        # 2 - BOTTOM
        pie.operator("class.edge", text="Edge", icon='EDGESEL')


class PieMenuSelectionObject(Menu):
    bl_idname = 'l0op.selection_object'
    bl_label = 'l0op: Object Selection'

    def draw(self, context):
        pie = self.layout.menu_pie()
        obj = context.active_object
        if obj.type == 'MESH':
            pie.operator("class.vertex", text="Vertex", icon='VERTEXSEL')
            # 6 - RIGHT
            pie.operator("class.face", text="Face", icon='FACESEL')
            # 2 - BOTTOM
            pie.operator("class.edge", text="Edge", icon='EDGESEL')


def register():
    bpy.utils.register_class(ClassVertex)
    bpy.utils.register_class(ClassEdge)
    bpy.utils.register_class(ClassFace)

    bpy.utils.register_class(PieMenuSelectionMesh)
    bpy.utils.register_class(PieMenuSelectionObject)
    add_hotkey(idName=PieMenuSelectionMesh.bl_idname, category='Mesh', key='RIGHTMOUSE', altStatus=True)
    add_hotkey(idName=PieMenuSelectionObject.bl_idname, category='Object Mode', key='RIGHTMOUSE', altStatus=True)


def unregister():
    bpy.utils.unregister_class(ClassVertex)
    bpy.utils.unregister_class(ClassEdge)
    bpy.utils.unregister_class(ClassFace)

    bpy.utils.unregister_class(PieMenuSelectionMesh)
    bpy.utils.unregister_class(PieMenuSelectionObject)
    remove_hotkeys()


if __name__ == "__main__":
    register()

    bpy.ops.wm.call_menu_pie(name=PieMenuSelectionMesh.bl_idname)
