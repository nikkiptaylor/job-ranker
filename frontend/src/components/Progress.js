export default function Progress({ loading, progress, numToClassify }) {
  if (loading) {
    const loadingText = "Loading...";
    return (
      <span>
        <p>{loadingText}</p>
        <p>
          Classified {progress} of {numToClassify} jobs
        </p>
      </span>
    );
  } else return null;
}
