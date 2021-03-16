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


def stuff_on_list_ex3a():
    bpy.ops.object.select_all(action='DESELECT')
    for ob in bpy.context.scene.objects:
        if not ob.hide_viewport:
            continue

        if '.00' not in ob.name:
            continue

        ob.select = True
        ob.hide_viewport = False


def stuff_on_list_ex3b():
    for idx in range(600):
        x = idx % 25
        y = idx // 25
        bpy.ops.mesh.primitive_monkey_add(size=0.2, location=(x, y, 1))
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.ops.object.shade_smooth()


def ex5a_mass_rename():
    for name, ob in bpy.data.objects.items():
        if name[:2] == 'R_':
            ob.name = name[2:] + 'R_'
        elif name[2:] == 'L_':
            ob.name = name[2:] + 'L_'


def prefix_to_suffix(name: str, suffix: str):
    """Moves suffix to the end, Like L_cube to cube_L

    Return the new name
    """
    suffix_len = len(suffix)
    return name[suffix_len:] + suffix


def ex5a_mass_rename_b():
    for name, ob in bpy.data.objects.items():
        if name.startswith('R_'):
            ob.name = prefix_to_suffix(name, 'R_')
        elif name.startswith('L_'):
            ob.name = prefix_to_suffix(name, 'L_')


def ex5b_rename_using_dict():
    suffix_translation = {
        '_R': '_L',
        '_L': '_R'
    }

    object_to_rename = {}

    suflen = 2
    for name, ob in bpy.data.objects.items():
        suffix = name[-suflen:]

        if suffix not in suffix_translation:
            continue

        new_suffix = suffix_translation[suffix]
        ob.name = 'temp_' + name
        object_to_rename[ob.name] = name[:-suflen] + new_suffix

        ob.location.x *= -1

    print(object_to_rename)

    for ob in object_to_rename:
        bpy.data.objects[ob].name = object_to_rename[ob]


def ex6a_move_objects_between_collections():
    collection_source = bpy.data.collections['Collection toto']
    collection_destination = bpy.data.collections['DEMO']

    object_to_unlink = []
    for ob in collection_source.objects:
        try:
            collection_destination.objects.link(ob)
        except RuntimeError:
            pass
        object_to_unlink.append(ob)

    for ob in object_to_unlink:
        collection_source.objects.unlink(ob)

def ex7_manipulating_vtx():
    mesh = bpy.context.active_object.data

    if len(mesh.vertices) < 10000:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.subdivide()
        bpy.ops.object.mode_set(mode='OBJECT')

ex7_manipulating_vtx()