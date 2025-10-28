import { ConfirmRegistration } from '../buttons/auth/confirm';
import { GithubButton } from '../buttons/social';
import '../../style/register.css';
import '../../style/login.css';
import { useState } from 'react';

export function RegisterForm({ setActiveForm }) {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    passwordConfirm: '',
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
      <div className="main-register-div">
        <form className="form-register" onSubmit={handlSubmit}>
          <label>Email </label>
          <input
            type="text"
            placeholder="Enter your email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />

          <label>Create unique username </label>
          <input
            type="text"
            placeholder="Enter your username"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />

          <label>Password </label>
          <input
            type="password"
            placeholder="Create password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
          <span>
            The password must be at least 8 characters long and contain at least
            one number, one uppercase letter, and one special character. Please
            do not use your personal information as your password.
          </span>

          <label>Repeat password </label>
          <input
            type="password"
            placeholder="Repeat password"
            name="passwordConfirm"
            value={formData.passwordConfirm}
            onChange={handleChange}
          />

          <div className="checkbox-div">
            <input type="checkbox" />
            <span>
              I have read and agree to the{' '}
              <a className="link" href="#terms-of-service">Terms of Service</a>
            </span>
          </div>
        </form>

        <ConfirmRegistration formData={formData} />

        <div className="github-div">
          <p>
            Do you have a GitHub account? Great! <br />
            You can sign in with it!
          </p>
          <GithubButton />
        </div>
        <a
          className="link"
          href="#register"
          onClick={() => setActiveForm('login')}
        >
          Already have an account? Login.
        </a>
      </div>
      <div className="back-div">
        <a href="#home" onClick={() => setActiveForm(null)}>
          ← Back to Home
        </a>
      </div>
    </>
  );
}
