import { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export const ProtectedRoute = ({ children }: { children: ReactNode }) => {
  const { isAuthed } = useAuth()
  return isAuthed ? children : <Navigate to='/auth' />
}
