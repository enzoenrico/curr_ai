import { Canvas } from '@react-three/fiber'
import { AsciiRenderer } from '@react-three/drei'
import { Box } from '../components/Box'
import { Suspense } from 'react'
import { FaSpinner } from 'react-icons/fa6'

export const ModelCanvas = ({ loading, setLoading }) => {
  return (
    <Canvas camera={{ position: [0, 1, 2] }}>
      {/* <ambientLight position={[1, 1, 2]} intensity={0.3} /> */}
      {/* <spotLight position={[3, 1, 2]} intensity={0.25} color='#ffffff' /> */}
      <Suspense
        fallback={
          <div className='animate-spin text-3xl'>
            <FaSpinner />
          </div>
        }
      >
        <Box position={[0, 0, 0]} active={loading} setActive={setLoading} />
      </Suspense>
      <AsciiRenderer fgColor='#8b0000' bgColor='black' />
      {/* <OrbitControls /> */}
    </Canvas>
  )
}
