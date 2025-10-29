import { useState } from 'react';
import '../../style/authforgot-password.css';
import '../../style/authlogin.css';
import { ForgotPasswordRequest } from '../buttons/auth/confirm';

export function ForgotPasswordForm({setActiveForm}) {
  const [formData, setFormData] = useState({
    email: '',
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
      <div className='main-div-forgot'>
        <form className="form" onSubmit={handlSubmit}>
          <label>Enter your email:</label>
          <input
            type="email"
            placeholder="Enter your email or username"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
        </form>

        <ForgotPasswordRequest formData={formData} />

        <a href="#login" className='link'
        onClick={() => setActiveForm('login')}>← Back to Login</a>
      </div>
    </>
  );
}
