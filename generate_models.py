import trimesh as m, numpy as np
from pathlib import Path
out=Path(__file__).parent/'public/models'; out.mkdir(parents=True,exist_ok=True)
def material(mesh,c):
 mesh.visual= m.visual.TextureVisuals(material=m.visual.material.PBRMaterial(baseColorFactor=c,roughnessFactor=.48,metallicFactor=.18 if c[0]>.8 and c[2]<.5 else 0)); return mesh
def ell(p,s,c):
 a=m.creation.icosphere(subdivisions=2);a.apply_scale(s);a.apply_translation(p);return material(a,c)
def lathe(rings,c,n=48):
 v=[];f=[]
 for y,rx,rz in rings:
  for j in range(n):
   t=j*2*np.pi/n; ripple=1+.045*np.cos(t*9);v.append([rx*np.cos(t)*ripple,y,rz*np.sin(t)*ripple])
 for i in range(len(rings)-1):
  for j in range(n):
   a=i*n+j;b=i*n+(j+1)%n;f.extend([[a,a+n,b],[b,a+n,b+n]])
 return material(m.Trimesh(v,f,process=False),c)
white=[.96,.94,.87,1]; gold=[.84,.61,.22,1]; skin=[.65,.39,.25,1]; hair=[.19,.10,.055,1]
for kind in ['miguel','jesus','angel']:
 scene=m.Scene(); parts=[]
 parts.append(lathe([(0,.01,.01),(.08,.48,.33),(.35,.42,.30),(.8,.34,.23),(1.15,.28,.19),(1.48,.36,.22),(1.64,.26,.17),(1.72,.13,.12)],white))
 parts.extend([ell([0,1.72,0],[.115,.17,.105],skin),ell([0,1.99,0],[.21,.28,.20],skin),ell([0,2.16,-.035],[.22,.15,.21],hair),ell([0,1.98,.19],[.033,.061,.048],skin)])
 for s in [-1,1]:
  parts.extend([ell([s*.083,2.045,.174],[.043,.021,.022],[.95,.93,.88,1]),ell([s*.083,2.045,.194],[.016,.017,.009],hair),ell([s*.20,1.99,0],[.04,.064,.033],skin)])
  arm=ell([s*.40,1.35,0],[.13,.37,.14],white);parts.append(arm);parts.append(ell([s*.47,1.0,.025],[.09,.14,.07],skin));parts.append(ell([s*.17,.08,.10],[.13,.075,.22],gold))
  if kind=='jesus':parts.append(ell([s*.19,1.94,-.07],[.07,.27,.12],hair))
 if kind=='jesus':parts.append(ell([0,1.825,.105],[.15,.12,.115],hair))
 parts.append(lathe([(1.12,.29,.20),(1.19,.30,.21)],gold if kind!='jesus' else [.59,.12,.13,1]))
 for i,a in enumerate(parts):scene.add_geometry(a,node_name=f'body_{i}')
 scene.export(out/f'{kind}.glb')
# feathered wing asset, origin at shoulder
scene=m.Scene()
for row in range(3):
 for i in range(12-row*2):
  a=ell([0,0,0],[.12-row*.014,.61-row*.09,.045], [ .98-row*.06,.97-row*.05,.92-row*.025,1]); angle=-.85-i*.055
  a.apply_transform(m.transformations.rotation_matrix(angle,[0,0,1]));a.apply_translation([.20+i*.105,.66-i*.061+row*.13,-row*.035]);scene.add_geometry(a)
scene.export(out/'wing.glb')
# pavilion with fluted columns, dome and finial
scene=m.Scene()
def box(p,s,c):
 a=m.creation.box(s);a.apply_translation(p);return material(a,c)
for p,s,c in [([0,.2,0],[6,.4,6],gold),([0,3,0],[3.6,5.2,3.6],white),([0,5.7,0],[6,.5,6],gold),([0,6.05,0],[5.6,.25,5.6],white)]:scene.add_geometry(box(p,s,c))
for x in [-2.45,2.45]:
 for z in [-2.45,0,2.45]:
  a=lathe([(.4,.39,.39),(.65,.39,.39),(.8,.26,.26),(5.1,.22,.22),(5.3,.4,.4),(5.6,.4,.4)],white);a.apply_translation([x,0,z]);scene.add_geometry(a)
scene.add_geometry(lathe([(6.15,2.6,2.6),(6.5,2.55,2.55),(7.1,2.2,2.2),(7.7,1.6,1.6),(8.2,.7,.7),(8.45,.12,.12)],gold));scene.add_geometry(ell([0,8.7,0],[.18,.35,.18],gold));scene.export(out/'pavilion.glb')
