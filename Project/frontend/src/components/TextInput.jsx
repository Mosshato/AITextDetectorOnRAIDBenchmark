function TextInput({ value, onChange, disabled }) {
  return (
    <div className="field-group">
      <label htmlFor="textInput" className="field-label">
        Text to analyze
      </label>
      <textarea
        id="textInput"
        className="text-input"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Paste your email, message, or paragraph here..."
        disabled={disabled}
        rows={10}
      />
    </div>
  );
}

export default TextInput;
