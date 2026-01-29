import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 页面基础配置
st.set_page_config(page_title="苹果再制造业务决策系统", layout="wide")

# CSS 增强：提升文字对比度
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; border-radius: 12px; padding: 20px; border: 1px solid #d1d9e0; }
    .stMetric [data-testid="stMetricValue"] { color: #1e293b !important; }
    h1, h2, h3 { color: #f8fafc; font-family: "Hiragino Sans GB", sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部声明 ---
st.title("🕊️ 苹果产品再制造 (Remanufacturing) 业务调研系统")
st.info("📊 **业务基准：** 以 iPhone 15 Pro (128G) 为模型，覆盖全品类。中国区 iPhone 官翻主攻授权渠道。")

# --- 侧边栏交互 ---
st.sidebar.header("🍃 决策因子")
base_vol_k = st.sidebar.slider("回收基准规模 (k - 千台)", 1, 1000, 500)
base_vol = base_vol_k * 1000
retail_p = st.sidebar.slider("零售价 (CNY)", 4000, 9500, 6199)
buyback_r = st.sidebar.slider("回收成本占比 (%)", 50, 85, 65)
refurb_c = st.sidebar.slider("整备成本 (CNY)", 300, 1500, 750)
log_w = st.sidebar.number_input("质保及准备金 (CNY)", value=480)

# 计算逻辑
buyback_v = retail_p * (buyback_r / 100)
profit = retail_p - (buyback_v + refurb_c + log_w)
margin = (profit / retail_p) * 100

# --- 指标看板 ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("预测利润", f"¥{profit:,.0f}", f"{margin:.1f}% 毛利")
with c2: st.metric("回收成本", f"¥{buyback_v:,.0f}", f"{buyback_r}%")
with c3: st.metric("溢价优势", "22%", "对比第三方")
with c4: st.metric("技术拦截率", "99.9%", "零件配对壁垒")

st.markdown("---")

# --- 8大课题交互区 ---
st.header("🌿 行业专题调研：交互视觉中心")
qs = ["Q1: 商业模型解析", "Q2: 核心商业目标分析", "Q3: 关键成功因素(KSF)", 
      "Q4: 业务流程与质量损耗", "Q5: 中国区出货渠道份额", "Q6: 目标用户画像分析", 
      "Q7: 跨品牌残值衰减对标", "Q8: 业务红线风险矩阵"]
sel_q = st.selectbox("请点选调研课题：", qs)

JP_COLORS = ['#87adab', '#d6a0a0', '#e9c46a', '#a8dadc', '#82a1b1']

if sel_q == qs[0]:
    st.write("### Q1: 商业模型 - 筑屋式利润堆叠")
    fig = go.Figure([
        go.Bar(name='回收对价', x=['构成'], y=[buyback_v], marker_color=JP_COLORS[0]),
        go.Bar(name='整备物流', x=['构成'], y=[refurb_c+log_w], base=buyback_v, marker_color=JP_COLORS[1]),
        go.Bar(name='单机利润', x=['构成'], y=[profit], base=buyback_v+refurb_c+log_w, marker_color=JP_COLORS[2])
    ])
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[2]:
    st.write("### Q3: 关键成功因素 - 技术确权维度")
    df_q3 = pd.DataFrame(dict(r=[98, 95, 99, 88, 92], theta=['部件配对','SN溯源','激活校验','ATE测试','定价权']))
    fig = px.line_polar(df_q3, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself', fillcolor='rgba(135, 173, 171, 0.4)', line_color=JP_COLORS[0])
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[3]:
    st.write(f"### Q4: 流程损耗 - 基于 {base_vol_k}k 台规模 (含占比)")
    fig = go.Figure(go.Funnel(
        y=["回收总量", "通过初检", "原厂翻修", "合格成品"], 
        x=[base_vol, base_vol*0.85, base_vol*0.80, base_vol*0.78], 
        marker={"color": JP_COLORS},
        textinfo="value+percent initial"
    ))
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[5]:
    st.write("### Q6: 目标用户画像多维分析")
    fig = px.bar(x=[92, 88, 95, 65], y=["品牌执念","价格敏感","质量可靠","ESG认同"], orientation='h', color_discrete_sequence=[JP_COLORS[1]])
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[6]:
    st.write("### Q7: 1-36个月品牌残值对标")
    m = [1, 6, 12, 18, 24, 30, 36]
    df_q7 = pd.DataFrame({"月":m*4,"RV":[95,85,71,65,58,52,45, 92,80,65,50,42,35,28, 88,75,55,45,38,30,22, 80,55,40,28,18,10,5],"B":["Apple"]*7+["Huawei"]*7+["Samsung"]*7+["安卓平均"]*7})
    fig = px.line(df_q7, x="月", y="RV", color="B", markers=True, color_discrete_map={"Apple":"#27ae60","Huawei":"#e67e22","Samsung":"#3498db","安卓平均":"#e74c3c"})
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[7]:
    st.write("### Q8: 业务红线风险矩阵")
    fig = px.scatter(x=[90, 85, 75], y=[95, 80, 70], text=["隐私安全","品牌溢价","售后纠纷"], size=[40, 25, 30], color_discrete_sequence=[JP_COLORS[2]])
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write(f"### {sel_q}")
    st.info("数据分析已集成至下方流转全景中。")

st.markdown("---")

# --- 流转全景 ---
st.header("🌐 中国区逆向流转全景 (标注经销商占比)")
fig_s = go.Figure(go.Sankey(
    node = dict(pad=40, thickness=25, label=[
        "回收源 (70%)", "退货机 (30%)", "价值评估", "逆向物流", "工厂整备", 
        "官网直营 (15%)", "京东自营 (45%)", "爱回收渠道 (20%)", "转转及其他 (20%)"
    ], color=[JP_COLORS[0], JP_COLORS[1], JP_COLORS[2], JP_COLORS[3], JP_COLORS[4], "#457b9d", "#f4a261", "#fbc02d", "#ffcc80"]),
    link = dict(source=[0, 1, 2, 3, 4, 4, 4, 4], target=[2, 2, 3, 4, 5, 6, 7, 8], value=[70, 30, 100, 100, 15, 45, 20, 20], color="rgba(200, 200, 200, 0.3)")
))
st.plotly_chart(fig_s, use_container_width=True)
