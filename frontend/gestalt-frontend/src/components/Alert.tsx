import React, { ReactNode } from 'react'

interface Props{
    children:ReactNode
    onClick: () => void;
}
const Alert = ({children, onClick}:Props) => {
  return (
    <>
    <div className='alert alert-primary alert-dismissible' onClick={onClick}>{children}
    <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
   
    </>
  )
}

export default Alert