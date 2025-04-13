#!/usr/bin/env python3

import streamlit as st
from config import DEFAULT_CONFIG
import SQLiBridge as sb

# 页面配置
st.set_page_config(
    page_title="SQL注入代理生成器",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 主页内容
def main():
    st.title("SQLiBridge - SQL注入中转代理生成器")
    
    st.markdown("""
    ### 🛡️ 通过大语言模型生成SQL注入代理脚本
    
    这个工具利用AI技术生成用于SQL注入测试的PHP代理脚本，无需在提示词中包含特定的技术术语。
    
    #### 使用方法:
    
    1. 在**生成页面**中填写必要的配置信息
    2. 点击生成按钮创建代理脚本
    3. 在**查看脚本**页面中预览和下载生成的PHP文件
    
    #### 功能特点:
    
    - 支持GET和POST请求方法
    - 支持自定义参数名称
    - 可配置提交和结果URL
    - 使用OpenAI API生成代码
    - 保存生成历史
    """)
    
    st.info("请在左侧导航栏选择相应的功能页面")
    
    # 显示默认API配置信息
    with st.expander("当前API配置"):
        st.code(f"""
模型: {DEFAULT_CONFIG['model']}
API Base URL: {DEFAULT_CONFIG['api_base']}
        """)
        
        st.caption("可以在config.py文件中修改默认配置")

if __name__ == "__main__":
    main() 