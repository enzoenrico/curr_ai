import { Canvas, useFrame } from '@react-three/fiber'
import { useState, useRef, Suspense } from 'react'
import { AsciiRenderer, OrbitControls } from '@react-three/drei'
import { useSpring, animated } from '@react-spring/three'
import viteLogo from '/vite.svg'
import { FaSpinner } from 'react-icons/fa6'

function Box ({ active, ...props }) {
  const meshRef = useRef()

  const { scale } = useSpring({
    scale: active ? [0.4, 0.4, 0.4] : [0.8, 0.8, 0.8],
    config: { mass: 1, tension: 170, friction: 26 }
  })

  useFrame((state, delta) => (meshRef.current.rotation.y += delta))

  return (
    <animated.mesh {...props} ref={meshRef} scale={scale}>
      {active ? (
        <sphereGeometry args={[1, 32, 32]} />
      ) : (
        <boxGeometry args={[1, 1, 1]} />
      )}
      <meshStandardMaterial color={'white'} roughness={0.5} />
    </animated.mesh>
  )
}

function App () {
  const [active, setLoading] = useState(false)
  const [userInput, setUserInput] = useState<string>('')
  const [aiResponse, setAIResponse] = useState<string>('')

  const callAi = async () => {
    setLoading(true)
    try {
      console.log(userInput)
      setAIResponse('bonga bong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className='h-screen w-screen flex items-center justify-center relative'>
        <Canvas camera={{ position: [0, 1, 2] }}>
          <ambientLight position={[0, 1, 1]} intensity={0.3} />
          <spotLight position={[5, 1, 2]} intensity={0.4} color='#ffffff' />
          <Suspense fallback={<div>loading</div>}>
            <Box position={[0, 0, 0]} active={active} setActive={setLoading} />
          </Suspense>
          <AsciiRenderer fgColor='#8b0000' bgColor='black' />
          <OrbitControls />
        </Canvas>
        <div className='absolute bottom-5 w-full flex items-center justify-center gap-8'>
          <input
            type='text'
            placeholder='hello'
            className='w-3/5 p-1 px-4 rounded-full bg-red-600/40 border-2 text-white'
            onChange={e => setUserInput(e.target.value)}
          />
          <button
            type='button'
            className='bg-black border-2 border-white text-white p-2 rounded-xl'
            onClick={callAi}
          >
            Transform
          </button>
        </div>
        <div className='absolute top-5 text-white px-5'>
          {active || !aiResponse ? (
            <div className='animate-spin text-3xl'>
              <FaSpinner />
            </div>
          ) : (
            <p className='text-xl font-mono'>aiResponse</p>
          )}
        </div>
      </div>
    </>
  )
}

export default App
