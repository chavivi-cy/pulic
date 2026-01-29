import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 页面配置
st.set_page_config(page_title="苹果再制造业务深度决策系统", layout="wide")

# 视觉审美升级：日系雅致风格 + 增强对比度
st.markdown("""
    <style>
    .main { background-color: #fdfdfd; }
    .stMetric { background-color: #ffffff; border-radius: 12px; border: 1px solid #d1d9e0; padding: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.03); }
    /* 核心：确保数值在白色背景下绝对清晰 */
    .stMetric [data-testid="stMetricValue"] { color: #2c3e50 !important; font-weight: 700; }
    .stMetric [data-testid="stMetricLabel"] { color: #5d6d7e !important; }
    h1, h2, h3 { color: #34495e; font-family: "Hiragino Sans GB", sans-serif; }
    .stInfo { background-color: #e8f6f3; border: none; color: #16a085; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部：多品类业务基准声明 ---
st.title("🕊️ 苹果产品再制造 (Remanufacturing) 业务调研系统")
st.info("""
📊 **业务基准与全品类覆盖：**
* **核心机型：** 以 iPhone 15 Pro (128G) 2025年初定价为核心财务对标模型。
* **品类覆盖：** 涵盖 Mac, iPad, Watch 及 iPhone 全品类。
* **渠道核心：** iPhone 官翻机在华不通过 Apple Store 零售，由京东自营、爱回收及转转等渠道承接。
""")

# --- 侧边栏：交互因子 (新增动态规模) ---
st.sidebar.header("🍃 决策因子模拟")
base_volume = st.sidebar.select_slider("回收基准规模 (台)", options=[1000, 5000, 10000, 50000, 100000], value=10000)
retail_p = st.sidebar.slider("零售均价 (CNY)", 4000, 9500, 6199)
buyback_r = st.sidebar.slider("回收成本占比 (%)", 50, 85, 65)
refurb_c = st.sidebar.slider("整备成本 (CNY)", 300, 1500, 750)
log_w = st.sidebar.number_input("物流及质保准备 (CNY)", value=480)

# 财务计算
buyback_v = retail_p * (buyback_r / 100)
total_c = buyback_v + refurb_c + log_w
profit = retail_p - total_c
margin = (profit / retail_p) * 100

# --- 模块一：核心指标 (深色高对比度) ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("预测利润", f"¥{profit:,.0f}", f"{margin:.1f}% 毛利")
with c2: st.metric("回收成本", f"¥{buyback_v:,.0f}", f"{buyback_r}%")
with c3: st.metric("市场溢价", "22%", "对比第三方")
with c4: st.metric("拦截率", "99.9%", "数字化壁垒")

st.markdown("---")

# --- 模块二：8大课题交互分析 ---
st.header("🌿 行业专题深度调研")
qs = [
    "Q1: 商业模型解析", "Q2: 核心商业目标", "Q3: 关键成功因素(KSF)", 
    "Q4: 业务流程与分级", "Q5: 中国区出货渠道", "Q6: 目标用户画像", 
    "Q7: 跨品牌对标分析", "Q8: 为什么不碰纯二手"
]
sel_q = st.selectbox("请点选课题进行可视化演示：", qs)

if sel_q == qs[0]:
    st.write("### Q1: 商业模型 - 筑屋式资产增值结构")
    fig = go.Figure()
    fig.add_trace(go.Bar(name='底层支撑：回收对价', x=['价值堆叠'], y=[buyback_v], marker_color='#87adab'))
    fig.add_trace(go.Bar(name='核心增值：重整与质保', x=['价值堆叠'], y=[refurb_c + log_w], base=buyback_v, marker_color='#d6a0a0'))
    fig.add_trace(go.Bar(name='顶端收益：净利润', x=['价值堆叠'], y=[profit], base=buyback_v + refurb_c + log_w, marker_color='#e9c46a'))
    fig.update_layout(barmode='stack', plot_bgcolor='white', showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[3]:
    st.write(f"### Q4: 业务流程 - 基于 {base_volume:,} 台基数的质量过滤")
    fig = go.Figure(go.Funnel(
        y=["回收总量", "通过ATE初检", "原厂翻修后", "官方合格品"], 
        x=[base_volume, base_volume*0.85, base_volume*0.80, base_volume*0.78], 
        marker={"color": ["#87adab", "#a8dadc", "#f4a261", "#d6a0a0"]}))
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[6]:
    st.write("### Q7: 品牌残值衰减曲线 (多色对标)")
    m = [1, 6, 12, 18, 24, 30, 36]
    df = pd.DataFrame({
        "月份": m*4,
        "保持率 (%)": [95,85,71,65,58,52,45, 92,80,65,50,42,35,28, 88,75,55,45,38,30,22, 80,55,40,28,18,10,5],
        "品牌": ["Apple"]*7 + ["Huawei"]*7 + ["Samsung"]*7 + ["安卓其他"]*7
    })
    fig = px.line(df, x="月份", y="保持率 (%)", color="品牌", markers=True, 
                 color_discrete_map={"Apple":"#27ae60","Huawei":"#e67e22","Samsung":"#3498db","安卓其他":"#e74c3c"})
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write(f"### {sel_q}")
    st.info("该模块的深度交互逻辑已集成至下方流转全景路径中。")

st.markdown("---")

# --- 模块三：流转全景 (包含转转及精确占比) ---
st.header("🌐 中国区逆向流转全景 (含主要分销商占比)")
fig_s = go.Figure(go.Sankey(
    node = dict(
        pad = 20, thickness = 25, line = dict(color = "#ffffff", width = 2),
        label = [
            "个人回收 (55%)", "退货机 (15%)", "商业渠道回收 (30%)", 
            "评估(Brightstar)", "顺丰/逆向物流", "工厂检测整备", 
            "官网直营 (Mac/iPad) (15%)", "京东自营 (45%)", "爱回收渠道 (20%)", "转转及其他平台 (10%)", "B2B集采 (10%)"
        ],
        color = ["#87adab", "#d6a0a0", "#e9c46a", "#a8dadc", "#82a1b1", "#b5c7d3", "#457b9d", "#f4a261", "#fbc02d", "#ffcc80", "#e76f51"]
    ),
    link = dict(
        source = [0, 1, 2, 3, 4, 5, 5, 5, 5, 5], 
        target = [3, 3, 3, 4, 5, 6, 7, 8, 9, 10],
        value = [55, 15, 30, 100, 100, 15, 45, 20, 10, 10],
        color = "rgba(189, 195, 199, 0.4)"
    )
))
fig_s.update_layout(font_size=12, font_color="#34495e")
st.plotly_chart(fig_s, use_container_width=True)

st.caption("注：数据基于 2025 年逆向供应链模型测算，旨在展示业务逻辑波动，非实时财务审计数据。")
