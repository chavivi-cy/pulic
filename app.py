import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 页面基础配置
st.set_page_config(page_title="苹果再制造业务深度决策系统", layout="wide")

# 日系雅致 CSS 增强：解决字体对比度与布局问题
st.markdown("""
    <style>
    .main { background-color: #fdfdfd; }
    .stMetric { background-color: #ffffff; border-radius: 12px; border: 1px solid #d1d9e0; padding: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.03); }
    .stMetric [data-testid="stMetricValue"] { color: #2c3e50 !important; font-weight: 700; }
    h1, h2, h3 { color: #34495e; font-family: "Hiragino Sans GB", "Microsoft YaHei", sans-serif; }
    .stInfo { background-color: #f0f7f4; border: none; color: #4b635a; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部：业务声明 ---
st.title("🕊️ 苹果产品再制造 (Remanufacturing) 业务调研系统")
st.info("📊 **业务基准：** 以 iPhone 15 Pro (128G) 为财务模型。包含 Mac/iPad 等品类，中国区 iPhone 官翻主攻授权渠道流转。")

# --- 侧边栏：模拟参数 ---
st.sidebar.header("🍃 决策因子")
base_vol_k = st.sidebar.slider("回收基准规模 (k - 千台)", 1, 1000, 500)
base_vol = base_vol_k * 1000

retail_p = st.sidebar.slider("零售均价 (CNY)", 4000, 9500, 6199)
buyback_r = st.sidebar.slider("回收成本占比 (%)", 50, 85, 65)
refurb_c = st.sidebar.slider("整备成本 (CNY)", 300, 1500, 750)
log_w = st.sidebar.number_input("物流及质保准备 (CNY)", value=480)

# 财务计算
buyback_v = retail_p * (buyback_r / 100)
profit = retail_p - (buyback_v + refurb_c + log_w)
margin = (profit / retail_p) * 100

# --- 模块一：核心指标 ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("预测利润", f"¥{profit:,.0f}", f"{margin:.1f}% 毛利")
with c2: st.metric("回收成本", f"¥{buyback_v:,.0f}", f"{buyback_r}%")
with c3: st.metric("市场溢价", "22%", "对比第三方二手")
with c4: st.metric("拦截率", "99.9%", "数字化壁垒指标")

st.markdown("---")

# --- 模块二：8大课题交互面板 (视觉完全独立化) ---
st.header("🌿 行业专题调研：交互视觉中心")
qs = [
    "Q1: 商业模型解析", "Q2: 核心商业目标分析", "Q3: 关键成功因素(KSF)", 
    "Q4: 业务流程与质量损耗", "Q5: 中国区出货渠道份额", "Q6: 目标用户画像多维分析", 
    "Q7: 跨品牌残值衰减对标", "Q8: 业务红线风险矩阵"
]
sel_q = st.selectbox("请点选调研课题查看详细数据视觉呈现：", qs)

JP_PALETTE = ['#87adab', '#d6a0a0', '#e9c46a', '#a8dadc', '#82a1b1', '#b5c7d3']

if sel_q == qs[0]:
    st.write("### Q1: 商业模型 - 筑屋式利润价值堆叠")
    fig = go.Figure([
        go.Bar(name='回收对价', x=['价值构成'], y=[buyback_v], marker_color=JP_PALETTE[0]),
        go.Bar(name='重整成本', x=['价值构成'], y=[refurb_c+log_w], base=buyback_v, marker_color=JP_PALETTE[1]),
        go.Bar(name='单机利润', x=['价值构成'], y=[profit], base=buyback_v+refurb_c+log_w, marker_color=JP_PALETTE[2])
    ])
    fig.update_layout(barmode='stack', plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[1]:
    st.write("### Q2: 商业目标 - LTV 生命周期价值分布")
    fig = px.sunburst(pd.DataFrame({"A":["拉新","拉新","留存","留存"],"B":["首次购机","安卓切换","旧机换新","服务订阅"],"V":[20,15,45,20]}), path=['A','B'], values='V', color_discrete_sequence=[JP_PALETTE[0], JP_PALETTE[3]])
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[2]:
    st.write("### Q3: 关键成功因素 - 技术确权与壁垒维度")
    df
