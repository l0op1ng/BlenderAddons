import bpy


def boolean_operation(objTool):
    """
    Performs a boolean operation on the active object

    :param objTool: the other object, not affect by this method and use as a tool to achieve the boolean operation
    """
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bool_modifier = bpy.context.active_object.modifiers[-1]
    bool_modifier.name = "bool_modifier"



