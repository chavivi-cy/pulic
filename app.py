import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 页面配置
st.set_page_config(page_title="苹果逆向供应链深度决策系统", layout="wide")

# 日系雅致 CSS 增强
st.markdown("""
    <style>
    .main { background-color: #fdfdfd; }
    .stMetric { background-color: #ffffff; border-radius: 12px; border: 1px solid #d1d9e0; padding: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.03); }
    .stMetric [data-testid="stMetricValue"] { color: #2c3e50 !important; font-weight: 700; }
    h1, h2, h3 { color: #34495e; font-family: "Hiragino Sans GB", "Microsoft YaHei", sans-serif; }
    .stInfo { background-color: #f0f7f4; border: none; color: #4b635a; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部：业务基准 ---
st.title("🍏 苹果产品再制造 (Remanufacturing) 业务调研系统")
st.info("📊 **业务模型：** 以 iPhone 15 Pro (128G) 为财务基准。涵盖全品类，重点展示中国区授权分销逻辑。")

# --- 侧边栏：模拟参数 (规模大幅增强) ---
st.sidebar.header("🍃 决策因子模拟")
# 将规模扩展到 1,000,000 台量级
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
with c4: st.metric("拦截率", "99.9%", "数字化确权")

st.markdown("---")

# --- 模块二：8大课题交互面板 (视觉独立化) ---
st.header("🌿 行业专题深度调研")
qs = [
    "Q1: 商业模型解析", "Q2: 核心商业目标", "Q3: 关键成功因素(KSF)", 
    "Q4: 业务流程与分级", "Q5: 中国区出货渠道", "Q6: 目标用户画像", 
    "Q7: 跨品牌对标分析", "Q8: 为什么不碰纯二手"
]
sel_q = st.selectbox("请点选课题进行可视化演示：", qs)

# 日系清新色板定义
JP_PALETTE = ['#87adab', '#d6a0a0', '#e9c46a', '#a8dadc', '#82a1b1', '#b5c7d3']

if sel_q == qs[0]:
    st.write("### Q1: 商业模型 - 筑屋式利润结构")
    fig = go.Figure([
        go.Bar(name='回收成本', x=['核心结构'], y=[buyback_v], marker_color=JP_PALETTE[0]),
        go.Bar(name='重整增值', x=['核心结构'], y=[refurb_c+log_w], base=buyback_v, marker_color=JP_PALETTE[1]),
        go.Bar(name='净收益', x=['核心结构'], y=[profit], base=buyback_v+refurb_c+log_w, marker_color=JP_PALETTE[2])
    ])
    fig.update_layout(barmode='stack', plot_bgcolor='white', showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[1]:
    st.write("### Q2: 商业目标 - 存量留存与新客拉新 (旭日图)")
    fig = px.sunburst(
        pd.DataFrame({"cat": ["拉新", "拉新", "留存", "留存"], "sub": ["首次入iOS", "安卓切换", "存量换新", "保值回收"], "val": [25, 15, 40, 20]}),
        path=['cat', 'sub'], values='val', color_discrete_sequence=[JP_PALETTE[0], JP_PALETTE[3]]
    )
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[3]:
    st.write(f"### Q4: 业务流程 - 基于 {base_vol_k:,}k 台规模的损耗过滤")
    fig = go.Figure(go.Funnel(
        y=["回收总量", "初检通过", "原厂重整", "合格成品"], 
        x=[base_vol, base_vol*0.85, base_vol*0.80, base_vol*0.78], 
        marker={"color": JP_PALETTE}))
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[6]:
    st.write("### Q7: 1-36个月品牌残值衰减对比")
    m = [1, 6, 12, 18, 24, 30, 36]
    df = pd.DataFrame({"月份": m*4, "保持率": [95,85,71,65,58,52,45, 92,80,65,50,42,35,28, 88,75,55,45,38,30,22, 80,55,40,28,18,10,5], "品牌": ["Apple"]*7+["Huawei"]*7+["Samsung"]*7+["安卓平均"]*7})
    fig = px.line(df, x="月份", y="保持率", color="品牌", markers=True, color_discrete_map={"Apple":"#27ae60","Huawei":"#e67e22","Samsung":"#3498db","安卓平均":"#e74c3c"})
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write(f"### {sel_q}")
    st.info("该模块调研内容已动态集成至下方流转全景路径图中。")

st.markdown("---")

# --- 模块三：流转全景 ---
st.header("🌐 中国区逆向流转全景")
fig_s = go.Figure(go.Sankey(
    node = dict(pad=20, thickness=25, label=["回收源 (70%)", "退货机 (30%)", "Brightstar评估", "顺丰/逆向物流", "富士康整备", "官网直营 (15%)", "京东(45%)", "爱回收(20%)", "转转及其他(20%)"], color=[JP_PALETTE[0], JP_PALETTE[1], JP_PALETTE[2], JP_PALETTE[3], JP_PALETTE[4], "#457b9d", "#f4a261", "#fbc02d", "#ffcc80"]),
    link = dict(source=[0, 1, 2, 3, 4, 5, 5, 5, 5], target=[2, 2, 3, 4, 5, 6, 7, 8, 9], value=[70, 30, 100, 100, 100, 15, 45, 20, 20], color="rgba(225, 225, 225, 0.4)")
))
st.plotly_chart(fig_s, use_container_width=True)
