import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 设置页面配置
st.set_page_config(
    page_title="文瑞锋的电商销售分析项目",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .chart-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_sales_data.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    # 添加月份和年份列用于分析
    df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
    df['Year'] = df['Order Date'].dt.year
    return df

try:
    df = load_data()

    # --- 侧边栏设计 ---
    st.sidebar.title("🛠️ 数据筛选中心")
    st.sidebar.info("请选择筛选条件，系统将实时更新图表")

    # 日期范围选择
    min_date = df['Order Date'].min().to_pydatetime()
    max_date = df['Order Date'].max().to_pydatetime()
    
    st.sidebar.subheader("📅 时间跨度")
    col_start, col_end = st.sidebar.columns(2)
    with col_start:
        start_date = st.date_input(
            "开始日期",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )
    with col_end:
        end_date = st.date_input(
            "结束日期",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

    # 联动过滤器
    st.sidebar.subheader("🔍 分类筛选")
    all_categories = sorted(df['Category'].unique())
    selected_categories = st.sidebar.multiselect(
        "选择商品类别",
        options=all_categories,
        default=all_categories
    )

    all_regions = sorted(df['Region'].unique())
    selected_regions = st.sidebar.multiselect(
        "选择业务地区",
        options=all_regions,
        default=all_regions
    )

    # 数据筛选逻辑
    if start_date > end_date:
        st.sidebar.error("⚠️ 开始日期不能晚于结束日期")
        filtered_df = df.iloc[0:0] # 返回空数据
    else:
        mask = (
            (df['Order Date'].dt.date >= start_date) & 
            (df['Order Date'].dt.date <= end_date) &
            (df['Category'].isin(selected_categories)) &
            (df['Region'].isin(selected_regions))
        )
        filtered_df = df.loc[mask]

    # --- 主界面设计 ---
    st.title(" 电商销售分析 Dashboard")
    
    # KPI 核心指标 (带环比/对比概念，这里模拟一个对比值)
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_quantity = filtered_df['Quantity'].sum()
    avg_order_value = total_sales / len(filtered_df) if len(filtered_df) > 0 else 0
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    with col1:
        st.metric("总销售额", f"${total_sales:,.0f}", delta=f"{(total_sales/1000000):.1f}M")
    with col2:
        st.metric("核心净利润", f"${total_profit:,.0f}", delta=f"{profit_margin:.1f}% 利润率")
    with col3:
        st.metric("累计订单量", f"{len(filtered_df):,}", delta=f"{total_quantity:,} 件商品")
    with col4:
        st.metric("客单价 (AOV)", f"${avg_order_value:,.2f}")

    st.markdown("---")

    # --- 核心图表区 ---
    tabs = st.tabs(["📈 销售趋势", "🌍 区域与分类", "📦 产品洞察", "📊 数据透视"])

    with tabs[0]:
        st.subheader("时间序列深度分析")
        freq = st.selectbox("统计频率", ["日", "周", "月"], index=2)
        
        freq_map = {"日": "D", "周": "W", "月": "ME"}
        ts_data = filtered_df.set_index('Order Date').resample(freq_map[freq])['Sales'].sum().reset_index()
        
        fig_ts = px.area(ts_data, x='Order Date', y='Sales', 
                         title=f'{freq}度销售趋势',
                         template="plotly_white",
                         color_discrete_sequence=['#00CC96'])
        fig_ts.update_layout(hovermode="x unified")
        st.plotly_chart(fig_ts, use_container_width=True)

    with tabs[1]:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("各地区盈利能力")
            region_perf = filtered_df.groupby('Region').agg({
                'Sales': 'sum',
                'Profit': 'sum'
            }).reset_index()
            fig_region = px.bar(region_perf, x='Region', y='Sales', color='Profit',
                               title='地区销售与利润热力图',
                               color_continuous_scale='RdYlGn')
            st.plotly_chart(fig_region, use_container_width=True)
        
        with c2:
            st.subheader("分类构成")
            cat_perf = filtered_df.groupby('Category')['Sales'].sum().reset_index()
            fig_pie = px.sunburst(filtered_df, path=['Category', 'Product Name'], values='Sales',
                                 title='类别-产品层级销售分布')
            st.plotly_chart(fig_pie, use_container_width=True)

    with tabs[2]:
        st.subheader("Top 10 核心产品表现")
        top_n = st.slider("展示产品数量", 5, 10, 10)
        product_rank = filtered_df.groupby('Product Name').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).sort_values('Sales', ascending=False).head(top_n).reset_index()
        
        fig_prod = go.Figure()
        fig_prod.add_trace(go.Bar(x=product_rank['Product Name'], y=product_rank['Sales'], name='销售额'))
        fig_prod.add_trace(go.Scatter(x=product_rank['Product Name'], y=product_rank['Profit'], name='利润', yaxis='y2'))
        
        fig_prod.update_layout(
            title='销售额与利润双轴对比',
            yaxis=dict(title='销售额'),
            yaxis2=dict(title='利润', overlaying='y', side='right'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_prod, use_container_width=True)

    with tabs[3]:
        st.subheader("多维交互数据探索")
        # 允许用户选择列进行快速分析
        group_col = st.selectbox("选择分组维度", ["Category", "Region", "Product Name"])
        metric_col = st.selectbox("选择统计指标", ["Sales", "Profit", "Quantity"])
        
        pivot_table = filtered_df.groupby(group_col)[metric_col].describe()
        st.dataframe(pivot_table.style.background_gradient(cmap='Blues'), use_container_width=True)

    # --- 底部交互 ---
    st.markdown("---")
    with st.expander("📥 导出筛选后的数据"):
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="下载 CSV 报告",
            data=csv,
            file_name=f'sales_report_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )

except Exception as e:
    st.error(f"发生错误: {e}")
    st.exception(e)
