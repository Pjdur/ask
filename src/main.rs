use cliux::Input;
use gh_models::{GHModels, types::ChatMessage};
use std::env;
use clap::Parser;
use colorline::Style;
use crossterm::{execute, terminal::{Clear, ClearType}, cursor::MoveTo};
use std::io::stdout;

#[derive(Parser, Debug)]
struct Args {
    /// Model to use (e.g. openai/gpt-4o)
    #[arg(long, default_value = "openai/gpt-4o")]
    model: String,
}

#[tokio::main]
async fn main() {
    let args = Args::parse();

    let token = env::var("GITHUB_TOKEN").expect("Missing GITHUB_TOKEN");
    let client = GHModels::new(token);

    let mut messages = vec![
        ChatMessage {
            role: "system".into(),
            content: "You are a helpful assistant.".into(),
        }
    ];

    loop {
        // I don't know why but I have to use both All and Purge
        // to clear the visible screen and scrollback
        execute!(stdout(), Clear(ClearType::All)).unwrap();
        execute!(stdout(), Clear(ClearType::Purge)).unwrap();
        execute!(stdout(), MoveTo(0,0)).unwrap();

        println!("{}", "ask - ask anything".grey());

        for msg in &messages {
            match msg.role.as_str() {
                "user" => println!("{} {}", "You:".green(), msg.content),
                "assistant" => println!("{} {}", "Assistant:".blue(), msg.content),
                _ => {}
            }
        }

        let input = Input::new("Enter your message")
            .bold(true)
            .color("cyan")
            .style("rounded")
            .width(50)
            .prompt();

        let input = input.trim().to_string();

        if input == "exit" {
            break;
        }

        messages.push(ChatMessage {
            role: "user".into(),
            content: input.clone(),
        });

        let response = client
            .chat_completion(&args.model, &messages, 1.0, 4096, 1.0)
            .await
            .unwrap();

        let reply = response.choices[0].message.content.clone();

        messages.push(ChatMessage {
            role: "assistant".into(),
            content: reply,
        });
    }
}
