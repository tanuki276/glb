"""Second collection: 80 everyday models. Blender 4.3.2.
blender -b -t 2 --python scripts/generate_expansion.py
Categories: transport buildings recreation kitchen
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from generate import *

def wheels(length=2.4,width=1.45,r=.31,z=None):
 z=r if z is None else z
 for x in [-width/2,width/2]:
  for y in [-length/2,length/2]:
   o=cyl((x,y,z),r,.17,'black',20);o.rotation_euler.y=math.pi/2
   o=cyl((x+(.09 if x>0 else -.09),y,z),r*.48,.018,'metal',16);o.rotation_euler.y=math.pi/2

def car_body(kind):
 color={'taxi':'yellow','police_car':'white','hatchback':'leaf','sedan':'blue'}.get(kind,'red')
 box((0,0,.65),(1.6,3.4,.58),color);wheels()
 if kind=='hatchback':
  box((0,.15,1.12),(1.42,1.8,.6),color);box((0,-.77,1.17),(1.23,.035,.42),'glass')
 else:
  box((0,.1,1.1),(1.4,1.65,.55),color);box((0,-.75,1.15),(1.2,.035,.35),'glass')
 for x in [-.715,.715]:
  for y in [-.35,.4]:box((x,y,1.15),(.015,.65,.35),'glass')
  box((x,.65,.8),(.02,.18,.035),'metal')
 for x in [-.55,.55]:
  box((x,-1.71,.7),(.35,.02,.15),'white');box((x,1.71,.7),(.3,.02,.15),'red')
 box((0,-1.73,.42),(1.45,.07,.1),'metal');box((0,1.73,.42),(1.45,.07,.1),'metal')
 if kind=='taxi':box((0,.1,1.48),(.55,.25,.17),'white');text('TAXI',(0,-.03,1.48),.13,'black')
 if kind=='police_car':
  box((0,.15,1.45),(1,.22,.08),'black')
  for x,c in [(-.32,'red'),(.32,'blue')]:cyl((x,.15,1.55),.12,.16,c)
  for x in [-.81,.81]:box((x,0,.7),(.02,1.4,.2),'black')

def transport(name):
 if name in ['sedan','hatchback','taxi','police_car']:car_body(name)
 elif name in ['van','ambulance','delivery_truck','pickup']:
  color='white' if name in ['ambulance','delivery_truck'] else 'blue';box((0,0,.65),(1.7,3.6,.5),color);wheels(2.5,1.6,.34)
  box((0,-.85,1.2),(1.65,1.35,.85),color);box((0,-1.54,1.35),(1.35,.03,.45),'glass')
  for x in [-.84,.84]:box((x,-.85,1.4),(.025,.95,.4),'glass')
  if name=='pickup':
   box((0,.85,.93),(1.55,1.7,.1),'black')
   for x in [-.8,.8]:box((x,.85,1.08),(.1,1.7,.45),color)
   box((0,1.65,1.08),(1.6,.1,.45),color)
  else:
   box((0,.65,1.35),(1.72,2.25,1.4 if name=='delivery_truck' else 1.1),color)
   if name=='ambulance':
    box((0,-.85,1.7),(1,.22,.12),'red')
    for x in [-.87,.87]:box((x,.7,1.45),(.025,.5,.13),'red');box((x,.7,1.45),(.025,.13,.5),'red')
   if name=='van':
    for x in [-.87,.87]:box((x,.65,1.5),(.02,1.6,.4),'glass')
  for x in [-.6,.6]:box((x,-1.82,.8),(.25,.03,.15),'white')
 elif name in ['city_bus','school_bus']:
  color='yellow' if name=='school_bus' else 'fabric';box((0,0,1.15),(2.2,6,1.8),color);wheels(4.2,2.15,.45)
  box((0,-3.02,1.6),(1.95,.04,.65),'glass')
  for x in [-1.11,1.11]:
   for i in range(7):box((x,-2.5+i*.8,1.65),(.025,.65,.6),'glass')
   box((x,0,.85),(.02,5.5,.08),'black')
  box((.65,-3.04,1),(.55,.025,1.4),'black');box((.65,-3.06,1.4),(.42,.01,.55),'glass');text('SCHOOL' if name=='school_bus' else 'CITY',(0,-3.06,2.0),.18,'black')
 elif name=='fire_truck':
  box((0,0,.9),(2,4.8,.9),'red');wheels(3.3,1.95,.4);box((0,-1.5,1.65),(2,1.5,1),'red');box((0,-2.27,1.8),(1.7,.03,.6),'glass')
  for x in [-.65,.65]:cyl((x,-1.4,2.22),.13,.18,'blue')
  for x in [-1.01,1.01]:
   for y in [-.2,.7,1.6]:box((x,y,1.15),(.02,.75,.6),'metal')
  for x in [-.35,.35]:box((x,.6,1.95),(.06,3.4,.06),'metal')
  for i in range(12):box((0,-.95+i*.28,1.95),(.7,.05,.05),'metal')
 elif name in ['bicycle','motorcycle','scooter']:
  r=.32 if name=='bicycle' else .25;length=1.2
  for y in [-length/2,length/2]:
   ring((0,y,r),r,.045 if name=='bicycle' else .09,'black',(0,math.pi/2,0));beam((-.09,y,r),(.09,y,r),.035)
   if name=='bicycle':
    for j in range(10):a=j*math.tau/10;beam((0,y,r),(0,y+math.cos(a)*r,r+math.sin(a)*r),.006,'metal')
  if name=='scooter':
   box((0,0,.22),(.3,1,.1),'blue');beam((0,-.6,.3),(0,-.6,1.1),.03);beam((-.3,-.6,1.1),(.3,-.6,1.1),.025,'black')
  else:
   for a,b in [((0,-.6,r),(0,-.35,.9)),((0,-.35,.9),(0,.3,.8)),((0,.3,.8),(0,.6,r)),((0,.6,r),(0,0,.32)),((0,0,.32),(0,-.35,.9)),((0,0,.32),(0,.3,.8))]:beam(a,b,.024 if name=='bicycle' else .055,'red')
   box((0,.3,.85),(.23,.3,.08),'black');beam((-.3,-.35,1),(.3,-.35,1),.025,'black')
   if name=='motorcycle':ball((0,-.1,.65),(.2,.3,.22),'blue',2);box((0,.05,.43),(.26,.35,.25),'metal')
 elif name=='forklift':
  box((0,.2,.5),(1.1,1.7,.65),'yellow');wheels(1.1,1.05,.27)
  for x in [-.4,.4]:box((x,-.8,1.1),(.07,.12,2.2),'metal');box((x,-1.35,.12),(.12,1.1,.07),'metal');beam((x,.65,.7),(x,.65,1.8),.035)
  box((0,.2,1.85),(1.15,1.15,.1),'black');box((0,.2,.95),(.45,.5,.15),'black');box((0,.45,1.18),(.45,.1,.45),'black')
 elif name=='tractor':
  box((0,0,.65),(1.1,2,.45),'leaf');box((0,-.5,1),(1,1,.5),'leaf')
  for x in [-.65,.65]:
   for y,r in [(-.75,.3),(.65,.5)]:o=cyl((x,y,r),r,.25,'black',20);o.rotation_euler.y=math.pi/2;o=cyl((x+(.14 if x>0 else -.14),y,r),r*.5,.02,'yellow');o.rotation_euler.y=math.pi/2
  box((0,.4,1.05),(.5,.55,.15),'black');box((0,.65,1.3),(.5,.1,.4),'black');cyl((.35,-.5,1.5),.045,.7,'black');beam((0,0,.9),(0,0,1.35),.03);ring((0,0,1.35),.16,.02,'black')
 elif name in ['handcart','shopping_cart','stroller']:
  wheels(.65,.6,.09);box((0,0,.22),(.65,.8,.06),'metal')
  if name=='handcart':
   for x in [-.3,.3]:beam((x,.4,.2),(x,.4,1),.03)
   beam((-.3,.4,1),(.3,.4,1),.03,'black')
  elif name=='shopping_cart':
   for x in [-.32,.32]:
    for i in range(6):beam((x,-.35+i*.14,.35),(x,-.35+i*.14,.8),.01)
    for z in [.35,.55,.8]:beam((x,-.4,z),(x,.4,z),.013)
   for y in [-.4,.4]:
    for i in range(5):beam((-.3+i*.15,y,.35),(-.3+i*.15,y,.8),.01)
   beam((-.32,.5,.9),(.32,.5,.9),.025,'red')
  else:
   box((0,0,.4),(.5,.55,.12),'fabric');box((0,.23,.65),(.5,.1,.5),'fabric');cyl((0,.1,.95),.42,.18,'blue',12,r2=.28)
   for x in [-.3,.3]:beam((x,.2,.3),(x,.6,1),.025)
   beam((-.3,.6,1),(.3,.6,1),.025,'black')
TRANSPORT=['sedan','hatchback','taxi','police_car','van','ambulance','delivery_truck','pickup','city_bus','school_bus','fire_truck','bicycle','motorcycle','scooter','forklift','tractor','handcart','shopping_cart','stroller','cargo_trailer']
# Small utility trailer is separate from a powered vehicle.
_transport=transport
def transport(name):
 if name!='cargo_trailer':return _transport(name)
 box((0,0,.5),(1.3,1.8,.12),'metal')
 for x in [-.67,.67]:box((x,0,.8),(.07,1.8,.5),'wood');o=cyl((x,0,.3),.3,.18,'black',20);o.rotation_euler.y=math.pi/2
 for y in [-.9,.9]:box((0,y,.8),(1.35,.07,.5),'wood')
 beam((-.5,-.9,.45),(0,-1.7,.4),.035);beam((.5,-.9,.45),(0,-1.7,.4),.035)

def roof(w,d,z,mat='terracotta'):
 # True triangular-prism gable roof; ridge follows Y.
 vs=[(-w/2,-d/2,z),(w/2,-d/2,z),(0,-d/2,z+w*.3),(-w/2,d/2,z),(w/2,d/2,z),(0,d/2,z+w*.3)]
 mesh=bpy.data.meshes.new('gable');mesh.from_pydata(vs,[],[(0,2,1),(3,4,5),(0,3,5,2),(2,5,4,1),(0,1,4,3)]);mesh.update();o=bpy.data.objects.new('roof',mesh);bpy.context.collection.objects.link(o);finish(o,'gable_roof',mat)
def window(x,y,z,w=.7,h=.8):
 box((x,y,z),(w+.1,.09,h+.1),'white');box((x,y-.05,z),(w,.018,h),'glass');box((x,y-.07,z),(.045,.015,h),'white');box((x,y-.07,z),(w,.015,.045),'white')
def door(x,y,z=.95,w=.75,h=1.9):
 box((x,y,z),(w,.07,h),'wood');ball((x+w*.3,y-.055,z),(.035,)*3,'metal',2)
def house(w=4,d=3,h=2.6,color='white'):
 box((0,0,h/2),(w,d,h),color);roof(w+.3,d+.3,h);door(0,-d/2-.04)
 for x in [-w*.3,w*.3]:window(x,-d/2-.04,1.5)
 box((w*.25,.5,h+.5),(.35,.4,1.2),'stone')
def buildings(name):
 if name in ['cottage','cabin','townhouse']:
  if name=='cottage':house()
  elif name=='cabin':house(3,3,2.2,'wood')
  else:
   house(3,3,4.8,'terracotta')
   for x in [-.85,.85]:window(x,-1.54,3.7)
 elif name in ['apartment','office']:
  floors=4 if name=='apartment' else 5;w=5;d=3.5;box((0,0,floors*1.4),(w,d,floors*2.8),'concrete' if name=='apartment' else 'metal');box((0,0,floors*2.8+.1),(w+.3,d+.3,.2),'stone');door(0,-1.8)
  for f in range(floors):
   for x in [-1.7,0,1.7]:window(x,-1.8,1.5+f*2.8,1,1.1)
   box((0,-1.86,f*2.8+.3),(5,.15,.1),'white')
 elif name in ['corner_shop','bakery','coffee_shop']:
  box((0,0,1.5),(4,3,3),'white');box((0,0,3.1),(4.2,3.2,.2),'stone');door(1.25,-1.54)
  window(-.7,-1.55,1.25,2,1.6);box((0,-1.6,2.6),(3.7,.14,.5),'darkleaf' if name=='coffee_shop' else 'red');text({'corner_shop':'SHOP','bakery':'BAKERY','coffee_shop':'CAFE'}[name],(0,-1.69,2.6),.3)
  for i in range(8):box((-1.75+i*.5,-1.95,2.2),(.49,.9,.08),'white' if i%2 else ('fabric' if name=='coffee_shop' else 'red'))
 elif name in ['garage','garden_shed','warehouse','barn']:
  w,d,h={'garage':(3.5,4,2.7),'garden_shed':(2,2,2.2),'warehouse':(7,5,4),'barn':(5,6,3.5)}[name];box((0,0,h/2),(w,d,h),'red' if name=='barn' else 'wood' if name=='garden_shed' else 'concrete');roof(w+.3,d+.3,h,'metal')
  if name=='garden_shed':door(0,-d/2-.04,.9,.8,1.8)
  else:
   box((0,-d/2-.04,h*.4),(w*.65,.08,h*.75),'wood' if name=='barn' else 'metal')
   if name=='barn':
    beam((-w*.3,-d/2-.1,.1),(w*.3,-d/2-.1,h*.75),.07,'white');beam((w*.3,-d/2-.1,.1),(-w*.3,-d/2-.1,h*.75),.07,'white')
   else:
    for i in range(8):box((0,-d/2-.09,.15+i*h*.09),(w*.65,.02,.025),'black')
 elif name=='greenhouse':
  box((0,0,1),(3,4,2),'glass');roof(3,4,2,'glass')
  for x in [-1.5,1.5]:
   for y in [-2,-1,0,1,2]:beam((x,y,0),(x,y,2),.035,'white');beam((x,y,2),(0,y,2.9),.035,'white')
  for z in [.1,1,2]:
   for x in [-1.52,1.52]:beam((x,-2,z),(x,2,z),.035,'white')
  door(0,-2.05,1,.8,2)
 elif name=='chapel':
  house(3,5,3,'white');box((0,-1.8,3),(1,1.1,6),'stone');roof(1.3,1.4,6,'metal');beam((0,-1.8,6.3),(0,-1.8,7.2),.04,'wood');beam((-.25,-1.8,6.9),(.25,-1.8,6.9),.04,'wood');door(0,-2.55)
 elif name=='lighthouse':
  cyl((0,0,3),1,6,'white',20,r2=.65)
  for z in [1.5,3.5]:cyl((0,0,z),1-z*.35/6+.01,.5,'red',20,r2=1-(z+.5)*.35/6+.01)
  cyl((0,0,6.1),.95,.2,'metal',20);cyl((0,0,6.6),.6,.8,'glass',12);cyl((0,0,7.1),.9,.3,'red',12,r2=0);door(0,-1.01,.7,.5,1.4)
 elif name=='water_tower':
  for x in [-1,1]:
   for y in [-1,1]:beam((x,y,0),(x*.7,y*.7,4),.09,'metal')
  for y in [-1,1]:beam((-1,y,.2),(.7,y*.7,4),.04,'metal');beam((1,y,.2),(-.7,y*.7,4),.04,'metal')
  cyl((0,0,4.5),1.3,1.8,'blue',20);cyl((0,0,5.5),1.4,.3,'metal',20,r2=.1)
 elif name=='kiosk':
  box((0,0,1),(2,1.8,2),'yellow');box((0,-.94,1.4),(1.65,.06,.75),'black');box((0,-1.1,.95),(2,.5,.12),'wood');roof(2.4,2.2,2.1,'red');text('KIOSK',(0,-.99,1.95),.25,'black')
 elif name=='public_toilet':
  box((0,0,1.4),(3.5,2.5,2.8),'concrete');box((0,0,2.85),(3.8,2.8,.15),'metal')
  for x in [-.9,.9]:door(x,-1.29,1,.8,2);text('WC',(x,-1.35,2.4),.3,'blue')
 elif name=='bus_station':
  box((0,0,.1),(6,2.5,.2),'concrete')
  for x in [-2.6,0,2.6]:box((x,.9,1.5),(.12,.12,3),'metal')
  box((0,.96,1.7),(5.4,.06,2.2),'glass');box((0,0,3.05),(6.4,2.8,.15),'blue');box((0,.45,.6),(4.5,.5,.12),'wood');text('BUS STATION',(0,-1.43,2.95),.28)
 elif name=='recycling_shelter':
  for x in [-1.5,1.5]:
   for y in [-.8,.8]:box((x,y,1.2),(.1,.1,2.4),'metal')
  roof(3.4,2,2.4,'darkleaf')
  for x,c in [(-.9,'blue'),(0,'yellow'),(.9,'leaf')]:box((x,0,.6),(.7,.7,1.2),c);box((x,-.36,1),(.4,.02,.16),'black')
BUILDINGS=['cottage','cabin','townhouse','apartment','office','corner_shop','bakery','coffee_shop','garage','garden_shed','warehouse','barn','greenhouse','chapel','lighthouse','water_tower','kiosk','public_toilet','bus_station','recycling_shelter']

def recreation(name):
 if name=='swing_set':
  for x in [-1.5,1.5]:
   for y in [-.8,.8]:beam((x,y,0),(x,0,2.4),.06,'metal')
  beam((-1.7,0,2.4),(1.7,0,2.4),.07,'red')
  for x in [-.65,.65]:
   box((x,0,.5),(.55,.35,.08),'blue')
   for dx in [-.22,.22]:beam((x+dx,0,.5),(x+dx,0,2.4),.012,'metal')
 elif name=='slide':
  box((0,.7,1.5),(1,1,.12),'yellow');legs(.8,.8,1.5,'metal')
  for x in [-.4,.4]:beam((x,1.8,0),(x,1,1.5),.035,'metal')
  for i in range(6):box((0,1.75-i*.13,.12+i*.24),(.8,.12,.05),'metal')
  o=box((0,-.6,.85),(1,2.6,.08),'red');o.rotation_euler.x=math.radians(32)
  for x in [-.52,.52]:o=box((x,-.6,.98),(.06,2.6,.24),'yellow');o.rotation_euler.x=math.radians(32)
 elif name=='seesaw':
  cyl((0,0,.35),.3,.7,'blue',4,r2=.12);o=box((0,0,.7),(3,.3,.12),'wood');o.rotation_euler.y=.12
  for x in [-1.3,1.3]:box((x,0,.7-x*.12),(.45,.4,.07),'red');beam((x*.85,0,.75-x*.12),(x*.85,0,1.05-x*.12),.025)
 elif name=='roundabout':
  cyl((0,0,.16),1.2,.2,'red',24);cyl((0,0,.65),.05,1,'metal')
  for i in range(4):a=i*math.tau/4;beam((0,0,1),(math.cos(a),math.sin(a),1),.035);beam((math.cos(a),math.sin(a),.25),(math.cos(a),math.sin(a),1),.035)
 elif name=='basketball_hoop':
  box((0,.4,.08),(1,1,.16),'concrete');cyl((0,.4,1.6),.07,3.2);box((0,.35,3.1),(1.8,.08,1.1),'white');box((0,.29,3),(.65,.01,.4),'red');ring((0,-.15,2.85),.23,.025,'red')
  for i in range(12):a=i*math.tau/12;beam((.23*math.cos(a),-.15+.23*math.sin(a),2.85),(.16*math.cos(a),-.15+.16*math.sin(a),2.5),.006,'white')
 elif name=='soccer_goal':
  for x in [-1.5,1.5]:beam((x,0,0),(x,0,2),.05,'white');beam((x,0,2),(x,1,0),.03,'white')
  beam((-1.5,0,2),(1.5,0,2),.05,'white')
  for i in range(11):x=-1.5+i*.3;beam((x,0,2),(x,1,0),.006,'white')
  for i in range(8):z=i*.25;beam((-1.5,1-z/2,z),(1.5,1-z/2,z),.006,'white')
 elif name=='tennis_net':
  for x in [-2,2]:cyl((x,0,.6),.04,1.2,'metal')
  for i in range(17):x=-2+i*.25;beam((x,0,.25),(x,0,1.1),.005,'black')
  for z in [.25,.45,.65,.85,1.1]:beam((-2,0,z),(2,0,z),.008,'white' if z==1.1 else 'black')
 elif name in ['beach_umbrella','picnic_canopy']:
  if name=='beach_umbrella':cyl((0,0,1.2),.035,2.4,'wood');cyl((0,0,2.3),1.25,.55,'blue',12,r2=.03)
  else:
   legs(3,3,2.2,'metal',.04);cyl((0,0,2.6),2.35,.85,'white',4,r2=0)
 elif name=='deck_chair':
  for x in [-.35,.35]:beam((x,-.55,0),(x,.5,1.1),.035,'wood');beam((x,.55,0),(x,-.4,.55),.035,'wood')
  o=box((0,.13,.72),(.6,1.05,.03),'fabric');o.rotation_euler.x=.7
 elif name=='camping_tent':
  vs=[(-1,-1.3,0),(1,-1.3,0),(0,-1.3,1.5),(-1,1.3,0),(1,1.3,0),(0,1.3,1.5)];m=bpy.data.meshes.new('tent');m.from_pydata(vs,[],[(0,2,1),(3,4,5),(0,3,5,2),(2,5,4,1),(0,1,4,3)]);m.update();o=bpy.data.objects.new('tent',m);bpy.context.collection.objects.link(o);finish(o,'tent','orange')
  o=cyl((0,-1.32,.55),.65,.025,'black',3);o.rotation_euler.x=math.pi/2
  for x in [-1,1]:
   for y in [-1.3,1.3]:beam((x*.8,y,.35),(x*1.4,y*1.25,0),.008,'white')
 elif name=='campfire':
  for i in range(9):a=i*math.tau/9;ball((.65*math.cos(a),.65*math.sin(a),.12),(.18,.16,.14),'stone')
  for a in [0,math.pi/2]:beam((-.4*math.cos(a),-.4*math.sin(a),.15),(.4*math.cos(a),.4*math.sin(a),.15),.1,'bark')
  for i in range(5):a=i*2.4;cyl((.15*math.cos(a),.15*math.sin(a),.45),.16,.7,'orange' if i%2 else 'yellow',7,r2=0)
 elif name=='barbecue_grill':
  cyl((0,0,.65),.4,.3,'black',20);legs(.5,.5,.5,'metal',.025)
  for i in range(7):y=-.27+i*.09;beam((-.28,y,.81),(.28,y,.81),.008,'metal')
 elif name=='cooler_box':
  box((0,0,.23),(.65,.4,.46),'blue');box((0,0,.48),(.69,.44,.08),'white')
  for x in [-.35,.35]:box((x,0,.3),(.04,.2,.06),'white')
 elif name=='lifebuoy':
  ring((0,0,.08),.36,.1,'orange')
  for a in [0,math.pi/2,math.pi,math.pi*1.5]:box((math.cos(a)*.36,math.sin(a)*.36,.08),(.14,.19,.19),'white',a)
 elif name=='surfboard':
  ball((0,0,.08),(.38,1.4,.08),'blue',3);box((0,0,.15),(.08,2.1,.008),'white');o=cyl((0,.8,-.08),.16,.03,'black',3);o.rotation_euler.y=math.pi/2
 elif name=='kayak':
  ball((0,0,.24),(.48,1.8,.25),'yellow',3);ball((0,.1,.45),(.3,.5,.035),'black',2);beam((-.85,0,.6),(.85,0,.6),.018,'metal')
  for x in [-.95,.95]:ball((x,0,.6),(.22,.13,.025),'blue',2)
 elif name=='sandcastle':
  box((0,0,.25),(.8,.8,.5),'yellow')
  for x in [-.45,.45]:
   for y in [-.45,.45]:cyl((x,y,.35),.18,.7,'yellow',12);cyl((x,y,.8),.2,.25,'yellow',12,r2=0)
  box((0,-.41,.15),(.15,.02,.3),'soil')
 elif name=='balance_beam':
  box((0,0,.5),(3,.2,.2),'wood')
  for x in [-1,1]:box((x,0,.2),(.18,.6,.4),'red')
 elif name=='climbing_frame':
  for x in [-1,0,1]:
   for y in [-1,0,1]:beam((x,y,0),(x,y,2),.025,'blue')
  for z in [.4,.8,1.2,1.6,2]:
   for y in [-1,0,1]:beam((-1,y,z),(1,y,z),.025,'yellow')
   for x in [-1,0,1]:beam((x,-1,z),(x,1,z),.025,'red')
RECREATION=['swing_set','slide','seesaw','roundabout','basketball_hoop','soccer_goal','tennis_net','beach_umbrella','deck_chair','camping_tent','campfire','barbecue_grill','cooler_box','lifebuoy','surfboard','kayak','sandcastle','balance_beam','climbing_frame','picnic_canopy']

def vessel(r=.15,h=.15,mat='metal',bottom=None):
 rb=r*.8 if bottom is None else bottom;t=min(.012,r*.12);n=24;vs=[]
 for radius,z in [(rb,0),(r,h),(r-t,h),(rb-t,t)]:
  for i in range(n):a=i*math.tau/n;vs.append((radius*math.cos(a),radius*math.sin(a),z))
 fs=[]
 for ring_i in range(3):
  for i in range(n):j=(i+1)%n;fs.append((ring_i*n+i,ring_i*n+j,(ring_i+1)*n+j,(ring_i+1)*n+i))
 fs.append(tuple(reversed(range(n))));fs.append(tuple(range(3*n,4*n)));m=bpy.data.meshes.new('vessel');m.from_pydata(vs,[],fs);m.update();o=bpy.data.objects.new('vessel',m);bpy.context.collection.objects.link(o);return finish(o,'vessel',mat)
def kitchen(name):
 if name in ['saucepan','frying_pan','stockpot']:
  h=.06 if name=='frying_pan' else .25 if name=='stockpot' else .14;vessel(.18,h,'black' if name=='frying_pan' else 'metal')
  if name=='stockpot':
   for x in [-.22,.22]:ring((x,0,h*.7),.06,.013,'black',(math.pi/2,0,0))
  else:beam((.17,0,h*.8),(.48,0,h*.8+.03),.025,'black')
 elif name in ['kettle','teapot']:
  ball((0,0,.14),(.16,.16,.15),'metal' if name=='kettle' else 'white',2);cyl((0,0,.29),.08,.025,'black' if name=='kettle' else 'white');ball((0,0,.32),(.025,)*3,'black');beam((.1,0,.12),(.27,0,.23),.03,'metal' if name=='kettle' else 'white');ring((-.16,0,.19),.1,.02,'black',(math.pi/2,0,0))
 elif name=='toaster':
  box((0,0,.12),(.3,.2,.24),'white')
  for y in [-.05,.05]:box((0,y,.245),(.24,.025,.012),'black')
  box((.16,0,.12),(.03,.05,.035),'black')
 elif name=='microwave':
  box((0,0,.16),(.5,.35,.32),'white');box((-.045,-.182,.16),(.36,.02,.24),'black');box((-.045,-.195,.16),(.28,.01,.17),'glass')
  for z in [.1,.2]:o=cyl((.2,-.19,z),.027,.015,'metal');o.rotation_euler.x=math.pi/2
 elif name=='oven':
  box((0,0,.43),(.6,.6,.86),'white');box((0,-.31,.36),(.5,.025,.5),'black');box((0,-.33,.36),(.4,.01,.36),'glass');box((0,-.35,.61),(.4,.04,.025),'metal')
  for x in [-.16,.16]:
   for y in [-.16,.16]:cyl((x,y,.868),.1,.012,'black',24)
  for x in [-.2,-.07,.07,.2]:o=cyl((x,-.32,.76),.027,.025,'black');o.rotation_euler.x=math.pi/2
 elif name=='coffee_maker':
  box((0,0,.23),(.25,.28,.46),'black');box((0,-.06,.32),(.2,.2,.12),'metal');box((0,-.12,.03),(.24,.2,.04),'metal');vessel(.07,.12,'white');beam((0,-.08,.24),(0,-.08,.18),.012,'metal')
 elif name=='blender':
  cyl((0,0,.08),.11,.16,'white',20);cyl((0,0,.29),.09,.26,'glass',20,r2=.12);cyl((0,0,.44),.125,.035,'black',20);ring((.12,0,.29),.08,.015,'white',(math.pi/2,0,0))
 elif name=='cutting_board':box((0,0,.015),(.42,.28,.03),'wood');box((0,.19,.015),(.1,.12,.03),'wood')
 elif name=='knife':box((0,-.1,.02),(.035,.16,.04),'black');box((0,.1,.015),(.07,.24,.015),'metal')
 elif name=='spoon':beam((0,-.12,.015),(0,.07,.015),.012,'metal');ball((0,.12,.015),(.04,.06,.012),'metal',2)
 elif name=='fork':
  beam((0,-.12,.015),(0,.07,.015),.012,'metal');box((0,.08,.015),(.065,.025,.012),'metal')
  for x in [-.025,-.008,.008,.025]:box((x,.13,.015),(.008,.09,.01),'metal')
 elif name in ['bowl','fruit_bowl']:
  vessel(.18,.12,'white',.075)
  if name=='fruit_bowl':
   for x,y,c in [(-.07,0,'red'),(.07,0,'orange'),(0,.06,'leaf')]:ball((x,y,.12),(.065,.065,.06),c,2);beam((x,y,.17),(x+.005,y,.19),.005,'bark')
 elif name=='bread_loaf':
  ball((0,0,.12),(.16,.28,.12),'wood',3)
  for y in [-.13,0,.13]:box((0,y,.235),(.18,.015,.008),'white')
 elif name=='milk_carton':
  box((0,0,.13),(.12,.12,.26),'white');roof(.12,.12,.26,'blue');box((0,-.065,.14),(.1,.01,.14),'blue');text('MILK',(0,-.075,.14),.035)
 elif name=='egg_carton':
  box((0,0,.025),(.3,.2,.05),'wood')
  for x in [-.1,0,.1]:
   for y in [-.05,.05]:ball((x,y,.07),(.038,.038,.05),'white',2)
 elif name=='dish_rack':
  box((0,0,.015),(.4,.3,.03),'metal')
  for x in [-.17,.17]:beam((x,-.13,.03),(x,-.13,.12),.008);beam((x,.13,.03),(x,.13,.12),.008)
  for y in [-.13,.13]:beam((-.18,y,.12),(.18,y,.12),.008)
  for x in [-.13,-.065,0,.065,.13]:o=cyl((x,0,.12),.11,.012,'white',24);o.rotation_euler.y=math.pi/2
KITCHEN=['saucepan','frying_pan','stockpot','kettle','teapot','toaster','microwave','oven','coffee_maker','blender','cutting_board','knife','spoon','fork','bowl','fruit_bowl','bread_loaf','milk_carton','egg_carton','dish_rack']
EXPANSION={'transport':(TRANSPORT,transport),'buildings':(BUILDINGS,buildings),'recreation':(RECREATION,recreation),'kitchen':(KITCHEN,kitchen)}
GROUPS.update(EXPANSION)
if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else list(EXPANSION)
 for group in args:run(group)
