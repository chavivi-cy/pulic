import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 页面配置
st.set_page_config(page_title="苹果再制造业务深度决策系统", layout="wide")

# 视觉基准声明
st.title("🍏 苹果产品再制造 (Remanufacturing) 业务调研系统")
st.info("📊 **业务基准：** 以 iPhone 15 Pro (128G) 2025年初定价为核心模型")

# 侧边栏：交互参数
st.sidebar.header("⚙️ 模拟参数配置")
retail_p = st.sidebar.slider("零售均价 (CNY)", 4000, 9500, 6199)
buyback_r = st.sidebar.slider("回收成本占比 (%)", 50, 85, 65)
refurb_c = st.sidebar.slider("整备成本 (CNY)", 300, 1500, 750)
log_w = st.sidebar.number_input("物流及质保金 (CNY)", value=480)

# 财务计算
buyback_v = retail_p * (buyback_r / 100)
total_c = buyback_v + refurb_c + log_w
profit = retail_p - total_c
margin = (profit / retail_p) * 100

# 核心指标
c1, c2, c3, c4 = st.columns(4)
c1.metric("预测利润", f"¥{profit:,.0f}", f"{margin:.1f}% 毛利")
c2.metric("回收成本", f"¥{buyback_v:,.0f}", f"{buyback_r}%")
c3.metric("市场溢价", "22%", "对比第三方")
c4.metric("拦截率", "99.9%", "数字化壁垒")

st.markdown("---")

# --- 8大课题交互面板：独立视觉呈现 ---
st.header("🔍 行业专题调研：8大核心课题")
qs = [
    "Q1: 商业模型解析", "Q2: 核心商业目标", "Q3: 关键成功因素(KSF)", 
    "Q4: 业务流程与分级", "Q5: 中国区出货渠道", "Q6: 目标用户画像", 
    "Q7: 跨品牌对标分析", "Q8: 为什么不碰纯二手"
]
sel_q = st.selectbox("请点选课题查看对应的可视化深度分析：", qs)

if sel_q == qs[0]:
    st.write("### Q1: 商业模型 - 价值链瀑布分析")
    fig = go.Figure(go.Waterfall(
        x = ["零售价", "回收成本", "整备物料", "逆向物流", "净利润"],
        y = [retail_p, -buyback_v, -refurb_c, -log_w, 0],
        measure = ["relative", "relative", "relative", "relative", "total"],
        decreasing = {"marker":{"color":"#EF553B"}},
        increasing = {"marker":{"color":"#228B22"}},
        totals = {"marker":{"color":"#1f77b4"}}
    ))
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[1]:
    st.write("### Q2: 商业目标 - 存量与拉新构成")
    fig = px.pie(names=["首次入坑(新客)", "生态升级(老客)"], values=[35, 65], hole=0.4, color_discrete_sequence=['#228B22', '#AB63FA'])
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[2]:
    st.write("### Q3: 关键成功因素 - 技术确权壁垒")
    fig = px.bar(x=["官方翻新", "三方精品", "拼装机"], y=[100, 75, 30], labels={'x':'类别', 'y':'功能完备度 (%)'}, color_discrete_sequence=['#228B22'])
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[3]:
    st.write("### Q4: 业务流程 - 质量分级漏斗")
    fig = go.Figure(go.Funnel(y=["回收总量", "通过ATE初检", "原厂翻修后", "官方合格品"], x=[100, 85, 80, 78], marker={"color": "#228B22"}))
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[4]:
    st.write("### Q5: 出货渠道 - 中国区份额分布")
    fig = px.bar(x=["京东自营", "爱回收/线下", "B2B集采", "官网"], y=[45, 20, 20, 15], labels={'x':'渠道', 'y':'占比 (%)'}, color_discrete_sequence=['#FFA07A'])
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[5]:
    st.write("### Q6: 用户画像 - 多维度属性雷达图")
    fig = px.line_polar(r=[90, 85, 95, 60], theta=["品牌忠诚", "价格敏感", "质量焦虑", "环保意识"], line_close=True)
    fig.update_traces(fill='toself', fillcolor='rgba(34, 139, 34, 0.3)', line_color='#228B22')
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[6]:
    st.write("### Q7: 残值曲线对标 - 苹果的高残值护城河")
    m = [1, 6, 12, 18, 24, 30, 36]
    df = pd.DataFrame({
        "月份": m*4,
        "保持率": [95,85,71,65,58,52,45, 92,80,65,50,42,35,28, 88,75,55,45,38,30,22, 80,55,40,28,18,10,5],
        "品牌": ["Apple"]*7 + ["Huawei"]*7 + ["Samsung"]*7 + ["其他安卓"]*7
    })
    fig = px.line(df, x="月份", y="保持率", color="品牌", markers=True, color_discrete_map={"Apple":"#228B22","Huawei":"#FF8C00","Samsung":"#4169E1","其他安卓":"#B22222"})
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[7]:
    st.write("### Q8: 业务红线 - 为什么不碰纯二手风险分析")
    fig = px.bar(y=["隐私风险", "品牌稀释", "售后纠纷"], x=[95, 80, 85], orientation='h', color_discrete_sequence=['#EF553B'])
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- 严谨版彩色流转路径 (Sankey) ---
st.header("🌐 中国区逆向流转全景 (数据闭环版)")
fig_s = go.Figure(go.Sankey(
    node = dict(
        pad = 15, thickness = 20, line = dict(color = "black", width = 0.5),
        label = ["个人回收源 (55%)", "14天退货 (15%)", "商业/以旧换新 (30%)", "评估(Brightstar)", "顺丰/逆向物流", "富士康/整备", "官网直营", "京东/爱回收分销", "B2B集采"],
        color = ["#228B22", "#FF8C00", "#FFD700", "#4169E1", "#808080", "#AB63FA", "#00D1B2", "#FFA07A", "#FF4500"]
    ),
    link = dict(
        source = [0, 1, 2, 3, 4, 5, 5, 5], 
        target = [3, 3, 3, 4, 5, 6, 7, 8],
        value = [55, 15, 30, 100, 100, 15, 65, 20]
    )
))
st.plotly_chart(fig_s, use_container_width=True)
st.write("**严谨性标注：** 货源由个人(55%)、退换货(15%)及大宗商业渠道(30%)共同构成，确保 100% 数据闭环。")
