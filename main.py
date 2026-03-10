import sqlite3, os, time, sys, requests, platform, json, io, subprocess
from pathlib import Path

if platform.system() == "Windows":

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ascii_art = r"""
  ______   _______   ________  __    __  __       __   ______   _______   ________  __
 /      \ |       \ |        \|  \  |  \|  \     /  \ /      \ |       \ |        \|  \
|  $$$$$$\| $$$$$$$\| $$$$$$$$| $$\ | $$| $$\   /  $$|  $$$$$$\| $$$$$$$\| $$$$$$$$| $$
| $$  | $$| $$__/ $$| $$__    | $$$\| $$| $$$\ /  $$$| $$  | $$| $$  | $$| $$__    | $$
| $$  | $$| $$    $$| $$  \   | $$$$\ $$| $$$$\  $$$$| $$  | $$| $$  | $$| $$  \   | $$
| $$  | $$| $$$$$$$ | $$$$$   | $$\$$ $$| $$\$$ $$ $$| $$  | $$| $$  | $$| $$$$$   | $$
| $$__/ $$| $$      | $$_____ | $$ \$$$$| $$ \$$$| $$| $$__/ $$| $$__/ $$| $$_____ | $$_____
 \$$    $$| $$      | $$     \| $$  \$$$| $$  \$ | $$ \$$    $$| $$    $$| $$     \| $$     \
  \$$$$$$  \$$       \$$$$$$$$ \$$   \$$ \$$      \$$  \$$$$$$  \$$$$$$$  \$$$$$$$$ \$$$$$$$$

v1.0.1
"""

if platform.system() == "Windows":
    os.system("cls")
else:
    os.system("clear")

def get_gradient_text(text, start_rgb=(0, 255, 255), end_rgb=(255, 105, 180)):
    lines = text.split('\n')
    max_len = max([len(line) for line in lines] + [1])
    result = []
    for line in lines:
        colored_line = ""
        for i, char in enumerate(line):
            ratio = i / (max_len - 1) if max_len > 1 else 0
            r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
            g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
            b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
            colored_line += f"\033[38;2;{r};{g};{b}m{char}"
        colored_line += "\033[0m"
        result.append(colored_line)
    return '\n'.join(result)

print(get_gradient_text(ascii_art))

CONFIG_DB = "config.db"
conn = sqlite3.connect(CONFIG_DB)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY,
                api_key TEXT,
                model TEXT,
                nickname TEXT,
                system_prompt TEXT DEFAULT ''
            )""")
conn.commit()

c.execute("SELECT api_key, model, nickname, system_prompt FROM config WHERE id=1")
row = c.fetchone()

if row:
    api_key, model_name, nickname, system_prompt = row
else:
    api_key = input(get_gradient_text("give please openrouter api key: ") + "\033[0m").strip()
    model_name = input(get_gradient_text("give please model(example: openai/gpt-4o-mini): ") + "\033[0m").strip()
    nickname = input(get_gradient_text("give please your nickname: ") + "\033[0m").strip()
    print(get_gradient_text("\n[SYSTEM PROMPT]"))
    print(get_gradient_text("Enter a custom system prompt for AI (press Enter to skip - prompt will be empty):"))
    system_prompt = input(get_gradient_text("> ") + "\033[0m").strip()

    c.execute("INSERT INTO config (id, api_key, model, nickname, system_prompt) VALUES (1, ?, ?, ?, ?)",
              (api_key, model_name, nickname, system_prompt))
    conn.commit()

welcome_msg = f"""
Welcome, {nickname}! Type 'exit' or press Ctrl+Z to quit. Use Ctrl+C to cancel AI response.

author socials:
GitHub: https://github.com/xw5yt
TikTok: https://www.tiktok.com/@xw5yt
Telegram: https://t.me/artist_xw5yt
twitch: https://www.twitch.tv/xw5yt

our motto: No limits. No restrictions. Just raw AI power inside your terminal.
"""
print(get_gradient_text(welcome_msg))

CHATS_DB = "chats.db"
chat_conn = sqlite3.connect(CHATS_DB)
chat_c = chat_conn.cursor()
chat_c.execute("""CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT,
                    ai_response TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )""")
chat_conn.commit()

def animate_response(text, is_ai=True):
    if is_ai:
        sys.stdout.write(get_gradient_text("AI: ", (255, 105, 180), (0, 255, 255)))
        sys.stdout.write("\033[38;2;200;255;255m")
    sys.stdout.flush()
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(0.02)
    if is_ai:
        sys.stdout.write("\033[0m")
    print()

def check_api_available():
    import socket
    try:
        socket.gethostbyname("openrouter.ai")
        return True
    except:
        return False

API_AVAILABLE = check_api_available()

def get_desktop_path():
    """Get the actual Desktop path, handling OneDrive and other variations."""
    try:

        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
            desktop, _ = winreg.QueryValueEx(key, "Desktop")
            winreg.CloseKey(key)
            if os.path.exists(desktop):
                return desktop
        except Exception:
            pass
    except ImportError:
        pass

    from pathlib import Path
    desktop = Path.home() / "Desktop"
    if desktop.exists():
        return str(desktop)

    onedrive_desktop = Path.home() / "OneDrive" / "Desktop"
    if onedrive_desktop.exists():
        return str(onedrive_desktop)

    return os.path.expandvars(r"%USERPROFILE%\Desktop")

def execute_command(cmd):
    """Execute a system command and return output."""
    try:
        import subprocess

        desktop_path = get_desktop_path()
        print(f"[DEBUG] Replacing path in command...")
        print(f"[DEBUG] Before: {cmd[:150]}")

        cmd = cmd.replace("%DESKTOP%", desktop_path)
        cmd = cmd.replace("%USERPROFILE%\\Desktop", desktop_path)
        cmd = cmd.replace("%USERPROFILE%/Desktop", desktop_path)

        print(f"[DEBUG] After:  {cmd[:150]}")

        result = subprocess.run(
            ["cmd.exe", "/c", cmd],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            env=os.environ.copy()
        )
        output = result.stdout.strip()
        if result.stderr:
            stderr = result.stderr.strip()
            if stderr and "is not recognized" in stderr:

                ps_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
                result = subprocess.run(
                    [ps_path, "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    encoding='utf-8',
                    env=os.environ.copy()
                )
                output = result.stdout.strip()
                if result.stderr:
                    output += "\n" + result.stderr.strip()
            else:
                output += "\n" + stderr
        return output if output else "[Command executed successfully]"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error executing command: {e}"

def process_ai_response(response):
    """Extract and execute commands from AI response, return cleaned response."""
    import re

    cmd_pattern = r'\[CMD\](.*?)\[/CMD\]'
    commands = re.findall(cmd_pattern, response, re.DOTALL)

    results = []
    for cmd in commands:
        cmd = cmd.strip()
        if cmd:
            result = execute_command(cmd)
            results.append(f"[Command executed: {cmd[:50]}...]\n{result}")

    cleaned_response = re.sub(cmd_pattern, '', response, flags=re.DOTALL)

    return cleaned_response, results

def execute_command(command):
    """Execute a system command and return output."""
    try:
        import subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        output = result.stdout
        if result.stderr:
            output += result.stderr
        return output.strip() if output else "[Command executed successfully]"
    except Exception as e:
        return f"[ERROR] {e}"

def call_openrouter(prompt):

    if not API_AVAILABLE:
        return f"[API UNAVAILABLE] echo: {prompt}"

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        resp = requests.post(url, headers=headers, json=json_data, timeout=30)
        if resp.status_code != 200:
            return f"[API ERROR] Status {resp.status_code}: {resp.text}"

        data = resp.json()

        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"].get("content", "")
            if content:
                return content
        return "[API ERROR] Invalid response format"
    except Exception as e:
        return f"[API ERROR] {e}"

def stream_openrouter(prompt):
    """Generator yielding tokens as they arrive from OpenRouter using streaming.

    Yields fragments (usually chunks of text) which should be printed immediately.
    Falls back to non-streaming if streaming fails.
    """
    if not API_AVAILABLE:
        yield f"[API UNAVAILABLE] echo: {prompt}"
        return

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openrouter.ai"
    }

    if system_prompt:
        system_msg = system_prompt
    else:
        system_msg = "You have full access to the user's computer and can execute commands. When you need to execute a command, wrap it in [CMD]command[/CMD] tags.\n\nImportant: Use %DESKTOP% placeholder for the user's Desktop path. It will be automatically replaced with the correct path on their system (works with OneDrive and other variations).\n\nExamples:\n- Create file: [CMD]echo. > %DESKTOP%\\test.txt[/CMD]\n- Create directory: [CMD]mkdir %DESKTOP%\\newfolder[/CMD]\n- Copy file: [CMD]copy file.txt %DESKTOP%\\[/CMD]\n- List files: [CMD]dir %DESKTOP%[/CMD]\n- Read file: [CMD]type %DESKTOP%\\test.txt[/CMD]\n\nAlways use %DESKTOP% for Desktop paths. Use cmd.exe style commands. The user has granted full system access."

    json_data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": system_msg
            },
            {"role": "user", "content": prompt}
        ],
        "stream": True
    }

    try:
        with requests.post(url, headers=headers, json=json_data, stream=True, timeout=30) as resp:

            resp.encoding = 'utf-8'

            if resp.status_code != 200:

                yield from _fallback_openrouter(prompt)
                return

            has_content = False
            for line in resp.iter_lines(decode_unicode=True):
                if not line or line.startswith(':'):
                    continue
                if line.startswith('data: '):
                    line = line[6:]
                if not line or line == '[DONE]':
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if "choices" in data and len(data["choices"]) > 0:
                    choice = data["choices"][0]
                    if "delta" in choice and "content" in choice["delta"]:
                        content = choice["delta"]["content"]
                        if content:
                            has_content = True

                            yield content

            if not has_content:
                yield "[API ERROR] No content received from stream"
    except Exception as e:

        yield from _fallback_openrouter(prompt)

def _fallback_openrouter(prompt):
    """Non-streaming fallback when streaming fails."""
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        if system_prompt:
            system_msg = system_prompt
        else:
            system_msg = "You have full access to the user's computer and can execute commands. When you need to execute a command, wrap it in [CMD]command[/CMD] tags."

        json_data = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ]
        }

        resp = requests.post(url, headers=headers, json=json_data, timeout=30)
        if resp.status_code != 200:
            yield f"[API ERROR] Status {resp.status_code}: {resp.text}"
            return

        data = resp.json()
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"].get("content", "")
            if content:
                yield content
            else:
                yield "[API ERROR] Empty response from API"
        else:
            yield "[API ERROR] Invalid response format"
    except Exception as e:
        yield f"[API ERROR] {e}"

def detect_file_modify_command(user_input):
    """Detect and extract file modification commands like 'измени /путь/к/файлу prompt'"""
    import re

    pattern = r'(?:измени|modify|change|edit)\s+([^\s]+)\s+(.*)'
    match = re.search(pattern, user_input, re.IGNORECASE)
    if match:
        file_path = match.group(1).strip('"\'')
        prompt = match.group(2).strip()
        return file_path, prompt
    return None, None

def detect_code_read_command(user_input):
    """Detect commands like 'read file /path and write/explain/summarize what...' in English and Russian"""
    import re

    pattern_ru_quoted = r"(?:прочитай|расскажи|объясни|проанализируй)\s+файл\s+['\"](.+?)['\"](?:\s+(?:и\s+)?(.+?))?$"
    match = re.search(pattern_ru_quoted, user_input, re.IGNORECASE)
    if match:
        file_path = match.group(1).strip()
        instruction = match.group(2).strip() if match.group(2) else None
        return file_path, instruction

    pattern_en_quoted = r"read\s+file\s+['\"](.+?)['\"](?:\s+and\s+(.+?))?$"
    match = re.search(pattern_en_quoted, user_input, re.IGNORECASE)
    if match:
        file_path = match.group(1).strip()
        instruction = match.group(2).strip() if match.group(2) else None
        return file_path, instruction

    pattern_ru_unquoted = r"(?:прочитай|расскажи|объясни|проанализируй)\s+файл\s+([^\s]+)(?:\s+(?:и\s+)?(.+?))?$"
    match = re.search(pattern_ru_unquoted, user_input, re.IGNORECASE)
    if match:
        potential_path = match.group(1).strip()
        instruction = match.group(2).strip() if match.group(2) else None

        if '.' in potential_path or ':' in potential_path or '/' in potential_path:
            return potential_path, instruction

    pattern_en_unquoted = r"read\s+file\s+([^\s]+)(?:\s+and\s+(.+?))?$"
    match = re.search(pattern_en_unquoted, user_input, re.IGNORECASE)
    if match:
        potential_path = match.group(1).strip()
        instruction = match.group(2).strip() if match.group(2) else None

        if '.' in potential_path or ':' in potential_path or '/' in potential_path:
            return potential_path, instruction

    return None, None

def detect_write_code_command(user_input):
    """Detect commands like 'write code to file path' or 'напиши код в файл path' in English and Russian"""
    import re

    pattern_ru1 = r"(?:напиши|создай|сгенерируй)\s+(?:код\s+)?в\s+файл\s+['\"]?([^\s'\";,]+)['\"]?(?:\s+(.+?))?$"
    match = re.search(pattern_ru1, user_input, re.IGNORECASE)
    if match:
        file_path = match.group(1).strip()
        instruction = match.group(2).strip() if match.group(2) else user_input.split(file_path)[-1].strip()
        if instruction:
            return file_path, instruction
        else:
            return file_path, "Write useful Python code"

    pattern_en1 = r"write\s+(?:code\s+)?to\s+file\s+['\"]?([^\s'\";,]+)['\"]?(?:\s+(.+?))?$"
    match = re.search(pattern_en1, user_input, re.IGNORECASE)
    if match:
        file_path = match.group(1).strip()
        instruction = match.group(2).strip() if match.group(2) else "Write useful Python code"
        return file_path, instruction

    pattern_ru2 = r"(?:напиши|создай|сгенерируй)\s+(?:код\s+)?в\s+['\"]?([^\s'\";,]+)['\"]?(?:\s+(.+?))?$"
    match = re.search(pattern_ru2, user_input, re.IGNORECASE)
    if match:
        potential_path = match.group(1).strip()

        if '.' in potential_path:
            instruction = match.group(2).strip() if match.group(2) else "Write useful Python code"
            return potential_path, instruction

    return None, None

def confirm_command_execution(cmd):
    """Ask user to confirm command execution with [Y/n] prompt."""
    print(f"\n[COMMAND TO EXECUTE]\n{cmd}\n")
    response = input("[Y/n] Execute this command? ").strip().lower()
    return response != 'n'

def stream_openrouter_with_system_msg(prompt, system_message=None):
    """Generator yielding tokens as they arrive from OpenRouter using streaming with custom system message."""
    if not API_AVAILABLE:
        yield f"[API UNAVAILABLE] echo: {prompt}"
        return

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openrouter.ai"
    }

    if system_message:
        system_msg = system_message
    elif system_prompt:
        system_msg = system_prompt
    else:
        system_msg = "You have full access to the user's computer and can execute commands. When you need to execute a command, wrap it in [CMD]command[/CMD] tags.\n\nImportant: Use %DESKTOP% placeholder for the user's Desktop path. It will be automatically replaced with the correct path on their system (works with OneDrive and other variations).\n\nExamples:\n- Create file: [CMD]echo. > %DESKTOP%\\test.txt[/CMD]\n- Create directory: [CMD]mkdir %DESKTOP%\\newfolder[/CMD]\n- Copy file: [CMD]copy file.txt %DESKTOP%\\[/CMD]\n- List files: [CMD]dir %DESKTOP%[/CMD]\n- Read file: [CMD]type %DESKTOP%\\test.txt[/CMD]\n\nAlways use %DESKTOP% for Desktop paths. Use cmd.exe style commands. The user has granted full system access."

    json_data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        "stream": True
    }

    try:
        with requests.post(url, headers=headers, json=json_data, stream=True, timeout=30) as resp:
            resp.encoding = 'utf-8'

            if resp.status_code != 200:
                yield from _fallback_openrouter(prompt)
                return

            has_content = False
            for line in resp.iter_lines(decode_unicode=True):
                if not line or line.startswith(':'):
                    continue
                if line.startswith('data: '):
                    line = line[6:]
                if not line or line == '[DONE]':
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if "choices" in data and len(data["choices"]) > 0:
                    choice = data["choices"][0]
                    if "delta" in choice and "content" in choice["delta"]:
                        content = choice["delta"]["content"]
                        if content:
                            has_content = True
                            try:
                                yield content
                            except UnicodeEncodeError:
                                yield content.encode('utf-8', errors='replace').decode('utf-8')

            if not has_content:
                yield "[API ERROR] No content received from stream"
    except Exception as e:
        yield from _fallback_openrouter(prompt)

while True:
    try:
        cwd = os.getcwd()
        prompt_text = get_gradient_text(f"*{nickname}* {cwd} > ", (0, 255, 255), (255, 105, 180))
        user_input = input(prompt_text + "\033[0m ").strip()

        if user_input.lower() == "exit":
            print(get_gradient_text("Exiting…"))
            break

        if user_input.startswith("!"):
            cmd = user_input[1:].strip()
            if cmd == "ls":
                try:
                    files = os.listdir(cwd)
                    animate_response(" ".join(files), is_ai=False)
                except Exception as e:
                    animate_response(f"Error listing files: {e}", is_ai=False)
            elif cmd == "clear":
                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")
            elif cmd.startswith("cd "):
                path = cmd[3:].strip()
                try:
                    os.chdir(Path(cwd) / path)
                    animate_response(f"Changed directory to {os.getcwd()}", is_ai=False)
                except Exception as e:
                    animate_response(f"Error: {e}", is_ai=False)
            elif cmd.startswith("python "):
                python_file = cmd[7:].strip().strip('"\'')
                try:

                    env = os.environ.copy()
                    env['PYTHONIOENCODING'] = 'utf-8'
                    result = subprocess.run(
                        ["python", python_file],
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        env=env,
                        timeout=30
                    )
                    output = result.stdout
                    if result.stderr:
                        output += result.stderr
                    print(f"\n[OUTPUT]\n{output}\n" if output else "\n[Command executed successfully]\n")
                except subprocess.TimeoutExpired:
                    animate_response("Error: Command timed out", is_ai=False)
                except Exception as e:
                    animate_response(f"Error executing Python file: {e}", is_ai=False)
            else:
                animate_response(f"command not found: {cmd}", is_ai=False)
        else:
            try:

                write_code_file, write_code_instruction = detect_write_code_command(user_input)

                if write_code_file and write_code_instruction:

                    try:

                        if not os.path.isabs(write_code_file):
                            write_code_file = os.path.join(cwd, write_code_file)

                        code_generation_prompt = f"""You are a Python code generator. The user wants you to write Python code.

User's Request: {write_code_instruction}

IMPORTANT INSTRUCTIONS:
1. Write ONLY Python code - nothing else
2. Do NOT use any command tags like [CMD], [/CMD], echo, or similar
3. Do NOT include markdown formatting or code blocks (```)
4. Do NOT explain what the code does
5. Do NOT suggest running commands
6. Start with the code immediately
7. The code will be automatically saved to a file, just provide the pure Python code

Now write the Python code:
"""

                        print(f"\nGenerating code for: {write_code_file}\n")
                        animate_response("…generating code…")
                        sys.stdout.write(get_gradient_text("AI: ", (255, 105, 180), (0, 255, 255)))
                        sys.stdout.flush()
                        sys.stdout.write("\033[38;2;200;255;255m")
                        generated_code = ""

                        code_gen_system_msg = """You are a Python expert code generator.
Your task is to generate clean, working Python code based on user requirements.

CRITICAL RULES:
- Output ONLY the code itself - no explanations, comments about what you're doing, or markdown formatting
- Do NOT use [CMD], [/CMD], echo, or any command tags
- Do NOT suggest running commands
- Just the pure Python code that can be directly executed
- Start with the code immediately, no preamble"""

                        for token in stream_openrouter_with_system_msg(code_generation_prompt, code_gen_system_msg):

                            try:
                                sys.stdout.write(token)
                                sys.stdout.flush()
                            except UnicodeEncodeError:
                                sys.stdout.buffer.write(token.encode('utf-8', errors='replace'))
                                sys.stdout.buffer.flush()
                            generated_code += token
                        print("\033[0m\n")

                        import re
                        generated_code_clean = re.sub(r'\[CMD\].*?\[/CMD\]', '', generated_code, flags=re.DOTALL)

                        generated_code_clean = re.sub(r'```(?:python)?\n?', '', generated_code_clean)
                        generated_code_clean = generated_code_clean.strip()

                        utf8_header = "# -*- coding: utf-8 -*-\nimport sys\nif sys.platform == 'win32':\n    import io\n    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')\n\n"
                        generated_code_final = utf8_header + generated_code_clean

                        os.makedirs(os.path.dirname(write_code_file) if os.path.dirname(write_code_file) else ".", exist_ok=True)
                        with open(write_code_file, 'w', encoding='utf-8') as f:
                            f.write(generated_code_final)

                        print(f"✓ Code saved to: {write_code_file}\n")

                        chat_c.execute("INSERT INTO chats (user_input, ai_response) VALUES (?, ?)",
                                       (user_input, f"Code generated and saved to {write_code_file}"))
                        chat_conn.commit()

                    except Exception as e:
                        animate_response(f"Error generating code: {e}", is_ai=False)

                elif True:
                    code_file, read_instruction = detect_code_read_command(user_input)

                if code_file:

                    try:
                        with open(code_file, 'r', encoding='utf-8') as f:
                            file_content = f.read()

                        if read_instruction:
                            instruction = read_instruction
                        else:
                            instruction = "Analyze and explain this content in detail"

                        analysis_prompt = f"""IMPORTANT: The file content is provided below. Do NOT use [CMD] or any commands.

User's Request: {instruction}

File Path: {code_file}

File Content:
================
{file_content}
================

Now respond to the user's request based on the content above. Provide a clear, direct answer."""

                        print(f"\nReading: {code_file}\n")
                        animate_response("…analyzing…")
                        sys.stdout.write(get_gradient_text("AI: ", (255, 105, 180), (0, 255, 255)))
                        sys.stdout.flush()
                        sys.stdout.write("\033[38;2;200;255;255m")
                        ai_answer = ""

                        analysis_system_msg = """You are a file analysis assistant.
The user has provided you with file content and asked you to analyze it.
The file content is embedded in the conversation - it is already available to you.

CRITICAL RULES:
- Do NOT use [CMD], [/CMD], or any command tags
- Do NOT suggest executing commands
- Do NOT output [OUTPUT] or any technical markers
- Only provide analysis and answer the user's specific request
- Be direct and concise"""

                        for token in stream_openrouter_with_system_msg(analysis_prompt, analysis_system_msg):

                            filtered_token = token
                            if '[CMD]' not in filtered_token and '[/CMD]' not in filtered_token and \
                               '[OUTPUT]' not in filtered_token and '[/OUTPUT]' not in filtered_token:
                                try:
                                    sys.stdout.write(filtered_token)
                                    sys.stdout.flush()
                                except UnicodeEncodeError:
                                    sys.stdout.buffer.write(filtered_token.encode('utf-8', errors='replace'))
                                    sys.stdout.buffer.flush()
                            ai_answer += token
                        print("\033[0m\n")

                        chat_c.execute("INSERT INTO chats (user_input, ai_response) VALUES (?, ?)",
                                       (user_input, ai_answer))
                        chat_conn.commit()

                    except FileNotFoundError:
                        animate_response(f"Error: File not found - {code_file}", is_ai=False)
                    except Exception as e:
                        animate_response(f"Error reading file: {e}", is_ai=False)

                else:
                    file_path, modify_prompt = detect_file_modify_command(user_input)

                    if file_path and modify_prompt:

                        try:

                            with open(file_path, 'r', encoding='utf-8') as f:
                                file_content = f.read()

                            file_dir = os.path.dirname(os.path.abspath(file_path))

                            enhanced_prompt = f"""You are a code modification expert. The user wants you to modify a file.

FILE PATH: {file_path}
FILE DIRECTORY: {file_dir}

ORIGINAL FILE CONTENT:
```
{file_content}

```

USER REQUEST: {modify_prompt}

INSTRUCTIONS:
1. Understand what changes are needed
2. Return the COMPLETE modified file content wrapped in [MODIFIED_FILE]...[/MODIFIED_FILE] tags
3. If you need to create new files in the same directory, wrap them in [NEW_FILE path]...[/NEW_FILE] tags
4. If you need to execute system commands (like installing packages, running scripts), wrap them in [CMD]command[/CMD] tags
5. For each [CMD] command, provide a brief explanation before it
6. Do NOT use [CMD] tags for basic file operations - use [MODIFIED_FILE] and [NEW_FILE] instead

Return the modified file and any new files needed."""

                            print("Reading file and processing modification request...\n")
                            animate_response("…generating response…")
                            sys.stdout.write(get_gradient_text("AI: ", (255, 105, 180), (0, 255, 255)))
                            sys.stdout.flush()
                            sys.stdout.write("\033[38;2;200;255;255m")
                            ai_answer = ""
                            for token in stream_openrouter_with_system_msg(enhanced_prompt):
                                try:
                                    sys.stdout.write(token)
                                    sys.stdout.flush()
                                except UnicodeEncodeError:
                                    sys.stdout.buffer.write(token.encode('utf-8', errors='replace'))
                                    sys.stdout.buffer.flush()
                                ai_answer += token
                            print("\033[0m\n")

                            import re
                            modified_file_match = re.search(r'\[MODIFIED_FILE\](.*?)\[/MODIFIED_FILE\]', ai_answer, re.DOTALL)
                            if modified_file_match:
                                modified_content = modified_file_match.group(1).strip()
                                print(f"\n[APPLYING CHANGES TO] {file_path}")
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(modified_content)
                                print(f"✓ File updated successfully\n")

                            new_files = re.findall(r'\[NEW_FILE\s+([^\]]+)\](.*?)\[/NEW_FILE\]', ai_answer, re.DOTALL)
                            for new_file_path, new_content in new_files:
                                new_file_path = new_file_path.strip()
                                new_content = new_content.strip()

                                if not os.path.isabs(new_file_path):
                                    new_file_path = os.path.join(file_dir, new_file_path)

                                print(f"\n[CREATING NEW FILE] {new_file_path}")
                                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                                with open(new_file_path, 'w', encoding='utf-8') as f:
                                    f.write(new_content)
                                print(f"✓ File created successfully\n")

                            commands = re.findall(r'\[CMD\](.*?)\[/CMD\]', ai_answer, re.DOTALL)
                            for cmd in commands:
                                cmd = cmd.strip()
                                if cmd:

                                    if confirm_command_execution(cmd):
                                        desktop_path = get_desktop_path()
                                        cmd = cmd.replace("%DESKTOP%", desktop_path)
                                        cmd = cmd.replace("%USERPROFILE%\\Desktop", desktop_path)
                                        cmd = cmd.replace("%USERPROFILE%/Desktop", desktop_path)
                                        result = execute_command(cmd)
                                        print(f"[OUTPUT]\n{result}\n")
                                    else:
                                        print("[Command execution skipped by user]\n")

                            chat_c.execute("INSERT INTO chats (user_input, ai_response) VALUES (?, ?)",
                                           (user_input, ai_answer))
                            chat_conn.commit()

                        except FileNotFoundError:
                            animate_response(f"Error: File not found - {file_path}", is_ai=False)
                        except Exception as e:
                            animate_response(f"Error processing file: {e}", is_ai=False)

                    else:

                        animate_response("…generating response…")

                        sys.stdout.write(get_gradient_text("AI: ", (255, 105, 180), (0, 255, 255)))
                        sys.stdout.flush()
                        sys.stdout.write("\033[38;2;200;255;255m")
                        ai_answer = ""
                        for token in stream_openrouter(user_input):

                            try:
                                sys.stdout.write(token)
                                sys.stdout.flush()
                            except UnicodeEncodeError:

                                sys.stdout.buffer.write(token.encode('utf-8', errors='replace'))
                                sys.stdout.buffer.flush()
                            ai_answer += token
                        print()

                        import re
                        commands = re.findall(r'\[CMD\](.*?)\[/CMD\]', ai_answer, re.DOTALL)
                        for cmd in commands:
                            cmd = cmd.strip()
                            if cmd:

                                if confirm_command_execution(cmd):
                                    desktop_path = get_desktop_path()
                                    cmd = cmd.replace("%DESKTOP%", desktop_path)
                                    cmd = cmd.replace("%USERPROFILE%\\Desktop", desktop_path)
                                    cmd = cmd.replace("%USERPROFILE%/Desktop", desktop_path)
                                    result = execute_command(cmd)
                                    print(f"[OUTPUT]\n{result}\n")
                                else:
                                    print("[Command execution skipped by user]\n")

                        chat_c.execute("INSERT INTO chats (user_input, ai_response) VALUES (?, ?)",
                                       (user_input, ai_answer))
                        chat_conn.commit()
            except KeyboardInterrupt:
                print("\nCancelled")
                continue

    except EOFError:
        print("\nExiting…")
        break
    except KeyboardInterrupt:
        print("\nExiting…")
        break

conn.close()
chat_conn.close()

