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

    km = kc.keymaps.new(name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'RIGHTMOUSE', 'PRESS', ctrl=False, alt=True, shift=False)
    kmi.properties.name = PieMenuMeshSelection.bl_idname
    addon_keymaps.append((km, kmi))


def remove_hotkey():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


# Pie menu definition for mesh component selection
class PieMenuMeshSelection(Menu):
    # tips : never put capital letters in the bl_idname
    bl_idname = 'l0op.mesh_selection'
    bl_label = 'l0op: Mesh Selection(s)'

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator_enum("mesh.select_mode", "type")
        pie.operator("mesh.extrude_faces_indiv")


def register():
    bpy.utils.register_class(PieMenuMeshSelection)
    add_hotkey()


def unregister():
    bpy.utils.unregister_class(PieMenuMeshSelection)
    remove_hotkey()


if __name__ == "__main__":
    register()
