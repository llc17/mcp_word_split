# mcp_word_split
纪念第一次接触mcp
🧠 MCP 工具调用演示系统
这是一个使用 Python 构建的本地 MCP 架构模拟示例，分为客户端和服务端两部分：

客户端：输入自然语言问题（如“88加99是多少”，“今天成都的天气怎么样”，“hello”），数字将进行拆分并给出结果，其他劲进行拆分

服务端：提供 add、sub、mul、div 四种基础计算工具接口供客户端调用。

📦 环境依赖
使用前请确保你已安装以下 Python 依赖包：

bash
复制
编辑
pip install fastapi aiohttp uvicorn
📁 项目结构
bash
复制
编辑
mcp_demo/
├── mcp_client.py    # 客户端：处理用户输入、调用工具接口、打印结果
└── mcp_server.py    # 服务端：提供加减乘除工具 API
🚀 使用方法
1. 启动服务端
在终端中运行：

bash
复制
编辑
python mcp_server.py
服务端将启动在 http://127.0.0.1:8001，暴露以下接口：

POST /tools/add

POST /tools/sub

POST /tools/mul

POST /tools/div

2. 启动客户端
在另一个终端中运行：

bash
复制
编辑
python mcp_client.py
你将看到：

bash
复制
编辑
开始交互，输入 '退出' 结束。
用户:
输入示例问题：

makefile
复制
编辑
用户: 888加999是多少
你将看到：

css
复制
编辑
DEBUG: LLM 响应原文 -> {"tool": "add", "arguments": {"a": 888, "b": 999}, "result": 1887}
💡 支持功能
✅ 中文自然语言中提取运算（加、减、乘、除）

✅ 自动调用对应计算工具接口

✅ 解析并打印返回 JSON（DEBUG 样式）

✅ 如果不是计算任务，提取所有中英文字符

⚠️ 注意事项
Python 版本推荐 ≥ 3.7

所有计算工具接口都需提供整数参数 { "a": int, "b": int }

除法操作时 b 不可为 0

客户端与服务端需在同一台机器或局域网中运行，默认使用 127.0.0.1:8001 地址通信

📜 License
MIT License（可根据你的实际需求自定义）

如果你还需要部署成 Web 页面或接入真实大模型 API，可以在此基础上继续扩展。是否需要我为你生成一个完整的 README.md 文件？








