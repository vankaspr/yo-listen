import { API_ENDPOINTS } from '../../../api/path';
import { useUser } from '../../../hooks/user';

export function ConfirmRegistration({ formData }) {
  const handleClick = async () => {
    try {
      // check if all field wad filled:
      if (!formData.email || !formData.password || !formData.username) {
        alert('Please fill all fields');
        return;
      }

      // password validation:
      if (formData.password != formData.passwordConfirm) {
        alert("Passwords don't match");
        return;
      }

      const response = await fetch(API_ENDPOINTS.AUTH.REGISTER, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: formData.email,
          username: formData.username,
          password: formData.password,
        }),
      });

      // here will be real notifications in the form of components:
      if (response.ok) {
        alert(
          "We've sent you an email so you can confirm your account.Please check it and follow the instructions in the email."
        );
      } else {
        alert('Error. Something was wrong...');
      }

      console.log('Registration succesfull: ', response.data);
    } catch (error) {
      console.log('Error response:', error.response?.data);
    }
  };

  return <button onClick={handleClick}>Continue</button>;
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
        {loading ? 'Loading...' : 'Continue'}
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
      <button onClick={handleClick}>Continue</button>
    </>
  );
}
