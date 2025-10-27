import { useState } from 'react';
import { RegisterForm } from './components/views/register';
import { LoginForm } from './components/views/login';
import { ForgotPasswordForm } from './components/views/forgot_password';

function App() {
  const [activeForm, setActiveForm] = useState(null);

  return (
    <>
      <div>Welcome to my app 👹</div>

      <div>
        {!activeForm && (
          <div>
            <button onClick={() => setActiveForm('register')}>Register</button>
            <button onClick={() => setActiveForm('login')}>Login</button>
          </div>
        )}

        {activeForm === 'register' && <RegisterForm setActiveForm={setActiveForm}/>}
        {activeForm === 'login' && <LoginForm setActiveForm={setActiveForm}/>}
        {activeForm === 'forgot-password' && <ForgotPasswordForm setActiveForm={setActiveForm}/>}
      </div>
    </>
  );
}

export default App;
