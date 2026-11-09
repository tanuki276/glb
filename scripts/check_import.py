"""Round-trip all GLBs with Blender; verify visible meshes and ground alignment."""
import bpy, math
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
files=sorted((root/'assets').rglob('*.glb'))
for p in files:
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 bpy.ops.import_scene.gltf(filepath=str(p));bpy.context.view_layer.update()
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
 assert meshes,p
 points=[o.matrix_world@Vector(v) for o in meshes for v in o.bound_box]
 assert abs(min(v.z for v in points))<.0001,(p,'not grounded')
 assert all(math.isfinite(c) for v in points for c in v),p
 assert all(len(o.data.polygons)>0 for o in meshes),p
print('IMPORT_PASS',len(files))
