import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 页面基础配置
st.set_page_config(page_title="苹果逆向供应链深度决策系统", layout="wide")

# 自定义视觉风格
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; border-radius: 10px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h2, h3 { color: #1e293b; border-bottom: 2px solid #228B22; padding-bottom: 8px; }
    .insight-box { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #228B22; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部：业务基准声明 ---
st.title("🍏 苹果产品再制造 (Remanufacturing) 业务深度调研看板")
st.info("📊 **业务基准：** 以 iPhone 15 Pro (128G) 在 2025 年初翻新市场定价为核心计算模型")

# --- 侧边栏：交互因子 ---
st.sidebar.header("⚙️ 模拟参数 (用于损益测算)")
retail_price = st.sidebar.slider("翻新零售均价 (CNY)", 4000, 9500, 6199)
buyback_rate = st.sidebar.slider("回收成本占比 (%)", 50, 85, 65)
refurb_cost = st.sidebar.slider("整备及备件成本 (CNY)", 300, 1500, 750)
log_warranty = st.sidebar.number_input("逆向物流及质保金 (CNY)", value=480)

# 财务逻辑计算
buyback_val = retail_price * (buyback_rate / 100)
total_cost = buyback_val + refurb_cost + log_warranty
net_profit = retail_price - total_cost
margin_pct = (net_profit / retail_price) * 100

# --- 模块一：核心指标看板 ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("预测单机利润", f"¥{net_profit:,.0f}", f"毛利 {margin_pct:.1f}%")
c2.metric("回收成本锚点", f"¥{buyback_val:,.0f}", f"占比 {buyback_rate}%")
c3.metric("市场流转溢价", "22%", "对比社会二手")
c4.metric("技术校验拦截率", "99.9%", "零件配对壁垒")

st.markdown("---")

# --- 模块二：8大课题交互式深度调研面板 ---
st.header("🔍 8大课题专家深度洞察 (交互选择)")

questions = [
    "Q1: 翻新业务的商业模型",
    "Q2: 核心商业目标分析",
    "Q3: 关键成功因素(KSF)",
    "Q4: 业务流程与质量标准",
    "Q5: 中国区主要出货渠道",
    "Q6: 目标用户画像分析",
    "Q7: 对标安卓厂商的可行性",
    "Q8: 为什么不参与纯二手业务"
]

selected_q = st.selectbox("请选择您想要深入了解的课题：", questions)

# 交互逻辑：根据选择显示内容
if selected_q == questions[0]:
    col_q1_a, col_q1_b = st.columns([1, 1])
    with col_q1_a:
        st.write("### 商业模型：资产价值再造")
        st.write("核心在于利用 **20% 的官方溢价** 覆盖 **12% 的重整成本**。通过控制逆向供应链，将废旧资产转化为高毛利的标准商品。")
    with col_q1_b:
        fig = go.Figure(go.Waterfall(
            orientation = "v",
            x = ["零售价", "回收", "整备",
