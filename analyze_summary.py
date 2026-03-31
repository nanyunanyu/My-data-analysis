import pandas as pd

def analyze_data():
    try:
        df = pd.read_csv("ecommerce_sales_data.csv")
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        
        print("--- 数据概览 ---")
        print(f"总记录数: {len(df)}")
        print(f"时间范围: {df['Order Date'].min()} 至 {df['Order Date'].max()}")
        
        print("\n--- KPI 指标 ---")
        total_sales = df['Sales'].sum()
        total_profit = df['Profit'].sum()
        print(f"总销售额: {total_sales:,.2f}")
        print(f"总利润: {total_profit:,.2f}")
        print(f"平均利润率: {(total_profit/total_sales)*100:.2f}%")
        
        print("\n--- 各类别销售排行 ---")
        cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
        print(cat_sales)
        
        print("\n--- 各地区销售排行 ---")
        region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        print(region_sales)
        
        print("\n--- 热销产品 Top 5 ---")
        top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5)
        print(top_products)
        
    except Exception as e:
        print(f"分析出错: {e}")

if __name__ == "__main__":
    analyze_data()
