import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Home } from './pages/Home'
import { Auth } from './pages/Auth'
import { AuthProvider } from './context/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'

function App () {
  return (
    <>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route
              path='/'
              element={
                <ProtectedRoute>
                  <Home />
                </ProtectedRoute>
              }
            />
            <Route path='/auth' element={<Auth />} />
            <Route path='*' element={<div>404</div>} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </>
  )
}

export default App
