function Loader() {
  return (
    <div className="loader" role="status" aria-live="polite">
      <div className="spinner" />
      <span>Checking text...</span>
    </div>
  );
}

export default Loader;
