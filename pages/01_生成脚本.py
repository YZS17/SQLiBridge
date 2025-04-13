#!/usr/bin/env python3

import streamlit as st
import subprocess
import json
import os
import sys
import tempfile
from datetime import datetime
from openai import OpenAI
from config import DEFAULT_CONFIG
import proxy_generator as pg

# 设置页面标题
st.title("生成代理脚本")

# 初始化会话状态
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []
if 'last_config' not in st.session_state:
    st.session_state.last_config = {}
if 'api_key' not in st.session_state:
    st.session_state.api_key = DEFAULT_CONFIG["openai_key"]

# API配置表单
with st.expander("API配置", expanded=False):
    api_form = st.form("api_form")
    with api_form:
        api_key = st.text_input("OpenAI API Key", value=st.session_state.api_key, type="password")
        api_base = st.text_input("API Base URL", value=DEFAULT_CONFIG["api_base"])
        model = st.text_input("模型", value=DEFAULT_CONFIG["model"])
        api_submit = st.form_submit_button("保存API配置")
    
    if api_submit:
        st.session_state.api_key = api_key
        st.success("API配置已保存")

# 中转脚本工作原理说明
with st.expander("中转脚本工作原理", expanded=False):
    st.markdown("""
    ### SQL注入中转脚本工作流程
    
    1. 中转脚本通过GET参数 `s` 接收SQL注入payload
    2. 将payload进行URL编码
    3. 将编码后的payload作为目标参数发送给目标网站
    4. 捕获目标网站的响应并返回

    例如，如果SQLMap发送请求 `http://yourproxy.php?s=1 OR 1=1`，中转脚本会：
    1. 接收 `s=1 OR 1=1`
    2. 将其编码
    3. 将编码后的值作为目标参数名提交：`id=1+OR+1%3D1&Submit=Submit`
    4. 返回目标网站响应
    """)

# 主表单
with st.form("generation_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        submit_url = st.text_input(
            "提交URL", 
            value=st.session_state.last_config.get("submit_url", ""),
            help="用于提交参数的URL地址"
        )
        
        result_url = st.text_input(
            "结果URL", 
            value=st.session_state.last_config.get("result_url", ""),
            help="用于获取结果的URL地址"
        )
        
        param_name = st.text_input(
            "目标参数名称", 
            value=st.session_state.last_config.get("param_name", "id"),
            help="目标网站接收注入内容的参数名称（注入点）"
        )
    
    with col2:
        session_cookie = st.text_input(
            "会话Cookie", 
            value=st.session_state.last_config.get("session_cookie", ""),
            help="用于授权的会话Cookie"
        )
        
        method = st.selectbox(
            "HTTP方法",
            options=["POST", "GET"],
            index=0 if st.session_state.last_config.get("method", "POST") == "POST" else 1,
            help="提交参数时使用的HTTP方法"
        )
        
        output_file = st.text_input(
            "输出文件名", 
            value=st.session_state.last_config.get("output_file", "generated_proxy.php"),
            help="生成的PHP文件名"
        )
    
    st.caption("注意: 生成的中转脚本总是通过GET参数's'接收注入内容，然后将其发送到目标的参数中")
    # 提交按钮
    submitted = st.form_submit_button("生成代理脚本")
    
# 处理表单提交
if submitted:
    if not submit_url or not result_url or not session_cookie:
        st.error("提交URL、结果URL和会话Cookie为必填项")
    else:
        st.session_state.last_config = {
            "submit_url": submit_url,
            "result_url": result_url,
            "param_name": param_name,
            "session_cookie": session_cookie,
            "method": method,
            "output_file": output_file
        }
        
        with st.spinner("生成代理脚本中..."):
            try:
                # 创建带自定义配置的OpenAI客户端
                client = OpenAI(
                    api_key=st.session_state.api_key,
                    base_url=api_base
                )
                
                # 参数准备
                args = type('Args', (), {
                    "submit_url": submit_url,
                    "result_url": result_url,
                    "param_name": param_name,
                    "session_cookie": session_cookie,
                    "method": method,
                    "output_file": output_file,
                    "model": model,
                    "custom_prompt": None
                })
                
                # 配置准备
                config = {
                    "openai_key": st.session_state.api_key,
                    "api_base": api_base,
                    "model": model
                }
                
                # 生成脚本
                proxy_script = pg.generate_proxy_script(args, config)
                
                # 保存到文件
                with open(output_file, 'w') as f:
                    f.write(proxy_script)
                
                # 保存到历史记录
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.generation_history.append({
                    "timestamp": timestamp,
                    "config": st.session_state.last_config.copy(),
                    "script": proxy_script,
                    "filename": output_file
                })
                
                st.success(f"代理脚本已成功生成: {output_file}")
                st.balloons()
                
                # 使用说明
                st.info("使用方法：将生成的脚本部署到Web服务器，然后通过 `http://yourserver/脚本.php?s=注入内容` 访问")
                
                # 显示生成的代码预览
                with st.expander("生成的代码预览", expanded=True):
                    st.code(proxy_script, language="php")
                    
                    # 下载按钮
                    st.download_button(
                        label="下载PHP文件",
                        data=proxy_script,
                        file_name=output_file,
                        mime="text/php"
                    )
                
            except Exception as e:
                st.error(f"生成代理脚本时出错: {e}")
                st.exception(e)

# 显示生成历史
if st.session_state.generation_history:
    st.subheader("最近生成历史")
    
    for i, item in enumerate(reversed(st.session_state.generation_history[-5:])):
        with st.expander(f"{item['timestamp']} - {item['filename']}"):
            st.json(item['config'])
            
            # 查看按钮将跳转到查看页面
            if st.button(f"在查看页面中显示 #{i+1}", key=f"view_{i}"):
                st.session_state.view_script = item['script']
                st.session_state.view_filename = item['filename']
                st.session_state.view_config = item['config']
                st.experimental_rerun()  # 跳转到查看页面

# 添加导出所有配置的功能
if st.session_state.generation_history:
    if st.button("导出所有生成历史"):
        history_data = json.dumps(st.session_state.generation_history, indent=2)
        
        st.download_button(
            label="下载历史记录 (JSON)",
            data=history_data,
            file_name="proxy_generation_history.json",
            mime="application/json"
        ) 