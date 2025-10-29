import { useState } from 'react';
import { RegisterForm } from './components/views/register';
import { LoginForm } from './components/views/login';
import { ForgotPasswordForm } from './components/views/forgot_password';
import { Navbar } from './components/navbar';
import { useUser } from './hooks/user';

function App() {
  const [activeForm, setActiveForm] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [activeBar, setActiveBar] = useState('welcome');
  const { logout } = useUser();

  const handleLoginSuccess = userData => {
    setIsAuthenticated(true);
    setCurrentUser(userData);
    setActiveForm(null);
    setActiveBar('profile');
  };

  const handleLogout = async () => {
    setIsAuthenticated(false);
    setCurrentUser(null);
    await logout();
    setActiveBar('welcome');
  };

  return (
    <>
      <Navbar
        setActiveForm={setActiveForm}
        isAuthenticated={isAuthenticated}
        currentUser={currentUser}
        onLogout={handleLogout}
        activeBar={activeBar}
        setActiveBar={setActiveBar}
      />

      {/* ToDO: элемент приветствия будет только для гостевых пользователей*/}
      {!isAuthenticated ? (
        <>
          <div>Welcome to my app 👹</div>

          <div>
            {!activeForm && (
              <p>Select "Join Us" in navbar to login or register!</p>
            )}

            {activeForm === 'register' && (
              <RegisterForm setActiveForm={setActiveForm} />
            )}
            {activeForm === 'login' && (
              <LoginForm
                setActiveForm={setActiveForm}
                onLoginSuccess={handleLoginSuccess}
              />
            )}
            {activeForm === 'forgot-password' && (
              <ForgotPasswordForm setActiveForm={setActiveForm} />
            )}
          </div>
        </>
      ) : (
        <>
          <div>Welcome back, {currentUser?.username}!</div>
          {/* ToDO: элемент приветствия будет только для авторизованных пользователей*/}
        </>
      )}
    </>
  );
}

export default App;
