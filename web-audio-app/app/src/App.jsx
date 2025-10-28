import { useState } from 'react';
import { RegisterForm } from './components/views/register';
import { LoginForm } from './components/views/login';
import { ForgotPasswordForm } from './components/views/forgot_password';
import { Navbar } from './components/buttons/navbar';

function App() {
  const [activeForm, setActiveForm] = useState(null);

  return (
    <>
      <Navbar setActiveForm={setActiveForm}/>
      <div>Welcome to my app 👹</div>

      <div>
        {!activeForm && (
          <p>Select "Join Us" in navbar to login or register!</p>
        )}

        {activeForm === 'register' && (
          <RegisterForm setActiveForm={setActiveForm} />
        )}
        {activeForm === 'login' && <LoginForm setActiveForm={setActiveForm} />}
        {activeForm === 'forgot-password' && (
          <ForgotPasswordForm setActiveForm={setActiveForm} />
        )}
      </div>
    </>
  );
}

export default App;
