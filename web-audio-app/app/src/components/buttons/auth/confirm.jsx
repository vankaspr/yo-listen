import { useState } from 'react';
import { API_ENDPOINTS } from '../../../api/path';
import { useUser } from '../../../hooks/user';

export function ConfirmRegistration({
  formData,
  isTermsAccepted,
  setErrors,
  onSuccess,
}) {
  const [isLoading, setIsLoading] = useState(false);
  const handleClick = async () => {

    const newErrors = {};

    // check if all field wad filled:
    if (!formData.email) newErrors.email = 'Заполните поле почты!';
    if (!formData.username) newErrors.username = 'Заполните поле никнейм!';
    if (!formData.password) newErrors.password = 'Заполните поле пароля!';
    if (!formData.passwordConfirm)
      newErrors.passwordConfirm = 'Заполните поле подтверждения пароля!';

    // password validation:
    if (formData.password != formData.passwordConfirm) {
      newErrors.passwordConfirm = 'Пароли не совпадают';
    }

    // check if click on checkbox
    if (!isTermsAccepted) {
      newErrors.terms =
        'Чтобы продолжить регистрацию необходимо принять пользовательское соглашение';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);

      const shakeFields = Object.keys(newErrors);
      shakeFields.forEach(field => {
        const input = document.querySelector(`[name="${field}"]`);
        if (input) {
          input.classList.add('shake-animation');
          setTimeout(() => input.classList.remove('shake-animation'), 500);
        }
      });

      return;
    }

    await sendRegistrationRequest();
  };

  const sendRegistrationRequest = async () => {
    setIsLoading(true);

    try {
      const response = await fetch(API_ENDPOINTS.AUTH.REGISTER, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: formData.email,
          username: formData.username,
          password: formData.password,
        }),
      });

      // будет отправлено письмо на почту + таймер
      if (response.ok) {
        onSuccess();
      } else {
        const errorData = await response.json();
        setErrors({
          submit: errorData.message || 'Произошла ошибка при регистрации, возможно никнейм уже занят',
        });
      }
      console.log('Успешно зарегистрировались!: ', response.data);
    } catch (error) {
      console.log('Ошибка:', error);
      setErrors({
        submit: 'Ошибка сети. Поробуйте ещё раз.',
      });
    } finally {
      setIsLoading(false);
    }
  };


  return (
    
    <button 
    onClick={handleClick}
    disabled={isLoading}
    >
      {isLoading ? 'Регистрируем...' : 'Продолжить'}
    </button>
    
  );
}

export function ConfirmLogin({ formData, onLoginSuccess }) {
  const { getCurrentUser, loading, error } = useUser();
  const handleClick = async () => {
    try {
      // check if all field wad filled:
      if (!formData.login || !formData.password) {
        alert('Please fill all fields');
        return;
      }

      const response = await fetch(API_ENDPOINTS.AUTH.LOGIN, {
        // form data
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          login: formData.login,
          password: formData.password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const accessToken = data.access_token || data.token;

        if (!accessToken) {
          throw new Error('No access token received');
        }

        localStorage.setItem('access_token', accessToken);
        const userData = await getCurrentUser(accessToken);
        onLoginSuccess(userData);
      }

      console.log('Login succesfull: ', response.data);
    } catch (error) {
      console.log('Error response:', error.response?.data);
      alert(error.message || 'Login failed. Please try again.');
    }
  };
  return (
    <>
      <button onClick={handleClick} disabled={loading}>
        {loading ? 'Обрабатываем...' : 'Продолжить'}
      </button>
      {error && <p className="error">{error}</p>}
    </>
  );
}

export function ForgotPasswordRequest({ formData }) {
  const handleClick = async () => {
    try {
      if (!formData.email) {
        alert('Please fill all fields');
        return;
      }

      const response = await fetch(API_ENDPOINTS.AUTH.FORGOT_PASSWORD, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: formData.email }),
      });

      if (response.ok) {
        // window.location.href -> login
        alert(
          "We've sent you an email so you can confirm your account.Please check it and follow the instructions in the email."
        );
      } else {
        alert('Error. Something was wrong...');
      }
    } catch (error) {
      console.log('Error response:', error.response?.data);
    }
  };
  return (
    <>
      <button onClick={handleClick}>Продолжить</button>
    </>
  );
}
