import '../style/navbar.css';
import { useState } from 'react';

export function Navbar({
  setActiveForm,
  isAuthenticated,
  currentUser,
  onLogout,
  activeBar,
  setActiveBar,
}) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isJoinDropdownOpen, setIsJoinDropdownOpen] = useState(false);
  const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false);

  const handleBarChange = bar => {
    setActiveBar(bar);
    setActiveForm(null);
  };

  return (
    <>
      <nav>
        <div>
          <ul>
            <div className="text-div">
              <h4>Йо! Слушай</h4>
            </div>

            <li
              className={activeBar === 'home' ? 'active' : ''}
              onClick={() => handleBarChange('home')}
            >
              Главная
            </li>

            <li
              className={activeBar === 'more' ? 'active' : ''}
              onClick={() => handleBarChange('more')}
            >
              Новости
            </li>
            <li
              className={activeBar === 'recomendation' ? 'active' : ''}
              onClick={() => handleBarChange('recomendation')}
            >
              Рекомендации
            </li>

            {/* Если пользователь авторизован, то вместо этого будет Профиль*/}
            {!isAuthenticated ? (
              <li
                className="dropdown"
                onMouseEnter={() => setIsJoinDropdownOpen(true)}
                onMouseLeave={() => setIsJoinDropdownOpen(false)}
              >
                <a className={activeBar === 'join' ? 'active' : ''} href="join">
                  Присоединиться
                </a>
                {isJoinDropdownOpen && (
                  <ul className="dropdown-content">
                    <div>
                      <li>
                        <button
                          onClick={() => {
                            setActiveForm('login');
                            setIsJoinDropdownOpen(false);
                            setActiveBar('join');
                          }}
                        >
                          Логин
                        </button>
                      </li>

                      <li>
                        <button
                          onClick={() => {
                            setActiveForm('register');
                            setIsJoinDropdownOpen(false);
                            setActiveBar('join');
                          }}
                        >
                          Регистрация
                        </button>
                      </li>
                    </div>
                  </ul>
                )}
              </li>
            ) : (
              <li
                className="dropdown"
                onMouseEnter={() => setIsProfileDropdownOpen(true)}
                onMouseLeave={() => setIsProfileDropdownOpen(false)}
              >
                <a
                  className={activeBar === 'profile' ? 'active' : ''}
                  href="#profile"
                  onClick={(e) => {
                    e.preventDefault();
                    setActiveBar('profile');
                  }}
                >
                  👤 {currentUser?.username} ! Profile
                </a>
                {isProfileDropdownOpen && (
                  <ul className="dropdown-content">
                    <div>
                      <li>
                        <button>Настройки</button>
                      </li>
                      <li>
                        <button>Слушаем!</button>
                      </li>
                      <li>
                        <button>Поддержка</button>
                      </li>
                      <li>
                        <button onClick={onLogout}>Выйти</button>
                      </li>
                    </div>
                  </ul>
                )}
              </li>
            )}
            <li
              className="dropdown"
              onMouseEnter={() => setIsDropdownOpen(true)}
              onMouseLeave={() => setIsDropdownOpen(false)}
            >
              <a href="#more">Ещё</a>
              {isDropdownOpen && (
                <ul className="dropdown-content">
                  <div>
                    <li>
                      <button>Помощь</button>
                    </li>
                    <li>
                      <button>О нас</button>
                    </li>
                  </div>
                </ul>
              )}
            </li>
          </ul>
        </div>
      </nav>
    </>
  );
}
