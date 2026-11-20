import React,{useMemo} from 'react';
import {useGLTF} from '@react-three/drei';
import * as T from 'three';
export function Asset({name,mirror=false}:{name:string,mirror?:boolean}){const {scene}=useGLTF(`/models/${name}.glb`);const model=useMemo(()=>{const a=scene.clone(true);a.traverse(o=>{if(o instanceof T.Mesh){o.castShadow=true;o.receiveShadow=true}});return a},[scene]);return <primitive object={model} scale={[mirror?-1:1,1,1]}/>}
