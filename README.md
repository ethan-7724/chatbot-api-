# chatbot-api-
一个简单的终端 AI 聊天助手，基于自定义 Chat 完成接口。

简介
----
本仓库包含一个轻量级的终端聊天助手，位于 `ai-terminal/ai.py`，通过向自定义的聊天完成接口发送会话历史来获得回复。它支持保存对话历史、在终端执行 Linux 命令（使用 `!cmd <命令>`）并将命令输出加入上下文。

主要特性
----
- 交互式终端聊天界面（支持 Markdown 渲染）
- 支持执行本地 Linux 命令并将输出写入对话历史（`!cmd` 前缀）
- 会话历史保存在 `chat_history.json` 中，可持久化上下文

先决条件
----
- Python 3.10+
- 推荐在虚拟环境中运行
- 网络访问到所配置的 API 地址

配置
----
- 在运行前，请在终端设置环境变量 `OPENAI_API_KEY`，示例：

```bash
export OPENAI_API_KEY="你的API_KEY"
```

- 默认 API 地址和模型在 `ai-terminal/ai.py` 中配置：
	- `API_URL` = `https://qywyai.com/thousand/openai/v1/chat/completions`
	- `MODEL` = `gpt-4o-mini`

运行
----
在仓库根目录运行：

```bash
python3 ai-terminal/ai.py
```

用法说明
----
- 在提示符输入自然语言问题与 AI 互动。
- 输入 `!cmd <命令>` 可以在主机上执行 Linux 命令，命令输出会显示并记录到会话中。
- 输入 `exit` 或 `quit` 退出助手。

文件结构
----
- `ai-terminal/ai.py` - 主程序，实现终端交互、API 调用与历史管理。
- `ai-terminal/chat_history.json` - 会话历史（运行时创建/更新）。
- `README.md` - 本文件。

License
----
请根据需要为本项目添加许可证（例如 MIT）。

如需扩展：可将 `API_URL`、超时时间等改为通过环境变量或命令行参数控制，以便更灵活地切换后端服务。