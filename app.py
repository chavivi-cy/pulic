import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 页面基础配置
st.set_page_config(page_title="苹果再制造业务深度决策系统", layout="wide")

# CSS 视觉增强
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }
    .stMetric [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.8rem; }
    h1, h2, h3 { color: #f8fafc; font-family: "Hiragino Sans GB", sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部声明 ---
st.title("🕊️ 苹果产品再制造 (Remanufacturing) 业务调研系统")
st.info("📊 **业务说明：** 以 iPhone 15 Pro 为财务基准。iPhone 官翻机在华主攻授权分销。")

# --- 侧边栏 ---
st.sidebar.header("🍃 决策因子")
base_vol_k = st.sidebar.slider("月流转基准规模 (k - 千台)", 1, 1000, 500)
base_vol = base_vol_k * 1000
retail_p = st.sidebar.slider("零售价 (CNY)", 4000, 9500, 6199)
buyback_r = st.sidebar.slider("回收成本占比 (%)", 50, 85, 65)
refurb_c = st.sidebar.slider("整备成本 (CNY)", 300, 1500, 750)

# 计算逻辑
buyback_v = retail_p * (buyback_r / 100)
profit = retail_p - (buyback_v + refurb_c + 480) # 480 为物流质保
margin = (profit / retail_p) * 100

# --- 核心指标看板 ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("预测利润", f"¥{profit:,.0f}", f"{margin:.1f}% 毛利")
with c2: st.metric("回收对价", f"¥{buyback_v:,.0f}", f"{buyback_r}%")
with c3: st.metric("溢价优势", "22%", "对比第三方")
with c4: st.metric("零件配对率", "99.9%", "技术拦截壁垒")

st.markdown("---")

# --- 8大课题交互区 ---
st.header("🌿 行业专题调研：交互可视化中心")
qs = ["Q1: 商业模型解析", "Q2: 核心商业目标", "Q3: 关键成功因素(KSF)", 
      "Q4: 业务流程与质量损耗", "Q5: 出货渠道份额", "Q6: 目标用户画像", 
      "Q7: 跨品牌残值对标", "Q8: 业务红线风险"]
sel_q = st.selectbox("请点选课题：", qs)

JP_COLORS = ['#87adab', '#d6a0a0', '#e9c46a', '#a8dadc', '#82a1b1']

if sel_q == qs[0]:
    st.write("### Q1: 商业模型 - 筑屋式利润堆叠图")
    fig = go.Figure([
        go.Bar(name='回收成本', x=['P&L'], y=[buyback_v], marker_color=JP_COLORS[0]),
        go.Bar(name='整备增值', x=['P&L'], y=[refurb_c+480], base=buyback_v, marker_color=JP_COLORS[1]),
        go.Bar(name='单机净利', x=['P&L'], y=[profit], base=buyback_v+refurb_c+480, marker_color=JP_COLORS[2])
    ])
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[3]:
    st.write(f"### Q4: 损耗过滤 - 基于 {base_vol_k}k 台规模 (含占比)")
    # 此处精准标注百分比
    fig = go.Figure(go.Funnel(
        y=["回收总量 (100%)", "通过初检 (85%)", "原厂重整 (80%)", "合格成品 (78%)"], 
        x=[base_vol, base_vol*0.85, base_vol*0.80, base_vol*0.78], 
        marker={"color": JP_COLORS},
        textinfo="value+percent initial"
    ))
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[6]:
    st.write("### Q7: 1-36个月品牌残值衰减对标")
    m = [1, 6, 12, 18, 24, 30, 36]
    df = pd.DataFrame({"月":m*4,"RV":[95,85,71,65,58,52,45, 92,80,65,50,42,35,28, 88,75,55,45,38,30,22, 80,55,40,28,18,10,5],"B":["Apple"]*7+["Huawei"]*7+["Samsung"]*7+["安卓平均"]*7})
    fig = px.line(df, x="月", y="RV", color="B", markers=True, color_discrete_map={"Apple":"#27ae60","Huawei":"#e67e22","Samsung":"#3498db","安卓平均":"#e74c3c"})
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write(f"### {sel_q}")
    st.info("数据分析已集成至下方流转全景。")

st.markdown("---")

# --- 流转全景 (细化货源：20% 退货率更严谨) ---
st.header("🌐 中国区逆向流转全景 (细化货源与分销占比)")
fig_s = go.Figure(go.Sankey(
    node = dict(pad=45, thickness=25, label=[
        "个人回收源 (Trade-in) (65%)", "14天退货机 (Buyer's Remorse) (20%)", "商业回收 (15%)", 
        "价值评估 (Grading)", "逆向物流", "检测整备工厂", 
        "京东自营 (45%)", "爱回收分销 (20%)", "转转及其他 (20%)", "官网直营 (15%)"
    ], color=[JP_COLORS[0], JP_COLORS[1], JP_COLORS[2], JP_COLORS[3], JP_COLORS[4], "#f4a261", "#fbc02d", "#ffcc80", "#457b9d"]),
    link = dict(source=[0, 1, 2, 3, 4, 4, 4, 4], target=[3, 3, 3, 4, 5, 6, 7, 8], value=[65, 20, 15, 100, 100, 45, 20, 20, 15], color="rgba(200, 200, 200, 0.4)")
))
st.plotly_chart(fig_s, use_container_width=True)
