#!/usr/bin/env python3
import os
import json
import subprocess
import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

# ---------- 配置 ----------
API_KEY = os.environ.get("OPENAI_API_KEY")
API_URL = "https://qywyai.com/thousand/openai/v1/chat/completions"
MODEL = "gpt-4o-mini"       # 接口支持的模型
MAX_TOKENS = 10000
HISTORY_FILE = "chat_history.json"  # 保存历史记录
# -------------------------

# 加载历史对话
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        session_messages = json.load(f)
else:
    session_messages = [
        {"role": "system", "content": "你是一个好用的终端助手，可以回答问题、帮助用户执行Linux命令，并提供建议。"}
    ]

def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(session_messages, f, ensure_ascii=False, indent=2)

def run_command(cmd: str):
    """执行 Linux 命令并返回输出，同时保存到上下文"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        output = result.stdout.strip() or result.stderr.strip()
        # 保存命令和输出到上下文
        session_messages.append({
            "role": "system",
            "content": f"用户执行命令: {cmd}\n输出结果:\n{output}"
        })
        save_history()
        return output
    except Exception as e:
        return f"命令执行错误: {e}"

def chat():
    console.print(Panel.fit("[bold green]AI Terminal Assistant (Advanced, Custom API)[/bold green]\n"
                            "[yellow]输入 exit 或 quit 退出助手 | 输入 !cmd <命令> 执行 Linux 命令[/yellow]"))

    while True:
        prompt = input("You: ").strip()
        if prompt.lower() in ["exit", "quit"]:
            console.print("[bold red]退出助手[/bold red]")
            break

        # 命令模式
        if prompt.startswith("!cmd "):
            cmd = prompt[5:]
            output = run_command(cmd)
            console.print(Panel(f"[magenta]{output}[/magenta]", title="命令输出", expand=False))
            continue

        # 保存用户消息到上下文
        session_messages.append({"role": "user", "content": prompt})
        save_history()

        try:
            # 调用自定义 API
            response = requests.post(
                API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                },
                json={
                    "model": MODEL,
                    "max_tokens": MAX_TOKENS,
                    "messages": session_messages
                },
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                answer = data["choices"][0].get("message", {}).get("content") \
                         or data["choices"][0].get("text", "")
            else:
                answer = "接口返回格式异常"

            # 保存 AI 回复到上下文
            session_messages.append({"role": "assistant", "content": answer})
            save_history()

            # 彩色打印 AI 回复，支持 Markdown
            console.print(Markdown(f"**AI:** {answer}"))

        except Exception as e:
            console.print(f"[bold red]错误:[/bold red] {e}")

if __name__ == "__main__":
    if not API_KEY:
        console.print("[bold red]请先在终端设置环境变量 OPENAI_API_KEY[/bold red]")
        console.print("示例: export OPENAI_API_KEY='你的API_KEY'")
    else:
        chat()
