import { ConfirmRegistration } from '../buttons/auth/confirm';
import { GithubButton } from '../buttons/social';
import { EmailSentMessage } from '../buttons/auth/email';
import '../../style/auth/register.css';
import '../../style/auth/login.css';
import { useState } from 'react';

export function RegisterForm({ setActiveForm }) {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    passwordConfirm: '',
  });

  const [errors, setErrors] = useState({});
  const [isTermsAccepted, setIsTermsAccepted] = useState(false);
  const [isRegistrationComplete, setIsRegistrationComplete] = useState(false);

  const handleSuccess = () => {
    setIsRegistrationComplete(true);
  };

  if (isRegistrationComplete) {
    // 🫸 TODO: компонент уведомления об отправке письма 
    return <EmailSentMessage email={formData.email} />;
  }

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));

    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleTermsChange = e => {
    setIsTermsAccepted(e.target.checked);
    if (errors.terms) {
      setErrors([
        prev => {
          const newErrors = { ...prev };
          delete newErrors.terms;
          return newErrors;
        },
      ]);
    }
  };

  const handlSubmit = e => {
    e.preventDefault();
  };

  return (
    <>
      <div className="form-errors-wrapper">
        <div className="main-register-div">
          <form className="form-register" onSubmit={handlSubmit}>
            <label>Почта </label>
            <input
              type="text"
              placeholder="введите почту"
              name="email"
              value={formData.email}
              onChange={handleChange}
            />

            <label>Придумайте уникальный никнейм </label>
            <input
              type="text"
              placeholder="введите никнейм"
              name="username"
              value={formData.username}
              onChange={handleChange}
            />

            <label>Придумайте пароль </label>
            <input
              type="password"
              placeholder="введите пароль"
              name="password"
              value={formData.password}
              onChange={handleChange}
            />
            <span>
              Пароль должен быть не менее 8 символов и содержать хотя бы одну
              цифру, одну заглавную букву и один специальный символ.
            </span>

            <label>Повторите пароль</label>
            <input
              type="password"
              placeholder="введите пароль"
              name="passwordConfirm"
              value={formData.passwordConfirm}
              onChange={handleChange}
            />

            {/* checkbox terms of privicy */}
            <div className="checkbox-div">
              <input
                type="checkbox"
                checked={isTermsAccepted}
                onChange={handleTermsChange}
              />
              <span>
                Я прочитал(а){' '}
                <a className="link" href="#terms-of-service">
                  пользовательское соглашение
                </a>
              </span>
            </div>
          </form>

          {/*TODO: визуальная обработка ошибок */}
          <ConfirmRegistration
            formData={formData}
            setErrors={setErrors}
            isTermsAccepted={isTermsAccepted}
            onSuccess={handleSuccess}
          />

          <div className="github-div">
            <p>
              У вас есть аккаунт на GitHub? Отлично! <br />
              Вы можете зарегистрироваться с ним:
            </p>
            <GithubButton />
          </div>
          <a
            className="link"
            href="#register"
            onClick={() => setActiveForm('login')}
          >
            Уже есть аккаунт? Залогиньтесь.
          </a>
        </div>

        {Object.keys(errors).length > 0 && (
          <div className="error-container">
            {errors.email && (
              <div className="error-message">📧 {errors.email}</div>
            )}
            {errors.username && (
              <div className="error-message">👤 {errors.username}</div>
            )}
            {errors.password && (
              <div className="error-message">🔒 {errors.password}</div>
            )}
            {errors.passwordConfirm && (
              <div className="error-message">🔒 {errors.passwordConfirm}</div>
            )}
            {errors.terms && (
              <div className="error-message">📄 {errors.terms}</div>
            )}
            {errors.submit && (
              <div className="error-message submit-error">
                ⚠️ {errors.submit}
              </div>
            )}
          </div>
        )}
      </div>

      <div className="back-div">
        <a href="#home" onClick={() => setActiveForm(null)}>
          ← Вернуться на Главную страницу
        </a>
      </div>
    </>
  );
}
