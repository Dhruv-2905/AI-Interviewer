import React, { Suspense, useState, useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Environment, useGLTF } from '@react-three/drei';

function Avatar({ jawMovement, headNod }) {
  const gltf = useGLTF('/model.glb');
  const headRef = useRef();
  const faceMeshRef = useRef();

  // Find head bone and face mesh with morph targets
  useEffect(() => {
    console.log('Traversing avatar scene...');
    gltf.scene.traverse((child) => {
      if (child.isBone) {
        console.log('Bone found:', child.name);
        if (child.name === 'Head') {
          headRef.current = child;
          console.log('Selected head bone:', child.name);
        }
      }
      if (child.isMesh && child.morphTargetDictionary && child.name === 'Wolf3D_Head') {
        faceMeshRef.current = child;
        console.log('Selected face mesh:', child.name);
        console.log('Morph targets:', Object.keys(child.morphTargetDictionary));
      }
    });
  }, [gltf.scene]);

  // Animate mouth (morph target) and head
  useFrame(() => {
    // Lip syncing: Morph target-based
    if (faceMeshRef.current && faceMeshRef.current.morphTargetDictionary) {
      const mouthOpenIndex = faceMeshRef.current.morphTargetDictionary['mouthOpen'];
      if (mouthOpenIndex !== undefined) {
        faceMeshRef.current.morphTargetInfluences[mouthOpenIndex] = jawMovement.current * 1.0; // Adjust intensity
      }
    }

    // Head nodding: Multi-directional
    if (headRef.current) {
      const nodAmount = headNod.current;
      headRef.current.rotation.x = nodAmount * 0.2 + Math.sin(Date.now() * 0.002) * nodAmount * 0.1; // Forward/back with oscillation
      headRef.current.rotation.y = nodAmount * 0.15 + Math.cos(Date.now() * 0.003) * nodAmount * 0.1; // Side-to-side with oscillation
      headRef.current.rotation.z = nodAmount * 0.1 + Math.sin(Date.now() * 0.004) * nodAmount * 0.05; // Slight tilt
    }
  });

  return (
    <primitive object={gltf.scene} scale={1.5} position={[0, -1.5, 0]} />
  );
}

function App() {
  const [speech, setSpeech] = useState('');
  const [voice, setVoice] = useState(null);
  const jawMovement = useRef(0);
  const headNod = useRef(0);

  // Load female voice
  useEffect(() => {
    const loadVoices = () => {
      const voices = window.speechSynthesis.getVoices();
      // Prefer female voices (common female voice names or language-specific)
      const femaleVoice = voices.find((v) =>
        v.name.toLowerCase().includes('female') ||
        v.name.match(/samantha|zira|tessa|ava|allison|susan|karen|moira|veena|victoria/i)
      ) || voices[0]; // Fallback to default voice
      if (femaleVoice) {
        setVoice(femaleVoice);
        console.log('Selected voice:', femaleVoice.name);
      }
    };
    loadVoices();
    window.speechSynthesis.onvoiceschanged = loadVoices;
    return () => {
      window.speechSynthesis.onvoiceschanged = null;
    };
  }, []);

  const handleSpeak = (e) => {
    e.preventDefault();
    if (!speech.trim()) return;

    const utterance = new SpeechSynthesisUtterance(speech);
    if (voice) utterance.voice = voice;
    utterance.rate = 0.8; // Slower, more natural speech

    // Animate mouth and head during speech
    utterance.onstart = () => {
      jawMovement.current = 0.3; // Initial mouth open
      headNod.current = 0.2; // Initial head tilt
    };

    utterance.onboundary = (event) => {
      if (event.name === 'word') {
        // Lip sync: Mouth movement per word
        jawMovement.current = 0.7; // Open mouth
        setTimeout(() => {
          jawMovement.current = 0.2; // Close slightly
        }, 120);

        // Head nod: Subtle nod per word
        headNod.current = Math.random() * 0.5 + 0.2; // Random nod intensity
        setTimeout(() => {
          headNod.current = 0.2; // Maintain slight nod
        }, 300);
      } else if (event.name === 'sentence') {
        // Head nod: Larger nod at sentence start
        headNod.current = 0.6;
        setTimeout(() => {
          headNod.current = 0.2; // Maintain slight nod
        }, 500);
      }
    };

    utterance.onend = () => {
      jawMovement.current = 0; // Reset mouth
      headNod.current = 0; // Reset head
    };

    window.speechSynthesis.speak(utterance);
    setSpeech('');
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 relative">
        <Canvas camera={{ position: [0, 1.5, 2] }} className="absolute inset-0">
          <ambientLight intensity={0.6} />
          <directionalLight position={[2, 5, 2]} intensity={1} />
          <Suspense fallback={null}>
            <Avatar jawMovement={jawMovement} headNod={headNod} />
            <Environment preset="sunset" />
            <OrbitControls />
          </Suspense>
        </Canvas>
      </div>
      <div className="bg-white p-4 shadow-md">
        <form onSubmit={handleSpeak} className="flex gap-2">
          <input
            type="text"
            value={speech}
            onChange={(e) => setSpeech(e.target.value)}
            placeholder="Type what the avatar should say..."
            className="flex-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          >
            Speak
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;