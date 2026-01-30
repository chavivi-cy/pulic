import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 页面基础配置
st.set_page_config(page_title="苹果再制造业务深度决策系统", layout="wide")

# CSS 视觉增强
st.markdown("""
    <style>
    /* 1. 全局背景：深色调 */
    .main { background-color: #0e1117; }

    /* 2. 指标卡片：深蓝背景与边框 */
    .stMetric { 
        background-color: #1e293b; 
        border-radius: 12px; 
        padding: 20px; 
        border: 1px solid #334155; 
    }

    /* 3. 指标数值：强制纯白，字号加大 */
    [data-testid="stMetricValue"] { 
        color: #ffffff !important; 
        font-size: 1.8rem !important; 
    }

    /* 4. 指标标签（标题）：强制纯白，确保手机端清晰 */
    [data-testid="stMetricLabel"] { 
        color: #ffffff !important; 
        font-size: 1.1rem !important; 
    }

    /* 5. 标题字体：雅致日系感 */
    h1, h2, h3 { 
        color: #f8fafc; 
        font-family: "Hiragino Sans GB", "Microsoft YaHei", sans-serif; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部声明 ---
st.title("🕊️ 苹果产品再制造业务调研系统")
st.info("📊 **业务说明：** 以 iPhone 15 Pro 为财务基准（2025-Q1）。iPhone 官翻机在华主攻授权分销，Mac/iPad 涵盖直营路径。")

# --- 侧边栏 ---
st.sidebar.header("🍃 决策因子")
base_vol_k = st.sidebar.slider("月流转规模 (k - 千台)", 1, 1000, 500)
base_vol = base_vol_k * 1000
retail_p = st.sidebar.slider("零售价 (CNY)", 4000, 9500, 6199)
buyback_r = st.sidebar.slider("回收成本占比 (%)", 50, 85, 65)
refurb_c = st.sidebar.slider("整备成本 (CNY)", 300, 1500, 750)

# 核心损益计算
buyback_v = retail_p * (buyback_r / 100)
profit = retail_p - (buyback_v + refurb_c + 480) # 480 为固定物流质保成本
margin = (profit / retail_p) * 100

# --- 指标看板 ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("预测单机利润", f"¥{profit:,.0f}", f"{margin:.1f}% 毛利")
with c2: st.metric("回收对价锚点", f"¥{buyback_v:,.0f}", f"{buyback_r}% 占比")
with c3: st.metric("溢价优势", "22%", "对比第三方二手")
with c4: st.metric("零件配对率", "99.9%", "数字化壁垒")

st.markdown("---")

# --- 8大课题交互区 (全独立可视化) ---
st.header("🌿 行业专题调研：交互可视化中心")
qs = ["Q1: 商业模型解析", "Q2: 核心商业目标", "Q3: 关键成功因素(KSF)", 
      "Q4: 业务流程与损耗", "Q5: 出货渠道分布", "Q6: 目标用户画像", 
      "Q7: 跨品牌残值对标", "Q8: 业务风险红线矩阵"]
sel_q = st.selectbox("请点选课题查看对应的交互图表：", qs)

JP_COLORS = ['#87adab', '#d6a0a0', '#e9c46a', '#a8dadc', '#82a1b1']

if sel_q == qs[0]:
    st.write("### Q1: 商业模型 - 价值堆叠筑屋图")
    fig1 = go.Figure([
        go.Bar(name='回收成本', x=['P&L'], y=[buyback_v], marker_color=JP_COLORS[0]),
        go.Bar(name='整备增值', x=['P&L'], y=[refurb_c+480], base=buyback_v, marker_color=JP_COLORS[1]),
        go.Bar(name='净利润', x=['P&L'], y=[profit], base=buyback_v+refurb_c+480, marker_color=JP_COLORS[2])
    ])
    st.plotly_chart(fig1, use_container_width=True)

elif sel_q == qs[1]:
    st.write("### Q2: 商业目标 - 存量留存与新客拉新")
    df2 = pd.DataFrame({"A":["拉新","拉新","留存","留存"],"B":["新入iOS","安卓切换","旧机换新","服务增购"],"V":[20,15,45,20]})
    fig2 = px.sunburst(df2, path=['A','B'], values='V', color_discrete_sequence=[JP_COLORS[0], JP_COLORS[3]])
    st.plotly_chart(fig2, use_container_width=True)

elif sel_q == qs[2]:
    st.write("### Q3: KSF - 技术确权维度图")
    df3 = pd.DataFrame(dict(r=[98, 95, 99, 88, 92], theta=['部件配对','SN溯源','激活校验','ATE测试','定价权']))
    fig3 = px.line_polar(df3, r='r', theta='theta', line_close=True)
    fig3.update_traces(fill='toself', fillcolor='rgba(135, 173, 171, 0.4)', line_color=JP_COLORS[0])
    st.plotly_chart(fig3, use_container_width=True)

elif sel_q == qs[3]:
    st.write(f"### Q4: 损耗过滤 - 基于 {base_vol_k}k 台基数的损耗分析 (含占比)")
    fig4 = go.Figure(go.Funnel(
        y=["回收总量 (100%)", "通过初检 (85%)", "原厂重整 (80%)", "合格成品 (78%)"], 
        x=[base_vol, base_vol*0.85, base_vol*0.80, base_vol*0.78], 
        marker={"color": JP_COLORS}, textinfo="value+percent initial"
    ))
    st.plotly_chart(fig4, use_container_width=True)

elif sel_q == qs[4]:
    st.write("### Q5: 渠道份额详细分布 (含具体占比)")
    df5 = pd.DataFrame({
        "渠道": ["京东自营", "爱回收", "官网(iPad/Mac)", "转转及其他", "B2B集采"],
        "占比": [45, 20, 15, 10, 10],
        "父级": ["所有渠道"] * 5
    })
    fig5 = px.treemap(df5, path=["父级", "渠道"], values='占比', 
                     color='占比', color_continuous_scale='Tealgrn')
    fig5.update_traces(textinfo="label+value+percent parent")
    st.plotly_chart(fig5, use_container_width=True)

elif sel_q == qs[5]:
    st.write("### Q6: 目标用户画像分析 (受众分类与占比)")
    df6 = pd.DataFrame({
        "画像受众": ["精致白领 (性价比升级)", "数码极客 (官方拆解件)", "在校学生 (官翻入门)", "小镇青年 (大屏刚需)"],
        "人群占比 (%)": [35, 25, 25, 15],
        "核心诉求权重": [92, 95, 88, 80]
    })
    fig6 = px.bar(df6, x="人群占比 (%)", y="画像受众", orientation='h', 
                 color="人群占比 (%)", color_continuous_scale='Burg', text="人群占比 (%)")
    fig6.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig6, use_container_width=True)

elif sel_q == qs[6]:
    st.write("### Q7: 品牌残值衰减对标 (1-36个月)")
    m = [1, 6, 12, 18, 24, 30, 36]
    df7 = pd.DataFrame({"月":m*4,"RV":[95,85,71,65,58,52,45, 92,80,65,50,42,35,28, 88,75,55,45,38,30,22, 80,55,40,28,18,10,5],"B":["Apple"]*7+["Huawei"]*7+["Samsung"]*7+["安卓平均"]*7})
    fig7 = px.line(df7, x="月", y="RV", color="B", markers=True, color_discrete_map={"Apple":"#27ae60","Huawei":"#e67e22","Samsung":"#3498db","安卓平均":"#e74c3c"})
    st.plotly_chart(fig7, use_container_width=True)

elif sel_q == qs[7]:
    st.write("### Q8: 业务风险红线矩阵")
    fig8 = px.scatter(x=[90, 85, 75], y=[95, 80, 70], text=["隐私安全","品牌溢价","售后纠纷"], 
                     size=[40, 25, 30], color_discrete_sequence=[JP_COLORS[2]],
                     labels={'x':'X：风险发生概率', 'y':'Y：负面冲击程度'})
    st.plotly_chart(fig8, use_container_width=True)

else:
    st.info("请选择上方课题进行数据分析")

st.markdown("---")

import plotly.graph_objects as go
import streamlit as st

st.header("🌐 中国区逆向流转全景")

# 确保颜色列表长度对应（防止因缺少变量报错，这里我先用Hex颜色代替，你确认没问题后可换回JP_COLORS）
colors_list = [
    "#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51", # 对应原来的 JP_COLORS
    "#f4a261", "#fbc02d", "#457b9d", "#ffcc80", "#e76f51", "#8d99ae"
]

fig_s = go.Figure(go.Sankey(
    node = dict(
        pad = 45, 
        thickness = 25, 
        label = [
            "个人回收源 (65%)", "14天退货机 (20%)", "商业渠道回收 (15%)", 
            "价值评估", "逆向物流", "检测整备工厂", 
            "京东自营 (45%)", "爱回收渠道 (20%)", "官网直营 (15%)", "转转及其他 (10%)", "B2B集采 (10%)"
        ], 
        # 这里的颜色列表长度最好和 label 数量一致 (11个)
        color = colors_list,
        
        # --- 核心修改：字体变成黑色 ---
        font = dict(
            color = "black",
            size = 12
        )
        # ---------------------------
    ),
    link = dict(
        source = [0, 1, 2, 3, 4, 5, 5, 5, 5, 5], 
        target = [3, 3, 3, 4, 5, 6, 7, 8, 9, 10], 
        value  = [65, 20, 15, 100, 100, 45, 20, 15, 10, 10], 
        color  = "rgba(200, 200, 200, 0.4)"
    )
))

st.plotly_chart(fig_s, use_container_width=True)
