# ask

A tiny terminal chat app for talking to an AI model, nothing fancy (yet!), just a clean little loop where you type a message and it answers back. Think of it as a lightweight companion you can summon from your shell whenever you want to ask something quickly.

## Getting Started

### Installation

Run:

```bash
cargo install --git https://github.com/Pjdur/ask.git
```

### Set your GitHub token

**Windows (PowerShell):**
```powershell
setx GITHUB_TOKEN "your_token_here"
```

**Linux / macOS:**
```bash
export GITHUB_TOKEN=your_token_here
```

### Run it

```bash
cargo run
```

You’ll drop into a simple chat prompt.  
Type your message, press Enter, and the AI replies.  
Type `exit` to leave the conversation.

You can also run it using a different model:

```bash
cargo run -- --model openai/gpt-5
```

## Why?

Because sometimes you just want to ask a question without opening a browser, switching apps, or losing your flow.
