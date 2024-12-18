import { Canvas, useFrame } from '@react-three/fiber'
import { useState, useRef, Suspense, useEffect } from 'react'
import { AsciiRenderer, OrbitControls } from '@react-three/drei'
import { useSpring, animated } from '@react-spring/three'
import { FaSpinner } from 'react-icons/fa6'

function Box ({ active, ...props }) {
  const meshRef = useRef()

  const { scale } = useSpring({
    scale: active ? [0.4, 0.4, 0.4] : [0.8, 0.8, 0.8],
    config: { mass: 1, tension: 170, friction: 26 }
  })

  useFrame((state, delta) => {
    meshRef.current.rotation.y += delta
    meshRef.current.rotation.x += delta
  })

  return (
    <animated.mesh {...props} ref={meshRef} scale={scale}>
      {active ? (
        <torusGeometry args={[1, 0.3]} />
      ) : (
        <boxGeometry args={[1, 1, 1]} />
      )}
      <meshStandardMaterial color={'#ffffff'} roughness={0.5} />
    </animated.mesh>
  )
}

function Home () {
  const [active, setLoading] = useState(false)
  const [userInput, setUserInput] = useState<string>('')
  const [aiResponse, setAIResponse] = useState<string>('')

  useEffect(() => {
    console.log('ur on home')
  })

  const callAi = async () => {
    setLoading(true)
    try {
      console.log(userInput)
      setTimeout(() => {
        setAIResponse('bonga bong')
        setLoading(false)
      }, 2000)
    } catch (error) {
      console.error(error)
      setLoading(false)
    }
  }

  return (
    <>
      <div className='h-screen w-screen flex items-center justify-center relative'>
        <Canvas camera={{ position: [0, 1, 2] }}>
          <spotLight position={[-5, 0, -2]} intensity={0.7} color='#ffffff' />
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
          {/* implement framer motion text effect */}
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

export default Home
