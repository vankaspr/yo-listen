import { useState } from 'react';
import { ConfirmLogin } from '../buttons/auth/confirm';
import { GithubButton } from '../buttons/social';
import '../../style/forms.css';

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
      <div>
        <form onSubmit={handlSubmit}>
          <label>Email or username:</label>
          <input
            type="text"
            placeholder="Enter your email or username"
            name="login"
            value={formData.login}
            onChange={handleChange}
          />

          <label>Password:</label>
          <input
            type="password"
            placeholder="Enter your password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </form>

        <button onClick={() => setActiveForm('forgot-password')}>
          Forgot password?
        </button>

        <ConfirmLogin formData={formData} />

        <div>
          <h3>Or login with other social:</h3>
          <GithubButton />
        </div>

        <div>
          <button onClick={() => setActiveForm(null)}>Back</button>
          <button onClick={() => setActiveForm('register')}>
            Don't have account? Register
          </button>
        </div>
      </div>
    </>
  );
}
