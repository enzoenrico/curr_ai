import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Home } from './pages/Home'
import { Auth } from './pages/Auth'

function App () {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/auth' element={<Auth />} />
          <Route path='*' element={<div>404</div>} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
