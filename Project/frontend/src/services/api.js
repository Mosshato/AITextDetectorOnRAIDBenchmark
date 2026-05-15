const API_BASE_URL = "http://localhost:8000";

export async function checkText(text) {
  const response = await fetch(`${API_BASE_URL}/check`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const errorMessage = data?.detail || "Failed to analyze text.";
    throw new Error(errorMessage);
  }

  return data;
}
