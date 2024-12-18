import { useState } from 'react'
import { ModelCanvas } from '../components/ModelCanvas'
import { FaSpinner } from 'react-icons/fa6'

export const Home = () => {
  const [active, setLoading] = useState(false)
  const [userInput, setUserInput] = useState<string>('')
  const [aiResponse, setAIResponse] = useState<string>('')

  const callAi = async () => {
    setLoading(true)
    try {
      console.log(userInput)
      await new Promise(resolve => setTimeout(resolve, 2000))
      setAIResponse('bonga bong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className='h-screen w-screen flex items-center justify-center relative'>
        <ModelCanvas loading={active} setLoading={setLoading} />
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
