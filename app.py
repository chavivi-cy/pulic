import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# 页面基础配置
st.set_page_config(page_title="苹果逆向供应链决策分析系统", layout="wide")

# 1. 顶部指标栏：实时决策看板
st.title("📱 苹果产品再制造 (Remanufacturing) 业务决策分析系统")
st.caption("版本：2026.1 | 核心逻辑：基于中国区逆向供应链财务模型")

# 侧边栏：核心决策因子
st.sidebar.header("⚙️ 决策因子配置")
retail_price = st.sidebar.slider("零售价区间 (CNY)", 4000, 9500, 6199)
buyback_rate = st.sidebar.slider("回收成本占比 (%)", 50, 85, 65)
refurb_cost = st.sidebar.slider("整备及备件成本 (CNY)", 300, 1500, 750)
logistics_warranty = st.sidebar.number_input("逆向物流及质保准备 (CNY)", value=480)

# 财务计算逻辑
buyback_val = retail_price * (buyback_rate / 100)
total_cost = buyback_val + refurb_cost + logistics_warranty
net_profit = retail_price - total_cost
margin_pct = (net_profit / retail_price) * 100

# 动态预警颜色
status_color = "normal" if margin_pct > 10 else "inverse"

c1, c2, c3, c4 = st.columns(4)
c1.metric("单机净利润", f"¥{net_profit:,.0f}", f"{margin_pct:.1f}% 毛利率", delta_color=status_color)
c2.metric("盈亏平衡线 (BEP)", f"¥{retail_price - refurb_cost - logistics_warranty:,.0f}", "最高回收出价")
c3.metric("市场流转溢价", "22%", "对比第三方二手")
c4.metric("零件配对校验率", "99.9%", "技术壁垒指标")

st.markdown("---")

# 2. 深度分析板块
t1, t2, t3 = st.tabs(["📊 损益结构分析", "📈 跨品牌残值对比", "🌐 渠道流转与用户画像"])

with t1:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("单机损益 (P&L) 瀑布流")
        fig_waterfall = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["relative", "relative", "relative", "relative", "total"],
            x = ["零售单价", "回收成本", "整备物料", "逆向质保", "净收益"],
            y = [retail_price, -buyback_val, -refurb_cost, -logistics_warranty, 0],
            text = [f"+{retail_price}", f"-{buyback_val:.0f}", f"-{refurb_cost}", f"-{logistics_warranty}", f"={net_profit:.0f}"],
            decreasing = {"marker":{"color":"#EF553B"}},
            increasing = {"marker":{"color":"#00CC96"}},
            totals = {"marker":{"color":"#1f77b4"}}
        ))
        st.plotly_chart(fig_waterfall, use_container_width=True)
    
    with col_b:
        st.subheader("回收敏感度分析表")
        # 自动生成不同回收率下的利润对照表
        rates = [55, 60, 65, 70, 75]
        sensitivity_data = {
            "回收占比": [f"{r}%" for r in rates],
            "单机利润": [f"¥{retail_price*(1-r/100)-refurb_cost-logistics_warranty:,.0f}" for r in rates]
        }
        st.table(pd.DataFrame(sensitivity_data))
        st.caption("提示：当回收成本超过 72% 时，业务进入低毛利陷阱。")

with t2:
    st.subheader("1-36个月残值保持率 (Residual Value) 趋势对比")
    months = [1, 6, 12, 18, 24, 30, 36]
    df_rv = pd.DataFrame({
        "月份": months * 3,
        "保持率 (%)": [95, 85, 71, 65, 58, 52, 45,  # Apple
                    92, 80, 65, 50, 42, 35, 28,  # Huawei
                    85, 60, 42, 30, 20, 12, 8],   # Android Avg
        "品牌": ["Apple (iPhone)"]*7 + ["Huawei (CPO)"]*7 + ["安卓主流旗舰"]*7
    })
    fig_rv = px.line(df_rv, x="月份", y="保持率 (%)", color="品牌", markers=True, 
                     color_discrete_map={"Apple (iPhone)": "#000000", "Huawei (CPO)": "#FF0000", "安卓主流旗舰": "#636EFA"})
    st.plotly_chart(fig_rv, use_container_width=True)
    st.info("💡 结论：iPhone 高残值特性是再制造业务 P&L 能够闭环的底层驱动力。")

with t3:
    col_c, col_d = st.columns(2)
    with col_c:
        st.subheader("中国区逆向流转路径 (Sankey)")
        fig_sankey = go.Figure(go.Sankey(
            node = dict(pad = 15, thickness = 20, label = ["回收源", "检测整备", "官网(Mac/iPad)", "分销(iPhone)", "B2B集采"], color = "royalblue"),
            link = dict(source = [0, 0, 1, 1, 1], target = [1, 1, 2, 3, 4], value = [60, 40, 15, 65, 20])))
        st.plotly_chart(fig_sankey, use_container_width=True)
    with col_d:
        st.subheader("细分用户画像")
        fig_pie = px.pie(names=["实用主义白领", "教育/学生", "B2B测试/租赁", "数码极客"], values=[45, 25, 20, 10], hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

# 3. 底部专家结论
st.markdown("---")
st.subheader("📌 核心业务策略结论")
st.success("""
1. **技术确权**：部件配对 (Parts Pairing) 已成为行业最高技术壁垒。
2. **渠道平衡**：iPhone 资源机模式有效规避了官网直接销售的售后冗余成本。
3. **利润引擎**：再制造业务的单机 GP 贡献远超新机，是存量市场的重要利润支撑。
""")