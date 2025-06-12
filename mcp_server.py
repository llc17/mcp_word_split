import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import uvicorn

# 创建FastAPI应用实例
app = FastAPI()


# 定义SSE（Server-Sent Events）端点
@app.get("/sse")
async def sse_endpoint():
    """服务器发送事件(SSE)流端点，持续向客户端推送事件"""

    # 事件生成器异步函数
    async def event_generator():
        # 初始发送心跳事件
        yield 'data: {"jsonrpc":"2.0","method":"heartbeat","params":{},"id":null}\n\n'

        # 无限循环，每5秒发送一次ping事件
        while True:
            await asyncio.sleep(5)  # 等待5秒
            yield 'data: {"jsonrpc":"2.0","method":"ping","params":{},"id":null}\n\n'

    # 返回流式响应，媒体类型为text/event-stream
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"  # SSE标准媒体类型
    )


# 定义工具处理端点（支持四则运算）
@app.post("/tools/{tool_name}")
async def tool_handler(tool_name: str, request: Request):
    """
    处理计算工具请求
    Args:
        tool_name: 工具名称（add/sub/mul/div）
        request: 包含JSON参数的请求对象
    Returns:
        JSON响应：包含计算结果或错误信息
    """
    # 解析请求体中的JSON数据
    data = await request.json()

    # 从JSON中获取参数a和b
    a = data.get("a")
    b = data.get("b")

    # 验证参数是否为整数
    if not isinstance(a, int) or not isinstance(b, int):
        return {"error": "参数 a 和 b 必须是整数"}

    # 根据工具名称执行不同的计算
    if tool_name == "add":
        result = a + b  # 加法运算
    elif tool_name == "sub":
        result = a - b  # 减法运算
    elif tool_name == "mul":
        result = a * b  # 乘法运算
    elif tool_name == "div":
        if b == 0:
            return {"error": "除数不能为0"}  # 除法零错误处理
        result = a / b  # 除法运算
    else:
        # 抛出404错误，不支持的工具
        raise HTTPException(
            status_code=404,
            detail=f"不支持的工具: {tool_name}"
        )

    # 返回计算结果
    return {"result": result}


# 主程序入口
if __name__ == "__main__":
    # 使用uvicorn运行FastAPI应用
    uvicorn.run(
        app,
        host="127.0.0.1",  # 监听本地回环地址
        port=8001  # 使用8001端口
    )