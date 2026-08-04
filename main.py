import os
import sys
import re
import time
import mimetypes
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()
client = genai.Client()

# Store uploaded files temporarily in this session: { "abs_filename": file_object }
session_files = {}

def extract_filenames(text):
    """Finds @filename patterns, supporting spaces by checking existing paths."""
    found_files = []
    candidates = re.findall(r'@([^,;\n]+)', text)
    
    for candidate in candidates:
        candidate = candidate.strip()
        if os.path.exists(candidate):
            found_files.append(candidate)
        else:
            parts = candidate.split()
            matched = False
            for i in range(len(parts), 0, -1):
                test_path = " ".join(parts[:i])
                if os.path.exists(test_path):
                    found_files.append(test_path)
                    matched = True
                    break
            
            # Warn the user if a file mention was detected but not found
            if not matched:
                # Grab the first word after the @ to show in the error
                attempted_name = parts[0] if parts else candidate
                console.print(f"[red]⚠️ Warning: Detected '@{attempted_name}' but could not find the file on your computer.[/red]")
                
    return found_files

def main():
    console.print(Panel.fit(
        "[bold blue]Ask[/bold blue]\nType 'exit' to quit. Use @filename to attach files.", 
        border_style="blue"
    ))
    
    chat = client.chats.create(model="gemini-2.5-flash")

    while True:
        user_input = Prompt.ask("[bold green]You[/bold green]")
        if user_input.lower() in ["exit", "quit"]:
            break
        if not user_input.strip():
            continue

        files_to_attach = []
        filenames = extract_filenames(user_input)
        
        for filename in filenames:
            user_input = user_input.replace(f"@{filename}", "", 1).strip()
            abs_filename = os.path.abspath(filename)
            
            if abs_filename in session_files:
                console.print(f"[yellow]✓ Using cached file: {filename}[/yellow]")
                files_to_attach.append(session_files[abs_filename])
            else:
                if os.path.exists(abs_filename):
                    try:
                        console.print(f"[cyan]⏳ Uploading {filename} via File API...[/cyan]")
                    
                        mime_type, _ = mimetypes.guess_type(abs_filename)
                    
                        if not mime_type:
                            mime_type = "text/plain"
                    
                        uploaded_file = client.files.upload(
                            file=abs_filename,
                            config=types.UploadFileConfig(mime_type=mime_type)
                        )
                    
                        while uploaded_file.state.name == "PROCESSING":
                            time.sleep(1)
                            uploaded_file = client.files.get(name=uploaded_file.name)
                    
                        if uploaded_file.state.name == "FAILED":
                            raise Exception("Google processing failed on the file.")

                        files_to_attach.append(uploaded_file)
                        console.print(f"[green]✓ Uploaded: {filename}[/green]")
                    except Exception as e:
                        console.print(f"[red]❌ CRITICAL: Upload failed for {filename}.[/red]")
                        console.print(f"[red]Error details: {e}[/red]")
                        
                else:
                    console.print(f"[red]File not found: {abs_filename}[/red]")

        payload = []
        if user_input:
            payload.append(user_input)
        elif files_to_attach:
            payload.append("[Attached File]")
            
        payload.extend(files_to_attach)

        try:
            with console.status("[bold purple]Thinking...", spinner="dots"):
                response = chat.send_message(payload)
            
            reply_text = response.text
            
            console.print()
            console.print("[bold blue]Assistant:[/bold blue]")
            console.print(Markdown(reply_text))
            console.print()

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()
    