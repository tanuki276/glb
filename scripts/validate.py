"""Dependency-free GLB container / buffer / accessor / geometry checks."""
import json,struct,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SIZES={5120:1,5121:1,5122:2,5123:2,5125:4,5126:4};WIDTH={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
count=0;total_tri=0
for path in sorted((ROOT/'assets').rglob('*.glb')):
 data=path.read_bytes();magic,version,length=struct.unpack_from('<4sII',data);assert magic==b'glTF' and version==2 and length==len(data),path
 n,kind=struct.unpack_from('<II',data,12);assert kind==0x4E4F534A;g=json.loads(data[20:20+n]);off=20+n;bn,bkind=struct.unpack_from('<II',data,off);assert bkind==0x004E4942;binary=data[off+8:off+8+bn];assert len(binary)==bn
 assert g['asset']['version']=='2.0';assert len(g['buffers'])==1 and 'uri' not in g['buffers'][0];assert g['buffers'][0]['byteLength']<=bn
 assert not g.get('animations') and not g.get('cameras');assert g.get('meshes') and g.get('materials')
 for v in g['bufferViews']:assert v.get('byteOffset',0)+v['byteLength']<=bn
 def values(a):
  v=g['bufferViews'][a['bufferView']];size=SIZES[a['componentType']]*WIDTH[a['type']];stride=v.get('byteStride',size);start=v.get('byteOffset',0)+a.get('byteOffset',0);assert a.get('byteOffset',0)+(a['count']-1)*stride+size<=v['byteLength']
  fmt={5126:'f',5125:'I',5123:'H',5121:'B',5122:'h',5120:'b'}[a['componentType']];return [struct.unpack_from('<'+fmt*WIDTH[a['type']],binary,start+i*stride) for i in range(a['count'])]
 for a in g['accessors']:
  vals=values(a);assert all(math.isfinite(x) for row in vals for x in row),path
 for mesh in g['meshes']:
  for p in mesh['primitives']:
   assert p.get('mode',4)==4;pos=g['accessors'][p['attributes']['POSITION']];idx=g['accessors'][p['indices']];assert idx['count']%3==0;assert max(x[0] for x in values(idx))<pos['count'];total_tri+=idx['count']//3
   assert all(a<=b for a,b in zip(pos['min'],pos['max']))
 count+=1
print(f'PASS: {count} GLBs; {total_tri:,} triangles; embedded buffers, valid indices, finite accessors')
