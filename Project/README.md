# AI Text Detector

A complete MVP full-stack app for detecting how likely a piece of text is AI-generated.

- Frontend: React + Vite (port `3000`)
- Backend: FastAPI (port `8000`)
- Current model: mock `callModel(text)` function (easy to replace later)

## Project Structure

```text
project-root/
 ├── frontend/
 ├── backend/
 └── README.md
```

Frontend structure:

```text
frontend/src/
 ├── components/
 │    ├── TextInput.jsx
 │    ├── ResultCard.jsx
 │    └── Loader.jsx
 ├── services/
 │    └── api.js
 ├── App.jsx
```

Backend structure:

```text
backend/
 ├── main.py
 ├── models.py
 ├── services/
 │    └── detector.py
```

## Requirements

- Node.js 18+
- Python 3.10+

## Installation

### 1) Clone/open project

Use this repository folder as the project root.

### 2) Backend setup

```bash
cd backend
python -m venv .venv
```

Activate virtual environment:

- Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

- macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3) Frontend setup

In another terminal:

```bash
cd frontend
npm install
```

## Running the App

### Run backend (port 8000)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Run frontend (port 3000)

```bash
cd frontend
npm run dev
```

Open: [http://localhost:3000](http://localhost:3000)

## API

### POST `/check`

Request:

```json
{
  "text": "Some message to analyze..."
}
```

Response:

```json
{
  "probability": 0.87
}
```

Validation behavior:

- Empty text: rejected (`400`)
- Text with fewer than 10 characters: rejected (`422`)

## Mock Model Details

The model logic is intentionally isolated in:

- `backend/services/detector.py`

Function:

```python
def callModel(text: str) -> float:
    ...
```

This function currently returns a deterministic mock probability (between `0.1` and `0.95`) based mainly on text length. It is separated so another developer can replace only this function with a real ML model without changing:

- API route (`POST /check`)
- Request/response schema
- Frontend integration

## Future ML Integration Notes

To integrate a real model later:

1. Keep `POST /check` contract unchanged.
2. Replace internal logic in `callModel(text)`.
3. Add optional preprocessing and model confidence calibration.
4. Add logging/monitoring and model version metadata if needed.
5. Add tests for edge cases and expected probability ranges.
