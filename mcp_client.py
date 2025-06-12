import asyncio
import re
import json
import aiohttp


# 定义提取计算操作的函数
def extract_calculation(text: str):
    """从文本中提取算术运算表达式
    Args:
        text: 用户输入的文本字符串
    Returns:
        元组 (操作类型, 第一个数字, 第二个数字) 或 None（未识别）
    """
    # 使用正则表达式提取文本中的所有数字
    numbers = list(map(int, re.findall(r'\d+', text)))

    # 如果找到的数字少于2个，返回None
    if len(numbers) < 2:
        return None

    # 根据中文关键词判断运算类型
    if "加" in text:
        return ("add", numbers[0], numbers[1])  # 加法
    elif "减" in text:
        return ("sub", numbers[0], numbers[1])  # 减法
    elif "乘" in text:
        return ("mul", numbers[0], numbers[1])  # 乘法
    elif "除" in text:
        return ("div", numbers[0], numbers[1])  # 除法
    else:
        return None  # 未识别到有效运算


# 定义提取中英文字符的函数
def extract_chinese_and_english_chars(text: str):
    """提取文本中的中文字符和英文字母
    Args:
        text: 用户输入的文本字符串
    Returns:
        匹配到的字符列表（中文汉字或英文字母）
    """
    # 正则表达式匹配：中文Unicode范围 \u4e00-\u9fff，英文A-Za-z
    pattern = r'[\u4e00-\u9fffA-Za-z]'
    return re.findall(pattern, text)


# 主异步函数
async def main():
    """主交互逻辑"""
    server_base = "http://127.0.0.1:8001"  # MCP服务器基础地址
    print("你好，我是你的助手！如果输入 '退出' 将结束对话。")

    # 创建aiohttp客户端会话
    async with aiohttp.ClientSession() as session:
        # 持续交互循环
        while True:
            user_input = input("用户: ").strip()  # 获取用户输入

            # 退出条件检测（支持多语言退出命令）
            if user_input.lower() in ["退出", "quit", "exit"]:
                print("助手已退出")
                break

            # 尝试提取计算操作
            calc = extract_calculation(user_input)
            if calc:
                op, a, b = calc  # 解构操作类型和操作数
                url = f"{server_base}/tools/{op}"  # 构造API请求URL
                payload = {"a": a, "b": b}  # 构造请求负载

                try:
                    # 发送POST请求到计算服务
                    async with session.post(url, json=payload) as resp:
                        data = await resp.json()  # 解析JSON响应

                        # 成功处理响应
                        if resp.status == 200 and "result" in data:
                            # 构造调试输出信息
                            debug_output = json.dumps(
                                {"tool": op, "arguments": payload, "result": data["result"]},
                                ensure_ascii=False  # 允许显示非ASCII字符
                            )
                            print(f"DEBUG: LLM 响应原文 -> {debug_output}")
                        else:
                            # 处理异常响应
                            print(f"助手: 计算调用失败，状态码 {resp.status}，返回：{data}")
                except Exception as e:
                    # 处理网络或JSON解析错误
                    print(f"助手: 发生错误: {e}")
                continue  # 跳过后续处理

            # 提取中英文字符
            chars = extract_chinese_and_english_chars(user_input)
            if chars:
                # 生成字符提取的调试输出
                debug_output = json.dumps({"characters": chars}, ensure_ascii=False)
                print(f"DEBUG: LLM 响应原文 -> {debug_output}")
            else:
                # 未识别到有效内容
                print("助手: 未识别到计算相关关键字或中英文字符")


# 程序入口
if __name__ == "__main__":
    # 启动异步主函数
    asyncio.run(main())