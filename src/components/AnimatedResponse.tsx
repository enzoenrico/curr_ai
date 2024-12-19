import { motion, useMotionValue, useTransform, animate } from 'framer-motion'
import { FC, useEffect } from 'react'

const cursorVariants = {
  blinking: {
    opacity: [0, 0, 1, 1],
    transition: {
      duration: 1,
      repeat: Infinity,
      repeatDelay: 0,
      ease: 'linear',
      times: [0, 0.5, 0.5, 1]
    }
  }
}

export const AnimatedResponse: FC<{ text: string }> = ({ text }) => {
  const count = useMotionValue(0)
  const rounded = useTransform(count, Math.round)
  const displayText = useTransform(rounded, latest => text.slice(0, latest))

  useEffect(() => {
    const controls = animate(count, text.length, {
      type: 'tween',
      duration: 1,
      ease: 'easeOut'
    })

    return controls.stop
  }, [count, text])

  return (
    <span className=''>
    <motion.span
      initial={{ color: '#ff0000' }}
      animate={{ color: '#ffffff' }}
      transition={{ duration: 2}}
    >
      {displayText}
    </motion.span>
      <motion.div
        variants={cursorVariants}
        animate='blinking'
        className='inline-block h-6 w-2 translate-y-1 bg-white ml-1'
      />
    </span>
  )
}
