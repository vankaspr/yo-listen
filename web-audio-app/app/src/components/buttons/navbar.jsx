import '../../style/navbar.css';
import { useState } from 'react';

export function Navbar({ setActiveForm }) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isJoinDropdownOpen, setIsJoinDropdownOpen] = useState(false);

  return (
    <>
      <nav>
        <div>
          <ul>
            <div className="text-div">
              <h4>Yo! Listen</h4>
            </div>

            <li>Home</li>
            <li>News</li>
            <li>Recomendation</li>

            <li
              className="dropdown"
              onMouseEnter={() => setIsJoinDropdownOpen(true)}
              onMouseLeave={() => setIsJoinDropdownOpen(false)}
            >
              <a href="join">Join us</a>
              {isJoinDropdownOpen && (
                <ul className="dropdown-content">
                  <div>
                    <li>
                      <button
                        onClick={() => {
                          setActiveForm('login');
                          setIsJoinDropdownOpen(false);
                        }}
                      >
                        Sign in
                      </button>
                    </li>

                    <li>
                      <button
                        onClick={() => {
                          setActiveForm('register');
                          setIsJoinDropdownOpen(false);
                        }}
                      >
                        Sign up
                      </button>
                    </li>
                  </div>
                </ul>
              )}
            </li>
            <li
              className="dropdown"
              onMouseEnter={() => setIsDropdownOpen(true)}
              onMouseLeave={() => setIsDropdownOpen(false)}
            >
              <a href="#more">More</a>
              {isDropdownOpen && (
                <ul className="dropdown-content">
                  <div>
                    <li>
                      <a href="#help">Help</a>
                    </li>
                    <li>
                      <a href="#about">About us</a>
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
