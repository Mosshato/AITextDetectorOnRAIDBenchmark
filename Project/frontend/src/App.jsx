import { useMemo, useState } from "react";
import TextInput from "./components/TextInput";
import Loader from "./components/Loader";
import ResultCard from "./components/ResultCard";
import { checkText } from "./services/api";

function App() {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [probability, setProbability] = useState(null);
  const [error, setError] = useState("");
  const [validationError, setValidationError] = useState("");

  const isButtonDisabled = useMemo(
    () => isLoading || text.trim().length === 0,
    [isLoading, text]
  );

  const validateInput = (value) => {
    const trimmed = value.trim();
    if (!trimmed) return "Please enter text before checking.";
    if (trimmed.length < 10) return "Text must be at least 10 characters long.";
    return "";
  };

  const handleCheck = async () => {
    const inputError = validateInput(text);
    setValidationError(inputError);
    setError("");
    setProbability(null);

    if (inputError) return;

    try {
      setIsLoading(true);
      const result = await checkText(text.trim());
      setProbability(result.probability);
    } catch (requestError) {
      setError(requestError.message || "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="page">
      <section className="card">
        <h1 className="title">AI Generated Text Detector</h1>
        <p className="subtitle">Paste your text below to analyze it</p>

        <TextInput
          value={text}
          onChange={(value) => {
            setText(value);
            if (validationError) {
              setValidationError(validateInput(value));
            }
          }}
          disabled={isLoading}
        />

        {validationError ? <p className="message error">{validationError}</p> : null}
        {error ? <p className="message error">{error}</p> : null}

        <button
          className="check-button"
          type="button"
          onClick={handleCheck}
          disabled={isButtonDisabled}
        >
          Check Text
        </button>

        {isLoading ? <Loader /> : null}
        {!isLoading && probability !== null ? <ResultCard probability={probability} /> : null}
      </section>
    </main>
  );
}

export default App;
