<script>
  import * as THREE from "three";
  import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
  import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
  import { onMount } from "svelte";

  let container;
  let scene, camera, renderer, controls;

    // function loadModel(folder, filename) {
    // const path = `${folder}/${filename}`;
    // console.log("Loading:", path);

//     loader.load(
//       path,
//       (gltf) => {
//         // remove previous models
//         for (let i = scene.children.length - 1; i >= 0; i--) {
//           const obj = scene.children[i];
//           if (obj.type === "Group" || obj.type === "Mesh") scene.remove(obj);
//         }

//         const model = gltf.scene;
//         model.scale.set(1, 1, 1);
//         model.position.set(0, 0, 0);
//         scene.add(model);
//       },
//       (xhr) => {
//         console.log(`Loading ${(xhr.loaded / xhr.total) * 100}%`);
//       },
//       (error) => {
//         console.error("Error loading model:", error);
//       }
//     );
//   }

  onMount(() => {
    // Scene
    scene = new THREE.Scene();

    const w = window.innerWidth;
    const h = window.innerHeight;

    // Camera
    camera = new THREE.PerspectiveCamera(75, w / h, 0.1, 1000);
    camera.position.set(0, 1, 3);

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(w, h);
    container.appendChild(renderer.domElement);

    // Controls
    controls = new OrbitControls(camera, renderer.domElement);


    // Light
    const light = new THREE.PointLight(0xffffff, 100);
    light.position.set(3, 3, 3);
    scene.add(light);

    // GLTF model
    const loader = new GLTFLoader();
    loader.load("/models/guzheng-1k.glb", (gltf) => {
      scene.add(gltf.scene);
    });

    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }
    animate();
    
    return () => {
        renderer.dispose();
    };
  });
</script>


<div class="canvas-container" bind:this={container}>
    Loading...
</div>