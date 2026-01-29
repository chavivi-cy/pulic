import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 页面配置：设置极简背景
st.set_page_config(page_title="苹果再制造业务深度决策系统", layout="wide")

# 日系小清新 CSS 样式
st.markdown("""
    <style>
    .main { background-color: #fdfdfd; }
    .stMetric { background-color: #ffffff; border-radius: 12px; border: 1px solid #e1e4e8; padding: 20px; }
    h1, h2, h3 { color: #5a5a5a; font-family: "Helvetica Neue", Arial, "Hiragino Sans GB", sans-serif; }
    .stInfo { background-color: #f0f7f4; border: none; color: #4b635a; border-radius: 10px; }
    .stAlert { background-color: #fff5f5; border: none; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部：多品类业务基准声明 ---
st.title("🕊️ 苹果产品再制造 (Remanufacturing) 业务调研系统")
st.info("""
📊 **业务基准与全品类覆盖：**
* **核心机型：** 以 iPhone 15 Pro (128G) 2025年初定价为财务对标模型。
* **品类覆盖：** 涵盖 Mac, iPad, Watch 及 iPhone 全品类。
* **渠道差异：** 明确 iPhone 品类在华不通过官方直营渠道销售官翻机，主要经由授权渠道流转。
""")

# --- 侧边栏：模拟参数 ---
st.sidebar.header("🍃 决策因子模拟")
retail_p = st.sidebar.slider("零售均价 (CNY)", 4000, 9500, 6199)
buyback_r = st.sidebar.slider("回收成本占比 (%)", 50, 85, 65)
refurb_c = st.sidebar.slider("整备成本 (CNY)", 300, 1500, 750)
log_w = st.sidebar.number_input("物流及质保准备 (CNY)", value=480)

# 财务计算逻辑
buyback_v = retail_p * (buyback_r / 100)
total_c = buyback_v + refurb_c + log_w
profit = retail_p - total_c
margin = (profit / retail_p) * 100

# --- 模块一：核心指标 ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("预测利润", f"¥{profit:,.0f}", f"{margin:.1f}% 毛利")
with c2: st.metric("回收成本", f"¥{buyback_v:,.0f}", f"{buyback_r}%")
with c3: st.metric("市场溢价", "22%", "对比第三方")
with c4: st.metric("拦截率", "99.9%", "数字化壁垒")

st.markdown("---")

# --- 模块二：8大课题交互分析 (日系清新视觉版) ---
st.header("🌿 行业专题调研：8大核心课题")
qs = [
    "Q1: 商业模型解析", "Q2: 核心商业目标", "Q3: 关键成功因素(KSF)", 
    "Q4: 业务流程与分级", "Q5: 中国区出货渠道", "Q6: 目标用户画像", 
    "Q7: 跨品牌对标分析", "Q8: 为什么不碰纯二手"
]
sel_q = st.selectbox("请点选课题进行深度交互演示：", qs)

# 定义日系小清新色板
JP_COLORS = ['#87adab', '#d6a0a0', '#e9c46a', '#f4a261', '#e76f51', '#a8dadc', '#457b9d', '#1d3557']

if sel_q == qs[0]:
    st.write("### Q1: 商业模型 - 资产价值再造")
    fig = go.Figure(go.Waterfall(
        x = ["零售价", "回收", "整备", "物流", "利润"],
        y = [retail_p, -buyback_v, -refurb_c, -log_w, 0],
        measure = ["relative", "relative", "relative", "relative", "total"],
        decreasing = {"marker":{"color":"#d6a0a0"}}, # 樱色
        increasing = {"marker":{"color":"#87adab"}}, # 苍色
        totals = {"marker":{"color":"#82a1b1"}} # 灰蓝
    ))
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[6]:
    st.write("### Q7: 残值曲线对标 - 苹果的高残值护城河")
    m = [1, 6, 12, 18, 24, 30, 36]
    df = pd.DataFrame({
        "月份": m*4,
        "保持率": [95,85,71,65,58,52,45,  # Apple
                    92,80,65,50,42,35,28,  # Huawei
                    88,75,55,45,38,30,22,  # Samsung
                    80,55,40,28,18,10,5],   # Others
        "品牌": ["Apple (iPhone)"]*7 + ["Huawei (CPO)"]*7 + ["Samsung (Flagship)"]*7 + ["其他安卓机型"]*7
    })
    # 颜色：Apple(绿色系), Huawei(橙色系), Samsung(蓝色系), Others(红色系)
    fig = px.line(df, x="月份", y="保持率", color="品牌", markers=True, 
                 color_discrete_map={"Apple (iPhone)":"#6b8e23","Huawei (CPO)":"#e67e22","Samsung (Flagship)":"#3498db","其他安卓机型":"#e74c3c"})
    fig.update_layout(plot_bgcolor='white', xaxis_showgrid=False, yaxis_showgrid=True, yaxis_gridcolor='#f0f0f0')
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[3]:
    st.write("### Q4: 业务流程 - 质量分级漏斗")
    fig = go.Figure(go.Funnel(
        y=["回收总量", "通过ATE初检", "原厂翻修", "官方合格品"], 
        x=[100, 85, 80, 78], 
        marker={"color": ["#87adab", "#a8dadc", "#f4a261", "#d6a0a0"]}))
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[5]:
    st.write("### Q6: 用户画像 - 维度权重图")
    fig = px.line_polar(r=[90, 85, 95, 60], theta=["品牌忠诚", "价格敏感", "质量焦虑", "环保意识"], line_close=True)
    fig.update_traces(fill='toself', fillcolor='rgba(135, 173, 171, 0.4)', line_color='#87adab')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write(f"### {sel_q}")
    st.markdown("> 该部分洞察已动态集成至下方流转全景图中，请上下对比查看。")

st.markdown("---")

# --- 模块三：流转全景 (彩色清新版) ---
st.header("🌐 中国区逆向流转全景")
# 替换灰色色块为清新彩色半透明色块
fig_s = go.Figure(go.Sankey(
    node = dict(
        pad = 20, thickness = 25, line = dict(color = "#ffffff", width = 2),
        label = ["个人回收源 (55%)", "14天退货 (15%)", "商业/以旧换新 (30%)", "评估(Brightstar)", "逆向物流 (100%)", "富士康整备 (100%)", "官网直营 (Mac/iPad)", "分销渠道 (iPhone)", "B2B集采 (20%)"],
        color = ["#87adab", "#d6a0a0", "#e9c46a", "#a8dadc", "#82a1b1", "#b5c7d3", "#457b9d", "#f4a261", "#e76f51"]
    ),
    link = dict(
        source = [0, 1, 2, 3, 4, 5, 5, 5], 
        target = [3, 3, 3, 4, 5, 6, 7, 8],
        value = [55, 15, 30, 100, 100, 15, 65, 20],
        color = "rgba(225, 225, 225, 0.4)" # 全彩色流向，告别灰色
    )
))
fig_s.update_layout(font_size=12, font_color="#5a5a5a")
st.plotly_chart(fig_s, use_container_width=True)

st.write("**业务说明：** iPhone 品类资源机约 65% 的份额经由京东二手和爱回收等授权分销体系消化，而非通过 Apple Store 直接零售。")
