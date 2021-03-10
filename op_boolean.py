import traceback
import bpy
from bpy.utils import register_class, unregister_class

# Header
bl_info = {
    "name": "Boolean operations",
    "author": "l0op1ng",
    "version": (0, 0, 1),
    "blender": (2, 90, 0),
    "location": "Object > Boolean",
    "support": "TESTING",
    "category": "l0op1ng Tools",
    "description": "Simple, 'destructive' Boolean operations on active object",
    "warning": " Still in the 'beta' version - use with caution",
    "wiki_url": "http://www.google.com",
    "tracker_url": "http://www.google.com",
}


def boolean_operation(tool, operation, apply=True):
    """
    Performs a boolean operation on the active object

    :param tool: the other object, not affect by this method and use as a tool to achieve the boolean operation
    :param operation: a boolean operation : {'UNION', 'INTERSECT', 'DIFFERENCE'}
    :param apply: apply results to the mesh (optional)
    """
    obj = bpy.context.object
    bpy.ops.object.modifier_add(type='BOOLEAN')
    mod = obj.modifiers[-1]
    mod.name = "bool_modifier"
    while obj.modifiers[0] != mod:
        bpy.ops.object.modifier_move_up(modifier=mod.name)

    mod.operation = operation
    mod.object = tool

    if apply:
        bpy.ops.object.modifier_apply(modifier=mod.name)

    # Setup objTool display as wireframe
    bpy.data.objects[tool.name].display_type = 'WIRE'


INPUT_ERR = "cannot execute"
ERROR = "run-time error"
WARNING = "warning"
SUCCESS = "completed"


# Main
def main(op, apply_objects=True, custom_context=None):
    """ Performs a Boolean operation on the active object, using the other
    selected objects as the 'tools'
        Arguments:
        @op (Enum): a Boolean operation: {'UNION', 'INTERSECT', 'DIFFERENCE'}
        @apply_objects (bool): apply the results to the mesh (optional)
        @returns (list): one or two message parts: [<flag>, Optional_details]
    """
    try:
        if custom_context is None:
            custom_context = bpy.context

        selected = list(custom_context.selected_objects)
        active = custom_context.object

        if active in selected:
            selected.remove(active)

        if active.type != 'MESH':
            return [INPUT_ERR, f"target object ('{active.name}') is not a mesh"]

        if active.library is not None or active.data.library is not None:
            return [INPUT_ERR, f"target object ('{active.name}') is linked from another file"]

        if not selected:
            return [INPUT_ERR, "this operation requires at least two objects"]

        skipped = []
        for tool in selected:
            if tool.type == 'MESH':
                boolean_operation(tool, op, apply_objects)
            else:
                skipped.append(tool.name)

        if not skipped:
            return [SUCCESS]

        if len(skipped) < len(selected):
            return [WARNING, "completed, but skipped non-mesh object(s): '%s'" % str.join("', '", skipped)]
        else:
            return [INPUT_ERR, "non-mesh object(s) selected: '%s' " % str.join("', '", skipped)]

    except Exception as err:
        traceback.print_exc()

        cntx_msg = ""
        if 'active' in locals():
            cntx_msg += "occurred for object(s): '%s'" % active.name

        if 'tool' in locals():
            cntx_msg += ", '%s'" % tool.name

        return [ERROR, "%s %s" % (str(err), cntx_msg)]


class OBJECT_OT_Boolean(bpy.types.Operator):
    """ Performs a 'destructive' Boolean operation on the active """
    bl_idname = "object.boolean"
    bl_label = "Boolean"
    bl_description = "Performs selected Boolean operation on active object"

    def execute(self, context):
        main('DIFFERENCE', custom_context=context)
        return {'FINISHED'}


def register():
    register_class(OBJECT_OT_Boolean)


def unregister():
    unregister_class(OBJECT_OT_Boolean)


# Main code
if __name__ == '__main__':
    register()

# result = main('DIFFERENCE')
# print(f"bool_operation --> %s" % str.join(": ", result))
