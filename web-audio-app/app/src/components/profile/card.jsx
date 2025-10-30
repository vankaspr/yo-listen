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
          <div>

            <di >
              <div>
                <div>
                    <p>Email:{profileData.email}</p>
                    <p>Username: {profileData.username}</p>
                    <p>Verified: {profileData.is_verified}</p>
                    <p>Member sinse: {profileData.created_at}</p>
                </div>
                <div>
                  {profileData.avatar ? (
                    <img
                      src={profileData.avatar}
                      alt="User avatar"
                    />
                  ) : (
                    <div>Avatar opso...sybai sybai </div>
                  )}
                  {/*TODO: достать аватарку и подгонять под размеры если нужно */}
                </div>
              </div>

              <div className="bio">
                {profileData.bio ? (
                  <p>{profileData.bio}</p>
                ) : (
                  <p>
                    Это место для описания вашего профиля!
                  </p>
                )}
              </div>
              <p>
                Profile: {profileData.message} for {currentUser.username}
              </p>
              <p>Theme: {profileData.theme}</p>
            </di>
          </div>
        </>
      )}
    </>
  );
}
