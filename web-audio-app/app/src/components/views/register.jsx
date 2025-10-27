import { ConfirmRegistration } from '../buttons/auth/confirm';
import { GithubButton } from '../buttons/social';
import '../../style/forms.css';
import { useState } from 'react';

export function RegisterForm({setActiveForm}) {
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

  const handlSubmit = (e) => {
    e.preventDefault();
  };

  return (
    <>
      <div>
        <form onSubmit={handlSubmit}>
          <label>Email: </label>
          <input
            type="text"
            placeholder="Enter your email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />

          <label>Username: </label>
          <input
            type="text"
            placeholder="Enter your username"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />

          <label>Password: </label>
          <input
            type="password"
            placeholder="Create password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />

          <label>Repeat password: </label>
          <input
            type="password"
            placeholder="Repeat password"
            name="passwordConfirm"
            value={formData.passwordConfirm}
            onChange={handleChange}
          />

          <h5>I have read the user agreement</h5>

        </form>
        
        <ConfirmRegistration formData={formData} />

        <div>
          <h3>Or register with other social:</h3>
          <GithubButton />
        </div>

        <div>
            <button onClick={() => setActiveForm(null)}>Back</button>
            <button onClick={() => setActiveForm('login')}>Already have an account? Login</button>
        </div>
      </div>
    </>
  );
}
