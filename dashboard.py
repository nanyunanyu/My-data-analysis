import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 设置页面配置
st.set_page_config(page_title="电商销售数据分析 Dashboard", layout="wide")

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_sales_data.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

try:
    df = load_data()

    # 侧边栏过滤器
    st.sidebar.header("过滤器")
    
    # 日期范围选择
    min_date = df['Order Date'].min().to_pydatetime()
    max_date = df['Order Date'].max().to_pydatetime()
    date_range = st.sidebar.date_input(
        "选择日期范围",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # 类别选择
    categories = st.sidebar.multiselect(
        "选择商品类别",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )

    # 地区选择
    regions = st.sidebar.multiselect(
        "选择地区",
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )

    # 根据过滤器筛选数据
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = (
            (df['Order Date'].dt.date >= start_date) & 
            (df['Order Date'].dt.date <= end_date) &
            (df['Category'].isin(categories)) &
            (df['Region'].isin(regions))
        )
        filtered_df = df.loc[mask]
    else:
        filtered_df = df

    # 主界面标题
    st.title("📊 电商销售数据分析 Dashboard")
    st.markdown("---")

    # KPI 指标
    col1, col2, col3, col4 = st.columns(4)
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_quantity = filtered_df['Quantity'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    col1.metric("总销售额", f"¥{total_sales:,.2f}")
    col2.metric("总利润", f"¥{total_profit:,.2f}")
    col3.metric("总销量", f"{total_quantity:,}")
    col4.metric("利润率", f"{profit_margin:.2f}%")

    st.markdown("---")

    # 图表展示
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("销售额趋势")
        sales_trend = filtered_df.groupby('Order Date')['Sales'].sum().reset_index()
        fig_trend = px.line(sales_trend, x='Order Date', y='Sales', title='每日销售趋势')
        st.plotly_chart(fig_trend, use_container_width=True)

    with row1_col2:
        st.subheader("各类别销售分布")
        cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
        fig_cat = px.pie(cat_sales, values='Sales', names='Category', hole=0.4, title='类别销售占比')
        st.plotly_chart(fig_cat, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("各地区销售情况")
        region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
        fig_region = px.bar(region_sales, x='Region', y='Sales', color='Region', title='地区销售对比')
        st.plotly_chart(fig_region, use_container_width=True)

    with row2_col2:
        st.subheader("利润与销售额关系")
        fig_scatter = px.scatter(filtered_df, x='Sales', y='Profit', color='Category', 
                                 size='Quantity', hover_name='Product Name', title='销售额 vs 利润')
        st.plotly_chart(fig_scatter, use_container_width=True)

    # 底部详情
    st.markdown("---")
    st.subheader("热销产品排行 (Top 10)")
    top_products = filtered_df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Quantity': 'sum',
        'Profit': 'sum'
    }).sort_values(by='Sales', ascending=False).head(10)
    st.table(top_products)

    # 数据预览
    with st.expander("查看原始数据"):
        st.dataframe(filtered_df)

except Exception as e:
    st.error(f"加载数据时出错: {e}")
    st.info("请确保 ecommerce_sales_data.csv 文件存在且格式正确。")
