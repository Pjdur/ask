# ask

`ask` is a simple terminal tool to ask AI anything.
This is the second iteration of ask (v2).

**Features**

- Add files (@filename)
- Session caching
- Terminal UI with `Rich`

**Version Comparison**

| Feature          | ask (v2)              | ask-v1           |
| :--------------- | :-------------------- | :--------------- |
| **Language**     | Python                | Rust             |
| **AI backend**   | Google Gemini         | Github Models    |
| **Speed**        | Fast                  | Instant          |
| **File Support** | @filename attachments | None (text only) |

## Setup

Set your Gemini API key in your environment variables:

- **Linux / macOS:**
  ```bash
  export GEMINI_API_KEY="your_api_key_here"
  ```

- **Windows (PowerShell):**
  ```powershell
  $env:GEMINI_API_KEY="your_api_key_here"
  ```
