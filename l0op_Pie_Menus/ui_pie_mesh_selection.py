import bpy


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


CLASSES = [LOOP_OT_select_object,
           LOOP_OT_select_vertex,
           LOOP_OT_select_edge,
           LOOP_OT_select_face
           ]


def register():
    for cls in CLASSES:
        try:
            bpy.utils.register_class(cls)
        except:
            print(f"{cls.__name__} already registred")


def unregister():
    for cls in CLASSES:
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
