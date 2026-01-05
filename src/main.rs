use gh_models::{GHModels, types::ChatMessage};
use std::env;
use std::io::{self, Write};

#[tokio::main]
async fn main() {
    let token = env::var("GITHUB_TOKEN").expect("Missing GITHUB_TOKEN");
    let client = GHModels::new(token);

    let mut messages = vec![
        ChatMessage {
            role: "system".into(),
            content: "You are a helpful assistant.".into(),
        }
    ];

    loop {
        print!("You: ");
        io::stdout().flush().unwrap();

        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        let input = input.trim().to_string();

        if input == "exit" {
            break;
        }

        messages.push(ChatMessage {
            role: "user".into(),
            content: input.clone(),
        });

        let response = client
            .chat_completion("openai/gpt-4o", &messages, 1.0, 4096, 1.0)
            .await
            .unwrap();

        let reply = response.choices[0].message.content.clone();
        println!("Assistant: {}", reply);

        messages.push(ChatMessage {
            role: "assistant".into(),
            content: reply,
        });
    }
}