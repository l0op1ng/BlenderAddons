bl_info = {
    "name": "l0op1ng Pie Menus",
    "description": "Pie Menus for blender",
    "author": "l0op1ng",
    "version": (0, 0, 1),
    "blender": (2, 90, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "3D View"}

##################################
# Import des modules
##################################
import bpy
import rna_keymap_ui
from bpy.props import (StringProperty,
                       BoolProperty,
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty,
                       PointerProperty)


if "bpy" in locals():
    import importlib
    reloadable_modules = [
        "ui_pie_mesh_selection",
    ]
    for module in reloadable_modules:
        if module in locals():
            importlib.reload(locals()[module])

from . import ( ui_pie_mesh_selection,
               )


keymaps_items_dict = {"Snapping Pie Menu": ['wm.call_menu_pie', 'LOOP_MT_PIE_selection_object',
                                            '3D View', 'VIEW_3D', 'WINDOW',
                                            'TAB', 'PRESS', False, True, False
                                            ],
                      }


##################################
# Preferences                    #
##################################

class LOOP_PIE_MENUS_MT_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    prefs_tabs: EnumProperty(
        items=(('info', "Info", "INFORMATION"),
               ('keymaps', "Keymaps", "CHANGE KEYMAPS"),
               ('links', "Links", "LINKS")),
        default='info')

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)

        # Info
        if self.prefs_tabs == 'info':
            box = layout.box()
            split = box.split()
            col = split.column()
            col.separator()
            col.label(text="l0op1ng Pie menus :")
            col.label(text="This addon provide non official pie menu closer to maya workflow")
            col.label(text="The addon is still in development")

        # ------Keymap settings
        if self.prefs_tabs == 'keymaps':
            wm = bpy.context.window_manager
            draw_keymap_items(wm, layout)

        # ------URls
        if self.prefs_tabs == 'links':
            box = layout.box()
            box.label(text="Help", icon='HAND')
            box.operator("wm.url_open", text="Google").url = "https://www.google.com"


# -----------------------------------------------------------------------------
#    Keymap
# -----------------------------------------------------------------------------
addon_keymaps = []


def draw_keymap_items(wm, layout):
    kc = wm.keyconfigs.user

    for name, items in keymaps_items_dict.items():
        kmi_name, kmi_value, km_name = items[:3]
        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text=name)
        col.separator()
        km = kc.keymaps[km_name]
        get_hotkey_entry_item(kc, km, kmi_name, kmi_value, col)


def get_hotkey_entry_item(kc, km, kmi_name, kmi_value, col):
    # for menus and pie_menu
    if kmi_value:
        for km_item in km.keymap_items:
            if km_item.idname == kmi_name and km_item.properties.name == kmi_value:
                col.context_pointer_set('keymap', km)
                rna_keymap_ui.draw_kmi([], kc, km, km_item, col, 0)
                return

        col.label(text=f"No hotkey entry found for {kmi_value}")
        col.operator(LOOP_PIE_MENUS_OT_Add_Hotkey.bl_idname, icon='ADD')

    # for operators
    else:
        if km.keymap_items.get(kmi_name):
            col.context_pointer_set('keymap', km)
            rna_keymap_ui.draw_kmi(
                [], kc, km, km.keymap_items[kmi_name], col, 0)
        else:
            col.label(text=f"No hotkey entry found for {kmi_name}")
            col.operator(LOOP_PIE_MENUS_OT_Add_Hotkey.bl_idname, icon='ADD')


class LOOP_PIE_MENUS_OT_Add_Hotkey(bpy.types.Operator):
    ''' Add hotkey entry '''
    bl_idname = "template.add_hotkey"
    bl_label = "Add Hotkeys"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        add_hotkey()

        self.report({'INFO'},
                    "Hotkey added in User Preferences -> Input -> Screen -> Screen (Global)")
        return {'FINISHED'}


def add_hotkey():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    # In background mode, there's no such thing has keyconfigs.user,
    # because headless mode doesn't need key combos.
    # So, to avoid error message in background mode, we need to check if
    # keyconfigs is loaded.
    if not kc:
        return

    for items in keymaps_items_dict.values():
        kmi_name, kmi_value, km_name, space_type, region_type = items[:5]
        eventType, eventValue, ctrl, shift, alt = items[5:]
        km = kc.keymaps.new(name=km_name, space_type=space_type,
                            region_type=region_type)

        kmi = km.keymap_items.new(kmi_name, eventType,
                                  eventValue, ctrl=ctrl, shift=shift,
                                  alt=alt

                                  )
        if kmi_value:
            kmi.properties.name = kmi_value

        kmi.active = True

    addon_keymaps.append((km, kmi))


def remove_hotkey():
    ''' clears all addon level keymap hotkeys stored in addon_keymaps '''

    kmi_values = [item[1] for item in keymaps_items_dict.values() if item]
    kmi_names = [item[0] for item in keymaps_items_dict.values() if item not in ['wm.call_menu', 'wm.call_menu_pie']]

    for km, kmi in addon_keymaps:
        # remove addon keymap for menu and pie menu
        if hasattr(kmi.properties, 'name'):
            if kmi_values:
                if kmi.properties.name in kmi_values:
                    km.keymap_items.remove(kmi)

        # remove addon_keymap for operators
        else:
            if kmi_names:
                if kmi.name in kmi_names:
                    km.keymap_items.remove(kmi)

    addon_keymaps.clear()


##################################
# register                       #
##################################

CLASSES = [LOOP_PIE_MENUS_MT_addon_prefs,
           LOOP_PIE_MENUS_OT_Add_Hotkey]


# Register
def register():
    for cls in CLASSES:
        #ui_pie_mesh_selection.register()

        try:
            bpy.utils.register_class(cls)
        except:
            print(f"{cls.__name__} already registered")

    # hotkey setup
    add_hotkey()


# Unregister
def unregister():
    #ui_pie_mesh_selection.unregister()

    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

    # hotkey cleanup
    remove_hotkey()
