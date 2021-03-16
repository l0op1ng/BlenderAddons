# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
'''
Boolean operator (ver. 1.0)
'''
bl_info = {
    "name": "Boolean operations",
    "description": "Performs simple ('destructive') Boolean operation on selected objects",
    "author": "Witold Jaworski",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Object > Boolean",
    "support": "TESTING",
    "category": "Object",
    "warning": "Still in the 'beta' version - use with caution",
    "wiki_url": "",
    "tracker_url": "",
}

DEBUG = 0  # A debug flag - just for the convinience (Set to 0 in the final version)

import bpy
import traceback  # for error handling


def boolean_operation(tool, op, apply=True):
    '''Performs a Boolean operation on the active object
        Arguments:
        @tool (Object): the other object, not affected by this method
        @op (Enum): a Boolean operation: {'UNION', 'INTERSECT', 'DIFFERENCE'}
        @apply (bool): apply results to the mesh (optional)
    '''
    obj = bpy.context.object  # active object
    bpy.ops.object.modifier_add(type='BOOLEAN')  # adds new modifier to obj
    mod = obj.modifiers[-1]  # new modifier always appear at the end of this list
    while obj.modifiers[0] != mod:  # move this modifier to the first position
        bpy.ops.object.modifier_move_up(modifier=mod.name)
    mod.operation = op  # set the operation
    mod.object = tool  # activate rhe modifier
    if apply:  # applies modifier results to the mesh of the active object (obj):
        if obj.users > 1 or obj.data.users > 1:  # obj has to be a single-user datablock
            # make sure, that obj is the only selected object:
            bpy.ops.object.select_all(action='DESELECT')  # deselect all
            obj.select_set(True)  # select obj, only
            bpy.ops.object.make_single_user(type='SELECTED_OBJECTS',
                                            object=True, obdata=True)
        bpy.ops.object.modifier_apply(modifier=mod.name)


# result constants:
INPUT_ERR = 'ERROR_INVALID_CONTEXT'
ERROR = 'ERROR'
WARNING = 'WARNING'
SUCCESS = 'OK'


def main(op, apply_objects=True, cntx=None):
    ''' Performs a Boolean operation on the active object, using the other
        selected objects as the 'tools'
        Arguments:
        @op (Enum): a Boolean operation: {'UNION', 'INTERSECT', 'DIFFERENCE'}
        @apply_objects (bool): apply results of the Boolean operation to the mesh (optional)
        @cntx (bpy.types.Context): overrides current context (optional)
        @returns (list): one or two message parts: [<flag>, Optional_details]
    '''
    try:
        if cntx == None: cntx = bpy.context
        selected = list(cntx.selected_objects)  # creates a static copy
        active = cntx.object  # active object
        if active in selected: selected.remove(active)
        # input validation:
        if active.type != 'MESH':
            return [INPUT_ERR, "target object ('%s') is not a mesh" % active.name]
        if active.library != None or active.data.library != None:
            return [INPUT_ERR, "target object ('%s') is linked from another file" % active.name]
        if not selected: return [INPUT_ERR, "this operation requires at least two objects"]
        # main loop
        skipped = []  # auxiliary list for the skipped object names
        for tool in selected:  # Apply each tool to the active object:
            if tool.type == 'MESH':
                boolean_operation(tool, op, apply_objects)
            else:  # store the name of the skipped object
                skipped.append(tool.name)
        # let's look at the results:
        if not skipped: return [SUCCESS]
        if len(skipped) < len(selected):  # still there are a few procesed objects"
            return [WARNING, "completed, but skipped non-mesh object(s): '%s'" % str.join("', '", skipped)]
        else:  # no object was processed:
            return [INPUT_ERR, "non-mesh object(s) selected: '%s' " % str.join("', '", skipped)]
    except Exception as err:  # Just in case of a run-time error:
        traceback.print_exc()  # print the Python stack details in the console (for you)
        cntx_msg = ""  # format the diagnostic message:
        if 'active' in locals(): cntx_msg += "occured for object(s): '%s'" % active.name
        if 'tool' in locals(): cntx_msg += ", '%s'" % tool.name
        return [ERROR, "%s %s" % (str(err), cntx_msg)]


# ---------- ### Operator -----------
from bpy.props import EnumProperty, BoolProperty


class OBJECT_OT_Boolean(bpy.types.Operator):
    '''Performs a 'destructive' Boolean operation on the active object
       Arguments:
       @op (Enum): Boolean operation, in ['DIFFERENCE', 'UNION', 'INTERSECT']
       @modifier (Bool): add this operation as the object modifier
    '''
    bl_idname = "object.boolean"
    bl_label = "Boolean"
    bl_description = "Perform a Boolean operation on active object"
    bl_options = {'REGISTER', 'UNDO'}  # Set this options, if you want to update
    #                                  parameters of this operator interactively
    #                                  (in the Tool pane)

    op: EnumProperty(items=[('DIFFERENCE', "Difference", "Boolean difference", 'SELECT_SUBTRACT', 1),
                            ('UNION', "Union", "Boolean union", 'SELECT_EXTEND', 2),
                            ('INTERSECT', "Intersection", "Boolean intersection", 'SELECT_INTERSECT', 3),
                            ],
                     name="Operation",
                     description="Boolean operation",
                     default='DIFFERENCE',
                     )  # end EnumProperty
    modifier: BoolProperty(name="Keep as modifier",
                           description="Keep the results as the object modifier",
                           default=False,
                           )  # end BoolProperty

    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT')

    def execute(self, context):
        main(self.op, apply_objects=not self.modifier, cntx=context)
        return {'FINISHED'}

    def invoke(self, context, event):
        result = main(self.op, apply_objects=not self.modifier, cntx=context)
        if result[0] == SUCCESS:
            return {'FINISHED'}
        else:
            self.report(type={result[0]}, message=result[1])
            return {'FINISHED' if result[0] == WARNING else 'CANCELLED'}


# ---------- # Pie Menu (invoked by the hotkey)  -----------
class VIEW3D_MT_Boolean(bpy.types.Menu):
    '''This pie menu shows Boolean operator options.
       Invoked by the hotkey assignet to this add-on
    '''
    bl_idname = "VIEW3D_MT_Boolean"  # Menu identifier has to contain a '_MT_'
    bl_label = "Select operation"  # Central label of the pie menu

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator_enum(OBJECT_OT_Boolean.bl_idname, property="op")


# ---------- # Add-On Preferences -----------
# default values for the keymap_items.new() call (see register_keymap() method, below)
hotkey_defaults = {"idname": 'wm.call_menu_pie',
                   "type": 'D', "value": 'PRESS', "shift": False, "ctrl": False, "alt": False}


class Preferences(bpy.types.AddonPreferences):
    '''This class provides the user pssibility of altering the keyboard shortcut
       assigned to the Boolean pie menu
    '''
    bl_idname = __name__  # do not change this line

    def on_update(self, context):
        unregister_keymap()
        register_keymap()

    shift: BoolProperty(name="Shift", description="Use the [Shift] key",
                        default=hotkey_defaults["shift"], update=on_update)
    ctrl: BoolProperty(name="Ctrl", description="Use the [Ctrl] key",
                       default=hotkey_defaults["ctrl"], update=on_update)
    alt: BoolProperty(name="Alt", description="Use the [Alt] key",
                      default=hotkey_defaults["alt"], update=on_update)
    key: EnumProperty(items=[('NONE', "None", "No hotkey")] +
                            [tuple([chr(i), chr(i), "[%s] key" % chr(i)]) for i in range(65, 91)],
                      name="Keyboard key",
                      description="Selected keyboard key",
                      default=hotkey_defaults["type"],
                      update=on_update
                      )

    def draw(self, context):
        row = self.layout.row(align=True)
        row.alignment = 'LEFT'
        row.separator(factor=10)
        row.prop(self, "key", text="Keyboard shortcut")
        row.separator(factor=3)
        row.label(text="with:")
        row.prop(self, "shift")
        row.prop(self, "ctrl")
        row.prop(self, "alt")

    # ---------- # hotkey registartion


addon_keymaps = []  # global list for this add-on keyboard shortcut definitions


def register_keymap():
    '''Registers current hotkey'''
    # assumption: at this moment the addon_keymaps[] list is empty
    args = hotkey_defaults  # use defaults in case when there is no preferences
    if Preferences.bl_idname in bpy.context.preferences.addons:  # update args, according preferences:
        prf = bpy.context.preferences.addons[Preferences.bl_idname].preferences
        args["type"] = prf.key  # use the user-defined key and its modifiers:
        args["shift"], args["ctrl"], args["alt"] = prf.shift, prf.ctrl, prf.alt
    else:
        prf = None

    if args["type"] == 'NONE': return  # do nothing (no shortcut)
    key_config = bpy.context.window_manager.keyconfigs.addon
    if key_config:
        key_map = key_config.keymaps.new(name="Object Mode")
        hotkey = key_map.keymap_items.new(**args)  # invoked command: args["idname"]
        hotkey.properties.name = VIEW3D_MT_Boolean.bl_idname  # pie menu to open
        addon_keymaps.append((key_map, hotkey))
        if DEBUG: print("Keyboard shortcut set to: " + ("[Shift]-" if args["shift"] else "")
                        + ("[Ctrl]-" if args["ctrl"] else "") + ("[Alt]-" if args["alt"] else "")
                        + ("[%s]" % args["type"]) + (" (from add-on preferences)" if prf else ""))


def unregister_keymap():
    key_config = bpy.context.window_manager.keyconfigs.addon
    if key_config:
        for key_map, hotkey in addon_keymaps:
            key_map.keymap_items.remove(hotkey)
    addon_keymaps.clear()


# ---------- ### Register -----------
from bpy.utils import register_class, unregister_class


def menu_draw(self, context):
    self.layout.operator_context = 'INVOKE_REGION_WIN'
    self.layout.operator_menu_enum(OBJECT_OT_Boolean.bl_idname, property="op")


# list of the classes in this add-on to be registered in Blender API:
classes = [
    OBJECT_OT_Boolean,
    VIEW3D_MT_Boolean,
    Preferences,
]


def register():
    for cls in classes:
        register_class(cls)
    bpy.types.VIEW3D_MT_object.prepend(menu_draw)
    register_keymap()
    if DEBUG: print(__name__ + ": registered")


def unregister():
    unregister_keymap()
    bpy.types.VIEW3D_MT_object.remove(menu_draw)
    for cls in classes:
        unregister_class(cls)
    if DEBUG: print(__name__ + ": UNregistered")


# ---------- ### Main code -----------
if __name__ == '__main__':
    register()
