import { useState } from 'react';
import '../../style/auth/forgot-password.css';
import '../../style/auth/login.css';
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
          <label>Введите вашу почту</label>
          <input
            type="email"
            placeholder="введите почту"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
        </form>

        <ForgotPasswordRequest formData={formData} />

        <a href="#login" className='link'
        onClick={() => setActiveForm('login')}>← Вернуться к Логину</a>
      </div>
    </>
  );
}
