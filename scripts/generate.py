"""Deterministic original low-poly props. Blender 4.3+: blender -b -t 2 --python scripts/generate.py -- nature"""
import bpy, math, random, json, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
PALETTE={'wood':'916344','bark':'654632','leaf':'438653','lightleaf':'75a857','darkleaf':'275d47','pink':'e994b0','stone':'909b9e','concrete':'bbc2bf','metal':'435763','black':'27323c','white':'f4ead6','red':'cb514b','orange':'e99c46','yellow':'efce68','blue':'4d8ea8','glass':'98ced3','soil':'564736','terracotta':'b8684a','fabric':'6a9b94'}
M={}
for k,h in PALETTE.items():
 m=bpy.data.materials.new(k); c=tuple(int(h[i:i+2],16)/255 for i in (0,2,4)); m.diffuse_color=(*c,1); m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*c,1); p.inputs['Roughness'].default_value=.78
 if k=='metal': p.inputs['Metallic'].default_value=.55
 M[k]=m

def finish(o,name,mat):
 o.name=name;o.data.materials.append(M[mat]);return o

def box(p,s,mat='wood',rot=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.scale=s;o.rotation_euler.z=rot; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,'block',mat)
def cyl(p,r,d,mat='metal',n=12,r2=None):
 bpy.ops.mesh.primitive_cone_add(vertices=n,radius1=r,radius2=r if r2 is None else r2,depth=d,location=p);return finish(bpy.context.object,'cylinder',mat)
def ball(p,s,mat='leaf',sub=1):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=p);o=bpy.context.object;o.scale=s;return finish(o,'faceted',mat)
def beam(a,b,r=.04,mat='metal'):
 a,b=Vector(a),Vector(b);o=cyl((a+b)/2,r,(b-a).length,mat);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def ring(p,r,t=.04,mat='metal',rot=None):
 bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=t,major_segments=20,minor_segments=6,location=p);o=finish(bpy.context.object,'ring',mat)
 if rot:o.rotation_euler=rot
 return o
def legs(w,d,h,mat='wood',r=.045):
 for x in [-w/2,w/2]:
  for y in [-d/2,d/2]:cyl((x,y,h/2),r,h,mat)
def slats(w,d,z,count=6):
 for i in range(count):box((0,-d/2+(i+.5)*d/count,z),(w,d/count*.84,.09))
def text(t,p,size=.3,mat='white'):
 bpy.ops.object.text_add(location=p,rotation=(math.pi/2,0,0));o=bpy.context.object;o.data.body=t;o.data.align_x='CENTER';o.data.align_y='CENTER';o.data.size=size;o.data.extrude=.002;o.data.materials.append(M[mat]);bpy.ops.object.convert(target='MESH')
def pot(p=(0,0,0),r=.3,h=.5):
 x,y,z=p;cyl((x,y,z+h/2),r*.75,h,'terracotta',r2=r);ring((x,y,z+h*.94),r,.035,'terracotta');cyl((x,y,z+h),r*.9,.02,'soil')

def nature(name):
 random.seed(name)
 if name in ['oak','birch','maple','cherry','apple_tree','dead_tree']:
  h=3.4 if name=='birch' else 2.7; bark='white' if name=='birch' else 'bark';cyl((0,0,h/2),.19,h,bark,r2=.09)
  for i in range(7):
   a=i*2.4; end=(math.cos(a)*.9,math.sin(a)*.9,h-.6+(i%3)*.36);beam((0,0,h*.56),end,.065,bark)
   if name!='dead_tree':ball(end,(.9,.82,.88),{'cherry':'pink','maple':'orange'}.get(name,'leaf' if i%2 else 'lightleaf'),2)
   if name=='apple_tree':ball((end[0],end[1]-.65,end[2]-.18),(.1,)*3,'red',2)
  if name=='birch':
   for i in range(8):box((0,-.165,.3+i*.34),(.13,.025,.045),'black')
 elif name in ['pine','fir','cypress']:
  cyl((0,0,1.5),.15,3,'bark',r2=.07)
  if name=='cypress':ball((0,0,2),(.65,.65,1.8),'darkleaf',2)
  else:
   for i in range(4):cyl((0,0,1.15+i*.62),1.1-i*.21,1.45,'darkleaf' if i%2 else 'leaf',9,r2=0)
 elif name=='palm':
  for i in range(8):cyl((i*.025,0,.2+i*.39),.19-i*.01,.42,'bark',r2=.17-i*.01)
  for i in range(9):
   a=i*math.tau/9;end=(math.cos(a)*1.5,math.sin(a)*1.5,2.8);beam((.2,0,3.2),end,.04,'leaf');o=ball((end[0]*.65,end[1]*.65,3.1),(.85,.19,.1),'leaf');o.rotation_euler.z=a
 elif name in ['bush','flower_bush','hedge','topiary']:
  if name=='hedge':box((0,0,.65),(2,.65,1.3),'leaf');return
  if name=='topiary':pot();cyl((0,0,.85),.06,.8,'bark');ball((0,0,1.5),(.55,)*3,'leaf',2);return
  for i in range(7):
   a=i*2.4;p=(math.cos(a)*.32,math.sin(a)*.32,.45+(i%2)*.2);ball(p,(.5,.45,.5),'leaf' if i%2 else 'lightleaf',2)
   if name=='flower_bush':ball((p[0],p[1]-.34,p[2]+.2),(.09,)*3,'pink',1)
 elif name in ['boulder','rock_cluster','pebbles']:
  for i in range({'boulder':1,'rock_cluster':5,'pebbles':9}[name]):
   r=.8 if name=='boulder' else random.uniform(.12,.45);ball((random.uniform(-.6,.6),random.uniform(-.4,.4),r*.55),(r,r*.8,r*.7),'stone',2)
 elif name=='stump':
  cyl((0,0,.3),.4,.6,'bark',10,r2=.32);cyl((0,0,.605),.29,.018,'wood');
  for i in range(5):a=i*math.tau/5;beam((0,0,.25),(math.cos(a)*.55,math.sin(a)*.55,.06),.12,'bark')
 elif name=='log':
  beam((-1,0,.22),(1,0,.22),.22,'bark');beam((1.005,0,.22),(1.02,0,.22),.19,'wood');beam((-.3,0,.3),(-.3,.4,.6),.07,'bark')
 elif name=='flower_patch':
  for i in range(12):
   x,y=random.uniform(-.6,.6),random.uniform(-.4,.4);h=random.uniform(.25,.55);beam((x,y,0),(x,y,h),.015,'leaf');ball((x,y,h),(.06,)*3,'yellow')
   for j in range(5):a=j*math.tau/5;ball((x+.075*math.cos(a),y+.075*math.sin(a),h),(.07,.06,.035),'pink' if i%2 else 'white')
 elif name=='grass_clump':
  for i in range(18):
   x,y=random.uniform(-.3,.3),random.uniform(-.3,.3);beam((x,y,0),(x*1.5,y*1.5,random.uniform(.2,.6)),.018,'lightleaf')

NATURE=['oak','birch','maple','cherry','apple_tree','dead_tree','pine','fir','cypress','palm','bush','flower_bush','hedge','topiary','boulder','rock_cluster','pebbles','stump','log','flower_patch','grass_clump']

def infrastructure(name):
 if 'bridge' in name:
  stone=name=='stone_bridge';length=6;w=2;mat='stone' if stone else 'wood'
  for i in range(25):
   x=-3+(i+.5)*6/25; z=.35+(.7*(1-(x/3)**2) if name in ['arched_bridge','stone_bridge'] else 0);box((x,0,z),(.235,w,.16),mat)
   if i%4==0:
    for y in [-1,1]:box((x,y,z+.48),(.12,.12,1),mat)
   if i:
    px=x-.24;pz=.35+(.7*(1-(px/3)**2) if name in ['arched_bridge','stone_bridge'] else 0)
    for y in [-1,1]:beam((px,y,pz+1),(x,y,z+1),.065,mat)
  for x in [-2.5,2.5]:
   for y in [-.7,.7]:box((x,y,.16),(.3,.3,.32),'stone')
  if name=='truss_bridge':
   for y in [-1,1]:
    beam((-3,y,2),(3,y,2),.08,'metal')
    for i in range(6):beam((-3+i,y,.4),(-2+i,y,2),.06,'metal');beam((-3+i,y,2),(-2+i,y,.4),.06,'metal')
  if name=='rope_bridge':
   for y in [-1,1]:
    for i in range(24):
     x=-3+i*.25;beam((x,y,1.4+.5*(x/3)**2),(x+.25,y,1.4+.5*((x+.25)/3)**2),.035,'bark')
 elif name in ['picket_fence','rail_fence','metal_fence']:
  for x in [-1.4,1.4]:box((x,0,.7),(.13,.13,1.4),'metal' if name=='metal_fence' else 'wood')
  for z in [.4,.95]:box((0,0,z),(3,.1,.09),'metal' if name=='metal_fence' else 'wood')
  if name!='rail_fence':
   for i in range(11):
    x=-1.3+i*.26;box((x,-.06,.65),(.1,.08,1.3),'white' if name=='picket_fence' else 'metal')
    if name=='picket_fence':cyl((x,-.06,1.34),.07,.12,'white',4,r2=0)
 elif name in ['brick_wall','stone_wall']:
  for row in range(5):
   for col in range(7):box((-1.5+col*.45+(row%2)*.2,0,.12+row*.24),(.43,.3,.22),'terracotta' if name=='brick_wall' else 'stone')
 elif name=='gate':
  for x in [-1.3,1.3]:box((x,0,.85),(.18,.18,1.7),'stone')
  for z in [.25,1.3]:box((0,0,z),(2.4,.08,.08),'metal')
  for i in range(11):box((-1.1+i*.22,0,.8),(.035,.05,1.2),'metal')
 elif name in ['stairs','ramp']:
  if name=='stairs':
   for i in range(6):box((0,i*.3,(i+1)*.1),(1.6,.3,(i+1)*.2),'concrete')
  else:
   o=box((0,0,.45),(1.6,3,.13),'concrete');o.rotation_euler.x=math.radians(15)
 elif name=='wooden_dock':
  slats(2,4,.65,18)
  for x in [-.85,.85]:
   for y in [-1.7,0,1.7]:cyl((x,y,.45),.1,.9,'wood')
 elif name=='gazebo':
  cyl((0,0,.12),1.8,.24,'wood',8)
  for i in range(8):a=i*math.tau/8;cyl((1.55*math.cos(a),1.55*math.sin(a),1.4),.07,2.6,'wood')
  cyl((0,0,3),2.1,1,'darkleaf',8,r2=0)
 elif name=='pergola':
  legs(3,2,2.5,'wood',.1)
  for y in [-1,1]:box((0,y,2.5),(3.5,.16,.2))
  for i in range(8):box((-1.6+i*.46,0,2.65),(.12,2.6,.15))
 elif name=='bus_shelter':
  for x in [-1.5,1.5]:box((x,.5,1.3),(.1,.1,2.6),'metal')
  box((0,.55,1.4),(3,.07,2),'glass');box((0,0,2.65),(3.5,1.6,.12),'metal');box((0,.25,.5),(2.5,.45,.1),'wood');legs(2,.3,.5,'metal')
 elif name=='well':
  for i in range(16):a=i*math.tau/16;box((.7*math.cos(a),.7*math.sin(a),.5),(.3,.3,1),'stone',a)
  for x in [-.9,.9]:box((x,0,1.4),(.12,.12,2.8))
  cyl((0,0,2.85),1.4,.6,'terracotta',4,r2=0);beam((-.9,0,1.85),(.9,0,1.85),.08,'wood');beam((0,0,1.85),(0,0,.7),.02,'bark')
 elif name=='planter_box':
  box((0,0,.35),(1.6,.7,.7));box((0,0,.71),(1.4,.5,.02),'soil')
  for i in range(5):ball((-.6+i*.3,0,.85),(.25,.25,.3),'leaf',2)
 elif name=='bollard_row':
  for x in [-1,0,1]:cyl((x,0,.45),.09,.9,'metal');cyl((x,0,.7),.095,.1,'yellow')
INFRA=['wooden_bridge','arched_bridge','stone_bridge','truss_bridge','rope_bridge','picket_fence','rail_fence','metal_fence','brick_wall','stone_wall','gate','stairs','ramp','wooden_dock','gazebo','pergola','bus_shelter','well','planter_box','bollard_row']

def signs(name):
 if name in ['a_frame','menu_board']:
  for y in [-.3,.3]:
   for x in [-.35,.35]:beam((x,y,0),(x,0,1.1),.035,'wood')
  box((0,-.15,.65),(.65,.06,.75),'black');text('MENU' if name=='menu_board' else 'OPEN',(0,-.19,.8),.16)
  for z in [.4,.5,.6]:box((0,-.19,z),(.38,.01,.015),'white')
  return
 if name=='notice_board':
  for x in [-.8,.8]:box((x,0,1),(.1,.1,2))
  box((0,0,1.5),(1.8,.12,1),'wood');box((0,-.07,1.5),(1.6,.02,.8),'white')
  for x in [-.5,0,.5]:box((x,-.09,1.5),(.35,.02,.55),'blue' if x==0 else 'yellow')
  return
 if name=='direction_post':
  cyl((0,0,1.2),.07,2.4,'wood')
  for i,t in enumerate(['PARK','CAFE','TRAIL']):box(((-1)**i*.25,-.05,2.1-i*.4),(1.2,.08,.25),'wood');text(t,((-1)**i*.25,-.1,2.1-i*.4),.17)
  return
 cyl((0,0,1),.045,2,'metal');cyl((0,0,.04),.18,.08,'concrete')
 labels={'parking':'P','bus_stop':'BUS','speed_30':'30','speed_50':'50','stop':'STOP','information':'i','hospital':'H','cafe':'CAFE','exit':'EXIT','park':'PARK','no_entry':'','warning':'!','crosswalk':'','bicycle':'BIKE','toilet':'WC','street_name':'MAPLE ST'}
 if name in ['speed_30','speed_50','no_entry']:
  o=cyl((0,-.04,2),.36,.07,'red',32);o.rotation_euler.x=math.pi/2
  if name!='no_entry':o=cyl((0,-.08,2),.29,.015,'white',32);o.rotation_euler.x=math.pi/2;text(labels[name],(0,-.095,2),.3,'black')
  else:box((0,-.09,2),(.48,.02,.1),'white')
 elif name=='stop':
  o=cyl((0,-.04,2),.4,.07,'red',8);o.rotation_euler.x=math.pi/2;text('STOP',(0,-.085,2),.21)
 elif name in ['warning','crosswalk']:
  o=cyl((0,-.04,2),.46,.07,'yellow' if name=='warning' else 'blue',3);o.rotation_euler=(math.pi/2,0,0);text('!' if name=='warning' else 'WALK',(0,-.09,1.95),.3 if name=='warning' else .14,'black' if name=='warning' else 'white')
 else:
  wide=name in ['street_name','cafe','park','exit'];box((0,-.04,2),(1.15 if wide else .65,.08,.4 if wide else .7),'darkleaf' if wide else 'blue');text(labels.get(name,name.upper()),(0,-.09,2),.18 if wide else .25)
SIGNS=['parking','bus_stop','speed_30','speed_50','stop','information','hospital','cafe','exit','park','no_entry','warning','crosswalk','bicycle','toilet','street_name','a_frame','menu_board','notice_board','direction_post']

def street(name):
 if name in ['bench','park_bench']:
  slats(1.8,.55,.48,4);legs(1.4,.4,.45,'metal')
  if name=='park_bench':
   for z in [.75,.95]:box((0,.27,z),(1.8,.07,.15))
   for x in [-.7,.7]:beam((x,.25,.3),(x,.3,1.05),.035)
 elif name=='picnic_table':
  slats(1.8,.85,.8,6)
  for y in [-.75,.75]:slats(1.8,.3,.45,1) if False else box((0,y,.45),(1.8,.28,.09))
  for x in [-.6,.6]:
   for y in [-.65,.65]:beam((x,y,0),(x,y*.4,.8),.06,'wood')
   box((x,0,.35),(.12,1.8,.1))
 elif name in ['trash_bin','recycling_bin']:
  cyl((0,0,.45),.3,.9,'darkleaf' if name=='trash_bin' else 'blue');cyl((0,0,.94),.34,.09,'metal');box((0,-.3,.65),(.32,.03,.14),'black')
  if name=='recycling_bin':text('R',(0,-.32,.4),.2)
 elif name=='street_lamp':
  cyl((0,0,.12),.18,.24);cyl((0,0,1.8),.06,3.6);beam((0,0,3.6),(.7,0,3.6),.06);box((.65,0,3.56),(.55,.3,.12),'metal');box((.65,0,3.49),(.44,.24,.025),'white')
 elif name=='lantern_lamp':
  cyl((0,0,1.25),.06,2.5);box((0,0,2.7),(.34,.34,.45),'yellow');cyl((0,0,3.02),.35,.25,'black',4,r2=0)
  for x in [-.17,.17]:
   for y in [-.17,.17]:box((x,y,2.7),(.025,.025,.5),'black')
 elif name=='traffic_light':
  cyl((0,0,1.4),.06,2.8);box((0,0,2.55),(.35,.22,.95),'black')
  for i,c in enumerate(['leaf','yellow','red']):o=cyl((0,-.125,2.25+i*.3),.105,.035,c,20);o.rotation_euler.x=math.pi/2
 elif name=='hydrant':
  cyl((0,0,.4),.14,.8,'red');ball((0,0,.8),(.15,.15,.12),'red',2);beam((-.27,0,.55),(.27,0,.55),.09,'red');cyl((0,0,.06),.2,.12,'metal')
 elif name=='post_box':
  box((0,0,.65),(.55,.42,1.3),'red');box((0,-.22,1.02),(.35,.02,.06),'black');text('POST',(0,-.225,.75),.12);box((0,-.22,.3),(.38,.02,.35),'red')
 elif name in ['traffic_cone','road_barrier']:
  if name=='traffic_cone':box((0,0,.04),(.42,.42,.08),'black');cyl((0,0,.36),.17,.64,'orange',16,r2=.035);cyl((0,0,.4),.105,.12,'white',16,r2=.08)
  else:
   for x in [-.8,.8]:box((x,0,.4),(.08,.08,.8),'metal');box((x,0,.04),(.15,.6,.08),'metal')
   box((0,0,.7),(1.9,.15,.3),'orange')
   for x in [-.6,-.2,.2,.6]:box((x,-.08,.7),(.18,.01,.28),'white')
 elif name=='bike_rack':
  for x in [-.75,0,.75]:beam((x,-.3,0),(x,-.3,.7),.035);beam((x,.3,0),(x,.3,.7),.035);beam((x,-.3,.7),(x,.3,.7),.035)
 elif name=='drinking_fountain':
  cyl((0,0,.45),.15,.9,'stone');cyl((0,0,.92),.3,.08,'metal');beam((.16,0,.94),(.16,0,1.07),.025)
 elif name=='fountain':
  cyl((0,0,.15),1.3,.3,'stone',32);cyl((0,0,.31),1.14,.02,'blue',32);cyl((0,0,.75),.17,.9,'stone');cyl((0,0,1.15),.6,.1,'stone',24);cyl((0,0,1.21),.52,.01,'blue',24);ball((0,0,1.4),(.15,.15,.2),'stone',2)
 elif name=='utility_box':
  box((0,0,.7),(.8,.45,1.4),'stone');box((0,-.235,.75),(.7,.02,1.1),'concrete')
  for i in range(6):box((0,-.25,.4+i*.08),(.5,.01,.018),'black')
 elif name=='vending_machine':
  box((0,0,.9),(.9,.65,1.8),'red');box((-.12,-.335,1.15),(.53,.025,.9),'glass')
  for z in [.85,1.1,1.35]:
   for x in [-.28,-.1,.08]:cyl((x,-.37,z),.045,.15,'yellow' if x<0 else 'blue')
  box((0,-.34,.3),(.6,.025,.2),'black');box((.3,-.34,.9),(.12,.025,.25),'metal')
 elif name=='manhole':
  cyl((0,0,.025),.45,.05,'metal',32)
  for i in range(-3,4):box((0,i*.09,.054),(.6,.025,.01),'black')
 elif name=='tree_guard':
  for i in range(12):a=i*math.tau/12;beam((.45*math.cos(a),.45*math.sin(a),0),(.45*math.cos(a),.45*math.sin(a),1),.018)
  for z in [.15,.9]:ring((0,0,z),.45,.025)
 elif name=='sandbox':
  box((0,0,.1),(2,2,.2),'yellow')
  for y in [-1,1]:box((0,y,.15),(2.2,.18,.3))
  for x in [-1,1]:box((x,0,.15),(.18,2.2,.3))
STREET=['bench','park_bench','picnic_table','trash_bin','recycling_bin','street_lamp','lantern_lamp','traffic_light','hydrant','post_box','traffic_cone','road_barrier','bike_rack','drinking_fountain','fountain','utility_box','vending_machine','manhole','tree_guard','sandbox']

def furniture(name):
 if name in ['chair','stool','dining_table','coffee_table','desk']:
  w,d,h={'chair':(.48,.48,.48),'stool':(.4,.4,.48),'dining_table':(1.5,.9,.75),'coffee_table':(1,.55,.42),'desk':(1.3,.65,.75)}[name];box((0,0,h),(w,d,.08));legs(w*.8,d*.8,h)
  if name=='chair':box((0,.21,.77),(.48,.07,.5));
  if name=='desk':box((.4,0,.53),(.35,.5,.35));box((.4,-.26,.54),(.12,.025,.025),'metal')
 elif name in ['sofa','armchair']:
  w=1.8 if name=='sofa' else .85;legs(w-.2,.6,.15,'black');box((0,0,.3),(w,.8,.35),'fabric');box((0,.32,.65),(w,.18,.7),'fabric')
  for x in [-w/2,w/2]:box((x,0,.53),(.18,.85,.45),'fabric')
  for i in range(2 if name=='sofa' else 1):box(((-.42 if i==0 else .42) if name=='sofa' else 0,-.02,.51),(.78 if name=='sofa' else .6,.6,.12),'lightleaf')
 elif name in ['bookshelf','cabinet','wardrobe']:
  w=1.2;h=1.8
  for x in [-.6,.6]:box((x,0,h/2),(.08,.4,h))
  box((0,.18,h/2),(1.2,.04,h))
  for z in [0.04,.6,1.2,1.8]:box((0,0,z),(1.2,.4,.06))
  if name!='bookshelf':
   for x in [-.3,.3]:box((x,-.22,.9),(.58,.05,1.7));box((x*.25,-.26,.9),(.03,.04,.16),'metal')
  else:
   for z in [.08,.64,1.24]:
    for i in range(7):box((-.48+i*.14,0,z+.18),(.09,.23,.36),['red','blue','yellow','darkleaf'][i%4])
 elif name=='bed':
  legs(1.2,1.8,.25);box((0,0,.3),(1.4,2,.2));box((0,0,.48),(1.35,1.95,.2),'white');box((0,-.35,.6),(1.36,1.2,.08),'blue');box((0,.95,.6),(1.45,.12,1));box((0,.65,.63),(.9,.42,.16),'white')
 elif name=='nightstand':
  legs(.4,.35,.2);box((0,0,.4),(.5,.45,.4));box((0,-.235,.4),(.42,.02,.3),'terracotta');ball((0,-.27,.4),(.025,)*3,'metal')
 elif name=='floor_lamp':
  cyl((0,0,.04),.25,.08,'black');cyl((0,0,.85),.025,1.7,'metal');cyl((0,0,1.65),.35,.45,'white',20,r2=.2)
 elif name=='table_lamp':
  cyl((0,0,.025),.13,.05,'metal');cyl((0,0,.25),.025,.45,'metal');cyl((0,0,.48),.2,.25,'yellow',20,r2=.1)
 elif name=='coat_rack':
  cyl((0,0,.025),.3,.05,'wood');cyl((0,0,.9),.04,1.8,'wood')
  for i in range(6):a=i*math.tau/6;beam((0,0,1.4),(.3*math.cos(a),.3*math.sin(a),1.65),.025,'wood')
 elif name=='tv_stand':
  box((0,0,.3),(1.4,.4,.6));box((0,-.21,.3),(1.2,.02,.38),'black');box((0,0,.66),(.5,.25,.04),'black');box((0,0,1.1),(1.15,.08,.65),'black');box((0,-.045,1.1),(1.04,.01,.54),'blue')
 elif name=='refrigerator':
  box((0,0,.9),(.7,.65,1.8),'white')
  for z,h in [(1.5,.55),(.6,1.18)]:box((0,-.34,z),(.66,.03,h),'concrete');box((-.25,-.38,z),(.03,.05,.25),'metal')
 elif name=='washing_machine':
  box((0,0,.45),(.65,.6,.9),'white');o=cyl((0,-.31,.42),.23,.04,'metal',32);o.rotation_euler.x=math.pi/2;o=cyl((0,-.34,.42),.18,.02,'glass',32);o.rotation_euler.x=math.pi/2;box((0,-.31,.8),(.5,.02,.08),'black')
 elif name=='kitchen_sink':
  box((0,0,.45),(1,.6,.9),'wood');box((0,0,.92),(1.05,.65,.06),'metal');box((0,-.03,.955),(.65,.4,.01),'black');beam((0,.2,.96),(0,.2,1.2),.025);beam((0,.2,1.2),(0,0,1.2),.025)
 elif name=='wall_clock':
  o=cyl((0,0,.3),.3,.06,'wood',32);o.rotation_euler.x=math.pi/2;o=cyl((0,-.04,.3),.26,.02,'white',32);o.rotation_euler.x=math.pi/2;beam((0,-.06,.3),(0,-.06,.49),.009,'black');beam((0,-.06,.3),(.13,-.06,.3),.012,'black')
FURNITURE=['chair','stool','dining_table','coffee_table','desk','sofa','armchair','bookshelf','cabinet','wardrobe','bed','nightstand','floor_lamp','table_lamp','coat_rack','tv_stand','refrigerator','washing_machine','kitchen_sink','wall_clock']

def props(name):
 if name in ['cardboard_box','wood_crate','parcel']:
  box((0,0,.3),(.6,.5,.6),'wood' if name=='wood_crate' else 'terracotta')
  if name=='wood_crate':
   for z in [.06,.3,.54]:
    for y in [-.26,.26]:box((0,y,z),(.64,.035,.08),'wood')
   for x in [-.25,.25]:box((x,-.29,.3),(.07,.04,.6),'bark')
  else:box((0,0,.605),(.1,.5,.01),'yellow');box((.13,-.255,.35),(.2,.01,.15),'white')
 elif name=='barrel':
  cyl((0,0,.45),.32,.9,'wood',16)
  for z in [.1,.45,.8]:ring((0,0,z),.325,.025,'metal')
 elif name=='bucket':
  cyl((0,0,.18),.15,.36,'blue',20,r2=.2);cyl((0,0,.365),.18,.008,'black');ring((0,0,.36),.2,.018,'metal');ring((0,0,.43),.2,.012,'metal',(math.pi/2,0,0))
 elif name=='watering_can':
  cyl((0,0,.2),.18,.4,'darkleaf');beam((.1,0,.1),(.45,0,.4),.035,'darkleaf');ball((.45,0,.4),(.07,.07,.035),'metal');ring((-.19,0,.25),.15,.025,'darkleaf',(math.pi/2,0,0))
 elif name=='flower_pot':pot();beam((0,0,.5),(0,0,1),.025,'leaf');ball((0,0,1),(.23,.23,.16),'pink',2)
 elif name=='potted_plant':
  pot()
  for i in range(7):a=i*2.4;beam((0,0,.45),(.25*math.cos(a),.25*math.sin(a),.8+i*.07),.015,'leaf');ball((.25*math.cos(a),.25*math.sin(a),.8+i*.07),(.2,.15,.12),'leaf',2)
 elif name in ['bottle','thermos']:
  cyl((0,0,.15),.07,.3,'blue' if name=='bottle' else 'metal');cyl((0,0,.325),.04,.05,'blue');cyl((0,0,.37),.035,.04,'black')
 elif name=='mug':
  cyl((0,0,.07),.075,.14,'white',24);cyl((0,0,.142),.063,.006,'bark');ring((.085,0,.075),.05,.014,'white',(math.pi/2,0,0))
 elif name=='plate':cyl((0,0,.014),.15,.028,'white',32);ring((0,0,.026),.14,.012,'white')
 elif name=='book_stack':
  for i in range(4):
   z=.025+i*.055;box((0,0,z),(.22,.3,.045),'white',i*.12);box((0,0,z+.025),(.235,.315,.008),['red','blue','yellow','darkleaf'][i],i*.12)
 elif name=='laptop':
  box((0,0,.015),(.34,.24,.03),'metal');box((0,.105,.135),(.34,.025,.24),'black');box((0,.09,.135),(.3,.005,.2),'blue');box((0,0,.033),(.28,.13,.006),'black')
 elif name=='suitcase':
  box((0,0,.4),(.5,.25,.7),'blue')
  for x in [-.18,.18]:ball((x,0,.05),(.05,.05,.05),'black',2);beam((x*.5,0,.75),(x*.5,0,1),.012)
  beam((-.09,0,1),(.09,0,1),.025,'black')
 elif name=='ladder':
  for x in [-.25,.25]:box((x,0,1),(.06,.08,2),'metal')
  for i in range(7):box((0,0,.15+i*.27),(.5,.08,.04),'metal')
 elif name=='shovel':
  cyl((0,0,.65),.025,1,'wood');box((0,0,.14),(.2,.035,.28),'metal');ring((0,0,1.2),.085,.018,'black',(math.pi/2,0,0))
 elif name=='broom':cyl((0,0,.7),.022,1.2,'wood');box((0,0,.12),(.32,.08,.24),'yellow')
 elif name=='wheelbarrow':
  box((0,0,.5),(.6,.8,.3),'darkleaf');o=cyl((0,-.55,.22),.22,.12,'black',20);o.rotation_euler.y=math.pi/2
  for x in [-.25,.25]:beam((x,-.5,.25),(x,.85,.65),.025);beam((x,.2,.4),(x,.35,0),.025)
 elif name=='pallet':
  for x in [-.48,0,.48]:box((x,0,.08),(.12,.8,.16))
  for i in range(6):box((0,-.4+i*.16,.18),(1.1,.12,.06))
PROPS=['cardboard_box','wood_crate','parcel','barrel','bucket','watering_can','flower_pot','potted_plant','bottle','thermos','mug','plate','book_stack','laptop','suitcase','ladder','shovel','broom','wheelbarrow','pallet']

GROUPS={'nature':(NATURE,nature),'infrastructure':(INFRA,infrastructure),'signs':(SIGNS,signs),'street':(STREET,street),'furniture':(FURNITURE,furniture),'props':(PROPS,props)}
def bounds(objects):
 pts=[o.matrix_world@Vector(v) for o in objects for v in o.bound_box];lo=Vector(tuple(min(v[i] for v in pts) for i in range(3)));hi=Vector(tuple(max(v[i] for v in pts) for i in range(3)));return lo,hi

def run(group):
 names,build=GROUPS[group];records=[]
 for name in names:
  bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);build(name);bpy.context.view_layer.update();objects=list(bpy.context.scene.objects);lo,hi=bounds(objects)
  # Center horizontal footprint and put lowest point exactly on ground.
  delta=Vector((-(lo.x+hi.x)/2,-(lo.y+hi.y)/2,-lo.z))
  for o in objects:o.location+=delta
  bpy.context.view_layer.update();lo,hi=bounds(objects)
  for i,o in enumerate(objects):o.name=f'{name}_{i:03d}'
  bpy.ops.object.select_all(action='SELECT');out=ROOT/'assets'/group/f'{name}.glb';out.parent.mkdir(parents=True,exist_ok=True)
  bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',use_selection=True,export_yup=True,export_cameras=False,export_lights=False,export_animations=False)
  records.append({'id':name,'category':group,'path':str(out.relative_to(ROOT)),'dimensions_m':{'x':round(hi.x-lo.x,3),'y':round(hi.z-lo.z,3),'z':round(hi.y-lo.y,3)},'bytes':out.stat().st_size})
  # Isolated studio thumbnail, camera/light never exported.
  center=(lo+hi)/2;size=max(hi-lo);bpy.ops.object.camera_add(location=center+Vector((1.4,-1.9,1.35))*size);cam=bpy.context.object;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=size*1.65;bpy.context.scene.camera=cam
  bpy.ops.object.light_add(type='AREA',location=center+Vector((1,-2,4))*size);bpy.context.object.data.energy=450*size*size;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=size*4
  sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=24;sc.cycles.use_denoising=False;sc.world.color=(.35,.35,.35);sc.render.resolution_x=240;sc.render.resolution_y=240;sc.render.resolution_percentage=100;sc.render.film_transparent=True;sc.view_settings.view_transform='Standard'
  thumb=ROOT/'previews'/group/f'{name}.png';thumb.parent.mkdir(parents=True,exist_ok=True);sc.render.filepath=str(thumb);bpy.ops.render.render(write_still=True)
  print('ASSET_DONE',group,name,flush=True)
 (ROOT/'assets'/group/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else list(GROUPS)
 for group in args:run(group)
