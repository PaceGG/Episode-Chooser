const GameDetails = ({ mainGameName, additionalGames }) => {
  if (additionalGames.length === 0) {
    return <li>{mainGameName}</li>;
  } else {
    return (
      <details>
        <summary>{mainGameName}</summary>
        <ul>
          {additionalGames.map((game, index) => (
            <li key={index}>{game}</li>
          ))}
        </ul>
      </details>
    );
  }
};

export default GameDetails;
