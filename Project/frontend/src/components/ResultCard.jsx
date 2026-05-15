function getInterpretation(probabilityPercent) {
  if (probabilityPercent <= 30) return "Likely Human";
  if (probabilityPercent <= 70) return "Uncertain";
  return "Likely AI Generated";
}

function ResultCard({ probability }) {
  const percent = Math.round(probability * 100);
  const interpretation = getInterpretation(percent);

  return (
    <section className="result-card">
      <h2 className="result-title">Result</h2>
      <p className="result-probability">{percent}%</p>
      <p className="result-interpretation">{interpretation}</p>
    </section>
  );
}

export default ResultCard;
