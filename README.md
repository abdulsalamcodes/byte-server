# Byte Server API

FastAPI service that generates programming quiz questions using an Ollama-compatible model.

**Live Frontend:** [https://byte-q.vercel.app/](https://byte-q.vercel.app/)

## Features

- **Quiz Generation**: Generate programming questions for various languages and difficulty levels.
- **Streaming Support**: Stream responses in real-time or get structured JSON.
- **Model Agnostic**: Compatible with any Ollama model (default: `gpt-oss:20b`).
- **Robust Error Handling**: Validates inputs and handles model failures gracefully.

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.10+
- **AI Integration**: Ollama
- **Validation**: Pydantic

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.com/) running locally or accessible via URL

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/abdulsalamcodes/byte-server.git
    cd byte-server
    ```

2.  Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Set the following environment variable:

- `OLLAMA_API_KEY`: Your Ollama API key (if required by your provider).

You can set this in a `.env` file or export it in your shell.

### Running the Server

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

### POST `/quiz/generate`

Generate programming quiz questions.

**Request Body:**

```json
{
  "lang": "Python",
  "num_questions": 5,
  "difficulty": "medium",
  "model": "gpt-oss:20b",
  "stream": false
}
```

| Field           | Type    | Description                           | Default       |
| :-------------- | :------ | :------------------------------------ | :------------ |
| `lang`          | string  | Programming language (e.g., "Python") | Required      |
| `num_questions` | integer | Number of questions (1–50)            | 5             |
| `difficulty`    | string  | `easy`, `medium`, or `hard`           | Required      |
| `model`         | string  | Ollama model identifier               | `gpt-oss:20b` |
| `stream`        | boolean | Stream response text                  | `false`       |

**Responses:**

- **200 OK (JSON)**: Array of question objects.
- **200 OK (Stream)**: Text stream.
- **422 Unprocessable Entity**: Invalid input.
- **502 Bad Gateway**: Model failure.

**Example (cURL):**

```bash
curl -s -X POST http://localhost:8000/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"lang": "Python", "difficulty": "medium"}'
```

## Contributing

We welcome contributions! Please follow these steps:

1.  **Fork the repository**.
2.  **Create a new branch**: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and commit them: `git commit -m 'Add some feature'`.
4.  **Push to the branch**: `git push origin feature/your-feature-name`.
5.  **Submit a pull request**.

Please ensure your code follows the existing style and includes tests where appropriate.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
