from openai import OpenAI

client = OpenAI(
    api_key="sk-MmEvUuqL79t36MegRW21tXv0p7w8X0jn9ltnOjlrshVmDgKX",
    base_url="https://api.chatanywhere.tech/v1"
)


# 非流式响应
def gpt_35_api(messages: list):
    """为提供的对话消息创建新的回答

    Args:
        messages (list): 完整的对话消息
    """
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def gpt_35_api_stream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
    """
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

if __name__ == '__main__':
    messages = [{'role': 'user','content': '写个100字的故事'},]
    # 非流式调用
    a = gpt_35_api(messages)
    print(a)
