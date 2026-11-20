// Ground-level obstacle footprints; player radius in world units.
type Rect = [number,number,number,number];
const obstacles: Rect[]=[];
const box=(x:number,z:number,w:number,d:number)=>obstacles.push([x-w/2,z-d/2,x+w/2,z+d/2]);
for(const s of [-1,1]){
 box(s*75,-160,3,460); box(s*12,13,15,5); box(s*15,13,5.4,5.4);
 for(let i=0;i<24;i++)box(s*75,60-i*19,5.4,5.4);
 for(let i=0;i<28;i++)box(s*(9+i%2*5),45-i*16,1.5,1.5);
 for(let i=0;i<20;i++)box(s*53,32-i*20,6,6);
 for(let i=0;i<46;i++)box(s*6.4,45-i*9,.65,.65);
 box(s*17,-365,15,13);box(s*19,-369,5.4,5.4);
}
box(39,-170,3,3);box(0,-380,19,14);box(0,-381,5.4,5.4);
box(0,-359,6,4.6);
export function blocked(x:number,z:number){const r=.42;return obstacles.some(([a,b,c,d])=>{const dx=x-Math.max(a,Math.min(c,x)),dz=z-Math.max(b,Math.min(d,z));return dx*dx+dz*dz<r*r;});}
export function walk(x:number,z:number,dx:number,dz:number):[number,number]{const n=Math.max(1,Math.ceil(Math.hypot(dx,dz)/.15));for(let i=0;i<n;i++){const nx=Math.max(-71,Math.min(71,x+dx/n)),nz=Math.max(-380,Math.min(60,z+dz/n));if(!blocked(nx,z))x=nx;if(!blocked(x,nz))z=nz;}return [x,z];}
