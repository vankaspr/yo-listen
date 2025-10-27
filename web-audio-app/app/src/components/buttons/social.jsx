export function GithubButton() {
  const handleClick = () => {
    alert('Github clicked!');
  };

  return <button onClick={handleClick}>Github</button>;
}
