import { useSpring, animated } from '@react-spring/three'
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'

export const Box = ({ active, ...props }) => {
  const meshRef = useRef()

  const { scale } = useSpring({
    scale: active ? [0.4, 0.4, 0.4] : [0.8, 0.8, 0.8],
    config: { mass: 1, tension: 170, friction: 26 }
  })

  useFrame((state, delta) => {
    meshRef.current.rotation.y += delta
    meshRef.current.rotation.x += delta * 0.9
  })

  return (
    <animated.mesh {...props} ref={meshRef} scale={scale}>
      {active ? (
        <boxGeometry args={[1, 1, 1]} />
      ) : (
        <coneGeometry args={[1, 2, 3]} />
      )}
      <meshStandardMaterial color={'white'} roughness={0.8} />
    </animated.mesh>
  )
}
