import bpy,math
from mathutils import Vector
from pathlib import Path
out=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,c,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*c,1);n.inputs['Roughness'].default_value=.38;n.inputs['Metallic'].default_value=metal;return m
navy=mat('Noche',(0.025,.045,.085));wood=mat('Nogal',(.22,.095,.045));gold=mat('Latón',(.8,.52,.12),.6);blue=mat('Cliente A',(.03,.25,.9));red=mat('Encargado B',(.8,.045,.045));skin=mat('Piel',(.58,.32,.18));white=mat('Porcelana',(.9,.88,.8));green=mat('Plantas',(.04,.24,.12));black=mat('Cabello',(.025,.02,.018))
def cube(n,p,s,m,bevel=.05):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.dimensions=s;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if bevel:q=o.modifiers.new('Bordes','BEVEL');q.width=bevel;q.segments=3;o.modifiers.new('Normales','WEIGHTED_NORMAL')
 return o
def sphere(n,p,s,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=p);o=bpy.context.object;o.name=n;o.scale=s;o.data.materials.append(m);bpy.ops.object.shade_smooth();return o
def cyl(n,p,r,d,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=r,depth=d,location=p);o=bpy.context.object;o.name=n;o.data.materials.append(m);q=o.modifiers.new('Borde','BEVEL');q.width=.025;q.segments=3;return o
cube('Piso',(0,0,-.1),(14,14,.2),wood)
cube('Pared', (0,3.3,2.3),(14,.2,4.6),navy)
for x in [-4,-2,0,2,4]:cube('Moldura',(x,3.15,2.3),(.025,.05,4.5),gold)
for x in [-3,3]:
 cube('Panel',(x,3.1,2.4),(1.4,.1,1.8),wood);cube('Cuadro',(x,3.02,2.4),(1.15,.06,1.5),gold)
 for y in [-1,1]:
  cyl('Mesa auxiliar',(x,y,.95),.6,.1,wood);cyl('Base',(x,y,.45),.05,.9,gold)
cyl('Mesa principal',(0,0,1),1.15,.14,wood);cyl('Pie',(0,0,.48),.12,.95,gold);cyl('Base',(0,0,.08),.65,.08,black)
for x in [-.4,.4]:
 cyl('Plato',(x,0,1.09),.25,.035,white);cyl('Vaso',(x,.45,1.17),.09,.2,gold)
cube('Cuenta',(0,-.38,1.09),(.3,.45,.012),white)
for x,m in [(-1.6,blue),(1.6,red)]:
 sphere('Torso',(x,.15,1.27),(.36,.25,.57),m);sphere('Cabeza',(x,.15,2.08),(.25,.23,.3),skin);sphere('Cabello',(x,.18,2.28),(.26,.235,.12),black)
 for a in [-1,1]:
  sphere('Brazo',(x+a*.4,.1,1.32),(.12,.13,.43),m);sphere('Mano',(x+a*.4,.1,.92),(.12,.13,.13),skin)
  cube('Pantalón',(x+a*.17,.16,.5),(.23,.27,.8),black);cube('Zapato',(x+a*.17,-.03,.12),(.25,.45,.16),black)
for x in [-4,4]:
 cyl('Maceta',(x,2,.3),.38,.6,gold)
 for i in range(6):sphere('Hoja',(x+math.sin(i)*.25,2+math.cos(i)*.2,.8+i*.12),(.22,.16,.55),green)
for p,power,size in [((1,-3,6),1500,5),((-4,-1,4),900,4),((1,3,5),1800,3)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(5,-9,6));cam=bpy.context.object;cam.rotation_euler=(Vector((0,.3,1.1))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=6.2
s=bpy.context.scene;s.camera=cam;s.render.engine='CYCLES';s.cycles.samples=20;s.cycles.use_denoising=False;s.render.resolution_x=1080;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.world.color=(.15,.15,.15);s.view_settings.view_transform='AgX';s.render.image_settings.file_format='PNG';s.render.filepath=str(out/'restaurante.png');bpy.ops.wm.save_as_mainfile(filepath=str(out/'restaurante.blend'));bpy.ops.render.render(write_still=True)
