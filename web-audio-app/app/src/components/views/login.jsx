import { useState } from 'react';
import { ConfirmLogin } from '../buttons/auth/confirm';
import { GithubButton } from '../buttons/social';
import '../../style/login.css';

export function LoginForm({ setActiveForm }) {
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
        <form onSubmit={handlSubmit}>
          <label>Email or username</label>
          <input
            type="text"
            placeholder="bruh@example.com or bruh1234"
            name="login"
            value={formData.login}
            onChange={handleChange}
          />

          <label>Password</label>
          <input
            type="password"
            placeholder="enter your password"
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
          Forgot password?
        </a>

        <ConfirmLogin formData={formData} />

        <div className="github-div">
          <p>
            Do you have a GitHub account? Great! <br />
            You can sign in with it:
          </p>
          <GithubButton />
        </div>

        <a
          className="link"
          href="#register"
          onClick={() => setActiveForm('register')}
        >
          Don't have account? Register
        </a>
      </div>

      {/* TODO: СДЕЛАТЬ ЧТО-ТО С ЭТОЙ КНОПКОЙ, как тебя ведать....*/}
      <div className='back-div'>
        <a href="#home" onClick={() => setActiveForm(null)}>← Back to Home</a>
      </div>
    </>
  );
}
