<script>

import { render } from "express/lib/response";
import { onMount } from "svelte";
import * as THREE from "three";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
// FOV, Aspect Ratio, near, far
const renderer = new THREE.WebGLRenderer();


renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );
</script>


