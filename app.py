import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 页面基础配置
st.set_page_config(page_title="苹果再制造业务深度决策系统", layout="wide")

# CSS 视觉增强：解决看板文字可见性与手机端适配
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    /* 顶部看板指标：文字设为白色 */
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.8rem !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 1.1rem !important; }
    .stMetric { background-color: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }
    h1, h2, h3 { color: #f8fafc; font-family: "Hiragino Sans GB", sans-serif; }
    .stInfo { background-color: #1e293b; border: none; color: #cbd5e1; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部声明 ---
st.title("🕊️ 苹果产品再制造业务调研系统")
st.info("📊 **业务基准：** 以 iPhone 15 Pro 为财务模型。iPhone 官翻机在华主攻授权分销，Mac/iPad 涵盖直营路径。")

# --- 侧边栏 ---
st.sidebar.header("🍃 决策因子")
base_vol_k = st.sidebar.slider("月流转规模 (k - 千台)", 1, 1000, 500)
base_vol = base_vol_k * 1000
retail_p = st.sidebar.slider("零售价 (CNY)", 4000, 9500, 6199)
buyback_r = st.sidebar.slider("回收成本占比 (%)", 50, 85, 65)
refurb_c = st.sidebar.slider("整备成本 (CNY)", 300, 1500, 750)

# 核心损益计算
buyback_v = retail_p * (buyback_r / 100)
profit = retail_p - (buyback_v + refurb_c + 480) 
margin = (profit / retail_p) * 100

# --- 指标看板 (白色文字) ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("预测单机利润", f"¥{profit:,.0f}", f"{margin:.1f}% 毛利")
with c2: st.metric("回收对价锚点", f"¥{buyback_v:,.0f}", f"{buyback_r}% 占比")
with c3: st.metric("溢价优势", "22%", "对比第三方二手")
with c4: st.metric("零件配对率", "99.9%", "数字化壁垒")

st.markdown("---")

# --- 8大课题交互区 (独立可视化) ---
st.header("🌿 行业专题调研：交互可视化中心")
qs = ["Q1: 商业模型解析", "Q2: 核心商业目标", "Q3: 关键成功因素(KSF)", 
      "Q4: 业务流程与损耗", "Q5: 出货渠道分布", "Q6: 目标用户画像", 
      "Q7: 跨品牌残值对标", "Q8: 业务风险红线矩阵"]
sel_q = st.selectbox("请点选课题查看对应的交互图表：", qs)

JP_COLORS = ['#87adab', '#d6a0a0', '#e9c46a', '#a8dadc', '#82a1b1']

if sel_q == qs[0]:
    st.write("### Q1: 商业模型 - 筑屋式价值堆叠")
    fig = go.Figure([
        go.Bar(name='回收成本', x=['P&L'], y=[buyback_v], marker_color=JP_COLORS[0]),
        go.Bar(name='整备增值', x=['P&L'], y=[refurb_c+480], base=buyback_v, marker_color=JP_COLORS[1]),
        go.Bar(name='净利润', x=['P&L'], y=[profit], base=buyback_v+refurb_c+480, marker_color=JP_COLORS[2])
    ])
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[2]:
    st.write("### Q3: KSF - 技术确权维度图")
    df3 = pd.DataFrame(dict(r=[98, 95, 99, 88, 92], theta=['部件配对','SN溯源','激活校验','ATE测试','定价权']))
    fig = px.line_polar(df3, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself', fillcolor='rgba(135, 173, 171, 0.4)', line_color=JP_COLORS[0])
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[3]:
    st.write(f"### Q4: 损耗过滤 - 基于 {base_vol_k}k 台规模")
    fig = go.Figure(go.Funnel(
        y=["回收总量 (100%)", "通过初检 (85%)", "原厂重整 (80%)", "合格成品 (78%)"], 
        x=[base_vol, base_vol*0.85, base_vol*0.80, base_vol*0.78], 
        marker={"color": JP_COLORS}, textinfo="value+percent initial"
    ))
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[4]:
    st.write("### Q5: 渠道份额分布")
    df5 = pd.DataFrame({
        "渠道": ["京东自营", "爱回收", "官网(iPad/Mac)", "转转及其他", "B2B集采"],
        "占比": [45, 20, 15, 10, 10], "父级": ["所有渠道"] * 5
    })
    fig = px.treemap(df5, path=["父级", "渠道"], values='占比', color='占比', color_continuous_scale='Tealgrn')
    fig.update_traces(textinfo="label+value+percent parent")
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[5]:
    st.write("### Q6: 目标用户画像分析")
    df6 = pd.DataFrame({
        "画像受众": ["精致白领 (35%)", "数码极客 (25%)", "在校学生 (25%)", "小镇青年 (15%)"],
        "占比": [35, 25, 25, 15]
    })
    fig = px.bar(df6, x="占比", y="画像受众", orientation='h', color="占比", color_continuous_scale='Burg', text="占比")
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[6]:
    st.write("### Q7: 品牌残值衰减对标")
    m = [1, 6, 12, 18, 24, 30, 36]
    df7 = pd.DataFrame({"月":m*4,"RV":[95,85,71,65,58,52,45, 92,80,65,50,42,35,28, 88,75,55,45,38,30,22, 80,55,40,28,18,10,5],"B":["Apple"]*7+["Huawei"]*7+["Samsung"]*7+["安卓平均"]*7})
    fig = px.line(df7, x="月", y="RV", color="B", markers=True, color_discrete_map={"Apple":"#27ae60","Huawei":"#e67e22","Samsung":"#3498db","安卓平均":"#e74c3c"})
    st.plotly_chart(fig, use_container_width=True)

elif sel_q == qs[7]:
    st.write("### Q8: 业务风险红线矩阵")
    fig = px.scatter(x=[90, 85, 75], y=[95, 80, 70], text=["隐私安全","品牌溢价","售后纠纷"], 
                     size=[40, 25, 30], color_discrete_sequence=[JP_COLORS[2]],
                     labels={'x':'X：风险发生概率', 'y':'Y：负面冲击程度'})
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("### Q2: 商业目标 - 拉新与留存")
    df2 = pd.DataFrame({"A":["拉新","拉新","留存","留存"],"B":["新入iOS","安卓切换","旧机换新","服务增购"],"V":[20,15,45,20]})
    fig = px.sunburst(df2, path=['A','B'], values='V', color_discrete_sequence=[JP_COLORS[0], JP_COLORS[3]])
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- 模块三：流转全景 (核心修复版) ---
st.header("🌐 中国区逆向流转全景")

# 定义节点标签、颜色
labels = ["个人回收源 (65%)", "14天退货机 (20%)", "商业渠道回收 (15%)", "价值评估", "逆向物流", "检测整备工厂", "京东自营 (45%)", "爱回收渠道 (20%)", "官网直营 (15%)", "转转及其他 (10%)", "B2B集采 (10%)"]
colors = [JP_COLORS[0], JP_COLORS[1], JP_COLORS[2], JP_COLORS[3], JP_COLORS[4], "#64748b", "#f4a261", "#fbc02d", "#457b9d", "#ffcc80", "#e76f51"]

# 确保索引正确映射：
# 0:个人, 1:退货, 2:商业 -> 3:评估 -> 4:物流 -> 5:整备 -> 6:京东, 7:爱回收, 8:官网, 9:转转, 10:B2B
fig_sankey = go.Figure(go.Sankey(
    node = dict(
        pad = 40, thickness = 25, line = dict(color = "#ffffff", width = 1),
        label = labels,
        color = colors,
        font = dict(color="black", size=12)
    ),
    link = dict(
        source =
