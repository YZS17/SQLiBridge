#!/usr/bin/env python3

import streamlit as st
import os
import json

# 设置页面标题
st.title("查看生成的脚本")

# 初始化会话状态
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []

# 侧边栏：生成历史选择器
if st.session_state.generation_history:
    st.sidebar.header("历史记录")
    
    # 创建生成历史选择器
    history_options = [f"{h['timestamp']} - {h['filename']}" for h in st.session_state.generation_history]
    selected_history = st.sidebar.selectbox(
        "选择历史记录",
        options=history_options,
        index=len(history_options) - 1
    )
    
    # 获取选择的历史记录
    selected_index = history_options.index(selected_history)
    selected_item = st.session_state.generation_history[selected_index]
    
    # 显示所选历史记录的详细信息
    with st.sidebar.expander("配置详情"):
        st.json(selected_item['config'])
    
    # 主要内容：显示脚本
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"脚本: {selected_item['filename']}")
        st.code(selected_item['script'], language="php")
        
        # 下载按钮
        st.download_button(
            label="下载PHP文件",
            data=selected_item['script'],
            file_name=selected_item['filename'],
            mime="text/php"
        )
    
    with col2:
        st.subheader("生成信息")
        st.write(f"**生成时间**: {selected_item['timestamp']}")
        st.write(f"**提交URL**: {selected_item['config']['submit_url']}")
        st.write(f"**结果URL**: {selected_item['config']['result_url']}")
        st.write(f"**参数名称**: {selected_item['config']['param_name']}")
        st.write(f"**HTTP方法**: {selected_item['config']['method']}")

# 查看文件系统中存在的PHP文件
st.header("文件系统中的PHP文件")

# 获取当前目录中的所有PHP文件
php_files = [f for f in os.listdir() if f.endswith('.php')]

if php_files:
    selected_file = st.selectbox("选择PHP文件", php_files)
    
    if selected_file:
        try:
            with open(selected_file, 'r') as f:
                file_content = f.read()
            
            st.subheader(f"文件内容: {selected_file}")
            st.code(file_content, language="php")
            
            # 下载按钮
            st.download_button(
                label="下载PHP文件",
                data=file_content,
                file_name=selected_file,
                mime="text/php"
            )
        except Exception as e:
            st.error(f"读取文件时出错: {e}")
else:
    st.info("当前目录中没有找到PHP文件")

# 如果没有历史记录，显示提示信息
if not st.session_state.generation_history:
    st.warning('您还没有生成任何代理脚本。请前往"生成脚本"页面创建新脚本。')
    
    if st.button("去生成脚本页面"):
        st.markdown("[点击这里](/生成脚本)前往生成脚本页面") 