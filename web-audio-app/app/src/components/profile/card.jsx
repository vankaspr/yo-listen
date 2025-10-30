import { useEffect, useState } from 'react';
import { API_ENDPOINTS } from '../../api/path';
import { useAuthFetch } from '../../hooks/auth';
import '../../style/profile/card.css';

export function Profile({ currentUser }) {
  const { authFetch } = useAuthFetch();
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await authFetch(API_ENDPOINTS.USER.PROFILE);

      if (response.ok) {
        const data = await response.json();
        // get data
        setProfileData(data);
      } else {
        setError('Failed to load profile');
        console.log('Error: something was wrong');
      }
    } catch (error) {
      setError('Network error');
      console.log('Error: ', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  if (loading) {
    return <div>Loading profile...</div>;
  }

  if (error) {
    return (
      <>
        <div>
          <p>Error: {error}</p>
          <button onClick={fetchProfile}>Try again</button>
        </div>
      </>
    );
  }

  return (
    <>
      {profileData && (
        <>
          <div className="card-container">

            <div className="profile-container">
              <div className="user-info-container ">
                <div className='user-info'>
                    <p>Email:{profileData.email}</p>
                    <p>Username: {profileData.username}</p>
                    <p>Verified: {profileData.is_verified}</p>
                    <p>Member sinse: {profileData.created_at}</p>
                </div>
                <div className="avatar">
                  {profileData.avatar ? (
                    <img
                      src={profileData.avatar}
                      alt="User avatar"
                      className="avatar-image"
                    />
                  ) : (
                    <div className="avatar-placeholder"></div>
                  )}
                  {/*TODO: достать аватарку и подгонять под размеры если нужно */}
                </div>
              </div>

              <div className="bio">
                {profileData.bio ? (
                  <p>{profileData.bio}</p>
                ) : (
                  <p>
                    Это место для описания вашего профиля! Расскажите что-то
                    интересное о себе. Не бойтесь быть красноречивым, большие
                    тексты приветствуются, это всего лишь пара строчек в css
                    файлике. Используйте свои любимые эмодзи, расскажите свой
                    любимый анекдот или напишите строчку вашей любимой песни.
                    Или напишите какую-нибудь ерунду, давай полосочка появись,
                    родная 🫩👅 Come to daddy 🥸 GOOD GIRL I SEE U
                  </p>
                )}
              </div>
              <p>
                Profile: {profileData.message} for {currentUser.username}
              </p>
              <p>Theme: {profileData.theme}</p>
            </div>
          </div>
        </>
      )}
    </>
  );
}
