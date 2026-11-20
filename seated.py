import trimesh as m, numpy as np
from pathlib import Path
# Reuse the original head and facial geometry; sculpt a seated robe and arms.
source=m.load('public/models/jesus.glb',force='scene'); scene=m.Scene()
for name in source.graph.nodes_geometry:
 mat,g=source.graph[name]; a=source.geometry[g].copy();a.apply_transform(mat)
 if a.bounds[0,1]>1.54:
  a.apply_translation([0,-.49,0]);scene.add_geometry(a)
white=[.96,.94,.87,1];skin=[.65,.39,.25,1];gold=[.84,.61,.22,1]
def ell(p,s,c):
 a=m.creation.icosphere(subdivisions=3);a.apply_scale(s);a.apply_translation(p);a.visual=m.visual.TextureVisuals(material=m.visual.material.PBRMaterial(baseColorFactor=c,roughnessFactor=.6));scene.add_geometry(a)
ell([0,.66,0],[.34,.54,.24],white);ell([0,.10,.25],[.44,.2,.52],white)
for s in [-1,1]:
 ell([s*.24,-.23,.54],[.23,.48,.23],white);ell([s*.24,-.65,.66],[.13,.09,.23],gold)
 ell([s*.38,.65,0],[.13,.3,.14],white);ell([s*.43,.34,.25],[.12,.14,.32],white);ell([s*.43,.34,.54],[.095,.08,.13],skin)
ell([0,.41,0],[.35,.07,.25],[.59,.12,.13,1]);scene.export('public/models/jesus-seated.glb')
# Apply HDR white and gold clothing after exporting (keeps face/hair unchanged).
import json, struct
p=Path('public/models/jesus-seated.glb'); b=p.read_bytes(); n=struct.unpack_from('<I',b,12)[0]; j=json.loads(b[20:20+n]); rest=b[20+n:]
for mat in j['materials']:
    rgb=mat['pbrMetallicRoughness']['baseColorFactor'][:3]
    white_robe=rgb[0]>.95 and rgb[1]>.93 and rgb[2]>.85
    trim=rgb[0]>.8 and .5<rgb[1]<.7 and rgb[2]<.3 or rgb[0]>.5 and rgb[1]<.2 and rgb[2]<.2
    if white_robe or trim:
        mat['pbrMetallicRoughness'].update(baseColorFactor=[1,.98,.92,1] if white_robe else [1,.79,.32,1],metallicFactor=0,roughnessFactor=.55)
        mat['emissiveFactor']=[1,.96,.84] if white_robe else [.8,.49,.14]
        mat['extensions']={'KHR_materials_emissive_strength':{'emissiveStrength':1.6 if white_robe else .85}}
j.setdefault('extensionsUsed',[]).append('KHR_materials_emissive_strength'); raw=json.dumps(j,separators=(',',':')).encode();raw+=b' '*(-len(raw)%4);p.write_bytes(struct.pack('<4sIIII',b'glTF',2,20+len(raw)+len(rest),len(raw),0x4e4f534a)+raw+rest)
