import { API_ENDPOINTS } from "../../api/path";

export function GithubButton() {
  const handleClick = async () => {
    try {
      window.location.href = API_ENDPOINTS.AUTH.GITHUB;
    } catch (error) {
      console.log('Error github auth: ', error);
    }
  };

  return <button onClick={handleClick}>Login with GitHub</button>;
}
