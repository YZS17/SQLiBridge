# SQLiBridge

这个工具使用大语言模型生成用于SQL注入测试的PHP中转代理脚本。它使用精心设计的提示词，避免包含特定的技术术语，同时生成功能完整的中转脚本。

## 中转脚本工作原理

SQL注入中转代理脚本的工作流程：

1. 注入工具（如SQLMap）向中转脚本发送请求：`http://yourserver/proxy.php?s=注入内容`
2. 中转脚本从GET参数`s`接收注入内容
3. 中转脚本对注入内容进行URL编码
4. 中转脚本将编码后的内容作为指定的目标参数发送给目标网站：`id=编码后内容&Submit=Submit`
5. 中转脚本从结果URL获取响应内容
6. 中转脚本将响应返回给注入工具

这样实现了注入工具与目标网站之间的中转，同时维持了会话状态。

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行模式

基本用法:

```bash
python SQLiBridge.py --submit-url "http://example.com/app/input.php" --result-url "http://example.com/app/results.php" --session-cookie "PHPSESSID=abcdef123456" --param-name "id" --method "POST"
```

#### 参数

- `--model`: 指定要使用的语言模型 (默认值在config.py中配置)
- `--output`或`-o`: 指定输出的PHP文件名 (默认: generated_proxy.php)
- `--submit-url`或`-s`: 参数提交URL (必需)
- `--result-url`或`-r`: 结果查看URL (必需)
- `--session-cookie`或`-c`: 会话cookie (必需)
- `--param-name`或`-p`: 目标网站的注入参数名称 (默认: "id")
- `--method`或`-m`: HTTP请求方法 (GET或POST, 默认: POST)
- `--custom-prompt`: 自定义提示词模板文件路径 (可选)

### Web界面模式

启动Web界面:

```bash
# Windows
run_streamlit.bat

# Linux/Mac
streamlit run app.py
```

Web界面提供以下功能:

1. **生成脚本**: 通过表单界面配置和生成中转脚本
2. **查看脚本**: 浏览和下载生成的脚本
3. **帮助文档**: 提供详细使用指南和常见问题解答

#### Web界面特点

- 简洁友好的用户界面
- 保存生成历史
- 直接查看和下载文件
- 详细的帮助文档

## SQLMap使用示例

将生成的中转脚本部署到Web服务器后，可以使用SQLMap进行测试：

```bash
# 基本使用方法
sqlmap -u "http://yourserver/proxy.php?s=1" --batch

# 指定测试技术
sqlmap -u "http://yourserver/proxy.php?s=1" --technique=BEUS --batch

# 获取数据库信息
sqlmap -u "http://yourserver/proxy.php?s=1" --dbs --batch
```

## 更多示例

自定义目标参数名称和HTTP方法：

```bash
python SQLiBridge.py --submit-url "http://example.com/app/input.php" --result-url "http://example.com/app/results.php" --session-cookie "PHPSESSID=abcdef123456" --param-name "query" --method "GET"
```

使用自定义模型：

```bash
python SQLiBridge.py --submit-url "http://example.com/app/input.php" --result-url "http://example.com/app/results.php" --session-cookie "PHPSESSID=abcdef123456" --model "gpt-4"
```

指定输出文件：

```bash
python SQLiBridge.py --submit-url "http://example.com/app/input.php" --result-url "http://example.com/app/results.php" --session-cookie "PHPSESSID=abcdef123456" -o my_proxy.php
```

使用自定义提示词：

```bash
python SQLiBridge.py --submit-url "http://example.com/app/input.php" --result-url "http://example.com/app/results.php" --session-cookie "PHPSESSID=abcdef123456" --custom-prompt my_prompt.txt
```

### Web-UI页面使用如下

![image-20250414010321131](https://xu17-1326239041.cos.ap-guangzhou.myqcloud.com/xu17/202504140103274.png)

![image-20250414010249596](https://xu17-1326239041.cos.ap-guangzhou.myqcloud.com/xu17/202504140102749.png)

![image-20250414010347674](https://xu17-1326239041.cos.ap-guangzhou.myqcloud.com/xu17/202504140103809.png)

### 配合`sqlmap`使用

```bash
sqlmap -u http://192.168.129.1/proxy-example.php?s=1 --dbs
```

![image-20250414011457195](https://xu17-1326239041.cos.ap-guangzhou.myqcloud.com/xu17/202504140114706.png)