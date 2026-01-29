import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 页面配置
st.set_page_config(page_title="苹果逆向供应链深度决策系统", layout="wide")

# 视觉审美升级：日系雅致风格
st.markdown("""
    <style>
    .main { background-color: #fdfdfd; }
    /* 解决白底看不清数字的问题：调深文字颜色并增强对比度 */
    .stMetric { background-color: #ffffff; border-radius: 12px; border: 1px solid #d1d9e0; padding: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.03); }
    .stMetric [data-testid="stMetricValue"] { color: #2c3e50 !important; font-weight: 700; }
    .stMetric [data-testid="stMetricLabel"] { color: #5d6d7e !important; }
    h1, h2, h3 { color: #34495e; font-family: "Hiragino Sans GB", sans-serif; }
    .stInfo { background-color: #e8f6f3; border: none; color: #16a085; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部：业务基准声明 ---
st.title("🕊️ 苹果产品再制造 (Remanufacturing) 业务调研系统")
st.info("""
📊 **业务基准与全品类覆盖：**
* **核心机型：** 以 iPhone 15 Pro (128G) 2025年初定价为模型。
* **品类覆盖：** 涵盖 Mac, iPad, Watch 及 iPhone 全品类。
* **渠道核心：** 明确 iPhone 官翻机在华主要经由授权分销渠道流转。
""")

# --- 侧边栏：模拟参数 ---
st.sidebar.header("🍃 决策因子")
retail_p = st.sidebar.slider("零售均价 (CNY)", 4000, 9500, 6199)
buyback_r = st.sidebar.slider("回收成本占比 (%)", 50, 85, 65)
refurb_c = st.sidebar.slider("整备成本 (CNY)", 300, 1500, 750)
log_w = st.sidebar.number_input("物流及质保准备 (CNY)", value=480)

# 财务计算逻辑
buyback_v = retail_p * (buyback_r / 100)
total_c = buyback_v + refurb_c + log_w
profit = retail_p - total_c
margin = (profit / retail_p) * 100

# --- 模块一：核心指标 (深色文字版) ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("预测利润", f"¥{profit:,.0f}", f"{margin:.1f}% 毛利")
with c2: st.metric("回收成本", f"¥{buyback_v:,.0f}", f"{buyback_r}%")
with c3: st.metric("市场溢价", "22%", "对比第三方")
with c4: st.metric("拦截率", "99.9%", "数字化壁垒")

st.markdown("---")

# --- 模块二：8大课题交互分析 (多样化图表版) ---
st.header("🌿 行业专题深度调研")
qs = [
    "Q1: 商业模型解析", "Q2: 核心商业目标", "Q3: 关键成功因素(KSF)", 
    "Q4: 业务流程与分级", "Q5: 中国区出货渠道", "Q6: 目标用户画像", 
    "Q7: 跨品牌对标分析", "Q8: 为什么不碰纯二手"
]
sel_q = st.selectbox("请点选课题进行可视化演示：", qs)

if sel_q == qs[0]:
    st.write("### Q1: 商业模型分析 (筑屋图结构)")
    # 使用筑屋图逻辑展示：地基、支柱与顶端利润
    fig = go.Figure()
    # 底部：回收对价
    fig.add_trace(go.Bar(name='底层支撑：回收对价', x=['商业模型结构'], y=[buyback_v], marker_color='#87adab'))
    # 中间：重整价值
    fig.add_trace(go.Bar(name='核心溢价：重整与增值', x=['商业模型结构'], y=[refurb_c + log_w], base=buyback_v, marker_color='#d6a0a0'))
    # 顶部：净利润
    fig.add_trace(go.Bar(name='顶端收益：净利润', x=['商业模型结构'], y=[profit], base=buyback_v + refurb_c + log_w, marker_color='#e9c46a'))
    fig.update_layout(barmode='stack', plot_bgcolor='white', title="商业模型价值堆叠图")
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[1]:
    st.write("### Q2: 商业目标 - 存量与新客比例 (环形图)")
    fig = px.pie(names=['首次入坑新客', '老客升级'], values=[35, 65], hole=0.6, color_discrete_sequence=['#87adab', '#d6a0a0'])
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[3]:
    st.write("### Q4: 业务流程 - 质量过滤漏斗")
    fig = go.Figure(go.Funnel(
        y=["回收总量", "通过ATE初检", "原厂翻修后", "官方合格品"], 
        x=[10000, 8500, 8000, 7800], 
        marker={"color": ["#87adab", "#a8dadc", "#f4a261", "#d6a0a0"]}))
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[5]:
    st.write("### Q6: 用户画像分析 (雷达图)")
    fig = px.line_polar(r=[90, 85, 95, 60], theta=["品牌忠诚", "价格敏感", "质量焦虑", "环保意识"], line_close=True)
    fig.update_traces(fill='toself', fillcolor='rgba(135, 173, 171, 0.4)', line_color='#87adab')
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
    st.info("该模块深度洞察已集成至下方流转全景图中。")

st.markdown("---")

# --- 模块三：流转全景 (标注具体的销售商及占比) ---
st.header("🌐 中国区逆向流转全景 (含销售商占比)")
fig_s = go.Figure(go.Sankey(
    node = dict(
        pad = 20, thickness = 25, line = dict(color = "#ffffff", width = 2),
        label = [
            "个人回收 (55%)", "退货机 (15%)", "大宗商业回收 (30%)", 
            "Brightstar评估", "顺丰逆向物流", "富士康/和硕整备", 
            "官网直营 (15%)", "京东自营 (45%)", "爱回收渠道 (20%)", "B2B集采 (20%)"
        ],
        color = ["#87adab", "#d6a0a0", "#e9c46a", "#a8dadc", "#82a1b1", "#b5c7d3", "#457b9d", "#f4a261", "#fbc02d", "#e76f51"]
    ),
    link = dict(
        source = [0, 1, 2, 3, 4, 5, 5, 5, 5], 
        target = [3, 3, 3, 4, 5, 6, 7, 8, 9],
        value = [55, 15, 30, 100, 100, 15, 45, 20, 20],
        color = "rgba(189, 195, 199, 0.4)"
    )
))
fig_s.update_layout(font_size=12, font_color="#34495e")
st.plotly_chart(fig_s, use_container_width=True)

st.write("**业务总结：** 中国区 iPhone 资源机约 **65% (45%+20%)** 的份额由 **京东自营** 和 **爱回收** 承载。")
