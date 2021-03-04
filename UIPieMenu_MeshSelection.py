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

addon_keymaps = []

def add_hotkey():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if not kc:
        print('Keymap Error')
        return
    # Mesh Mode
    km = kc.keymaps.new(name='Mesh', space_type='EMPTY')
    # here you can chose the keymapping.
    kmi = km.keymap_items.new(
        VIEW3D_OT_PIE_template_call.bl_idname, 'RIGHTMOUSE', 'PRESS', ctrl=False, alt=True, shift=False)
    addon_keymaps.append((km, kmi))


def remove_hotkey():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


class VIEW3D_MT_PIE_template(Menu):
    bl_label = 'S.Menu Navigation'

    def draw(self, context):
        print("test")
        layout = self.layout
        prefs = context.preferences
        inputs = prefs.inputs

        pie = layout.menu_pie()
        #pie.prop(inputs, "view_rotate_method", expand=True)
        pie.operator_enum("mesh.select_mode", "type")
        pie.operator("mesh.extrude_faces_indiv")

class VIEW3D_OT_PIE_template_call(bpy.types.Operator):
    bl_idname = 'l0op.meshselection'
    bl_label = 'l0op: Mesh Selection'
    bl_description = 'Calls pie menu for mesh selection'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_template")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_template)
    bpy.utils.register_class(VIEW3D_OT_PIE_template_call)
    add_hotkey()


def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_PIE_template)
    bpy.utils.unregister_class(VIEW3D_OT_PIE_template_call)
    remove_hotkey()


if __name__ == "__main__":
    register()