
import { API_ENDPOINTS } from '../../api/path';

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

export function ConfirmLogin({ formData }) {
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
        alert("Login succesfull!")
        // window.location.href -> profile (/api/user/me)
      } else {
        alert('Error. Something was wrong...');
      }

      console.log('Login succesfull: ', response.data);
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
