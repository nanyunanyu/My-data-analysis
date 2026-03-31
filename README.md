# 电商销售数据分析 Dashboard

这是一个使用 Streamlit 构建的数据可视化 Dashboard。

## 本地运行

1. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. 运行应用:
   ```bash
   streamlit run dashboard.py
   ```

## 部署到服务器

### 方式一：Streamlit Cloud (推荐)
- 将代码上传到 GitHub。
- 在 [Streamlit Cloud](https://share.streamlit.io/) 中连接你的仓库即可一键部署。

### 方式二：云服务器 (Ubuntu/CentOS)
1. 安装 Python 3.9+。
2. 克隆项目。
3. 创建虚拟环境并安装依赖。
4. 使用 `nohup` 或 `pm2` 运行:
   ```bash
   nohup streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 &
   ```
5. 在云服务器防火墙开启 8501 端口。
