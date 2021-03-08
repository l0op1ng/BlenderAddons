import bpy

def mySelector(objName, additive=False):
    # By default, clear other selections
    if not additive:
        bpy.ops.object.select_all(action='DESELECT')

    # Set the 'select' property of the datablock to True
    bpy.data.objects[objName].select_set(True)


def mySelectorAndActivator(objName, modeSet='EDIT'):
    """
    Select and edit one object

    :param objName: objet name of the targeted selected object
    :param modeSet: mode_set setup ('OBJECT','EDIT')
    """
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Cube'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[objName]
    bpy.ops.object.mode_set(mode=modeSet)


print([k.location for k in bpy.context.selected_objects])