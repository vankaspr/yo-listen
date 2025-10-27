import { RegisterForm } from '../views/register';
import { useState } from 'react';

export function RegisterButton() {
  const [showForm, setShowForm] = useState(false);

  const handleOpen = () => {
    setShowForm(true);
    console.log('register form show!');
  };

  //const handleClose = () => {
  //  setShowForm(false);
  //  console.log('register form close!');
  //};

  return (
    <>
      {!showForm && <button onClick={handleOpen}>Register</button>}
      {showForm && <RegisterForm/>}
    </>
  );
}
