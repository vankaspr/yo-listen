import { useState } from 'react';
import { ConfirmLogin } from '../buttons/auth/confirm';
import { GithubButton } from '../buttons/social';
import '../../style/auth/login.css';

export function LoginForm({ setActiveForm, onLoginSuccess }) {
  const [formData, setFormData] = useState({
    login: '',
    password: '',
  });

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handlSubmit = e => {
    e.preventDefault();
  };

  return (
    <>
      <div className="main-div">
        <form className="form" onSubmit={handlSubmit}>
          <label>Почта или ваш никнейм</label>
          <input
            type="text"
            placeholder="bruh@example.com или bruh1234"
            name="login"
            value={formData.login}
            onChange={handleChange}
          />

          <label>Пароль</label>
          <input
            type="password"
            placeholder="введите ваш пароль"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </form>

        <a
          className="link"
          href="#forgot-password"
          onClick={() => setActiveForm('forgot-password')}
        >
          Забыли пароль?
        </a>

        <ConfirmLogin 
        formData={formData} 
        onLoginSuccess={onLoginSuccess}
        />

        <div className="github-div">
          <p>
            У вас есть аккаунт на GitHub? Супер!<br />
            Можете войти через него:
          </p>
          <GithubButton />
        </div>

        <a
          className="link"
          href="#register"
          onClick={() => setActiveForm('register')}
        >
          Ещё нет аккаунта? Зарегистрируйтесь.
        </a>
      </div>

      <div className='back-div'>
        <a href="#home" onClick={() => setActiveForm(null)}>← Вернуться на Главную страницу</a>
      </div>
    </>
  );
}
