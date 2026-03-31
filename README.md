# 高级电商销售数据分析 Dashboard

这是一个基于 Streamlit 和 Plotly 构建的交互式数据可视化系统。

## 功能特性
- **实时 KPI 监控**：销售额、利润率、客单价等核心指标实时滚动。
- **多维趋势分析**：支持按日/周/月切换的销售趋势探索。
- **深度穿透图表**：使用 Sunburst 图表展示类别与产品的层级关系。
- **动态交互筛选**：侧边栏联动过滤，所有图表秒级响应。
- **数据导出**：支持一键导出筛选后的报表数据。

## 本地开发运行

1. **环境准备**：
   建议使用 Python 3.9+。
   
2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **启动应用**：
   ```bash
   streamlit run dashboard.py
   ```

---

## Windows 环境部署指南

在 Windows 服务器上部署 Streamlit 有多种方案，以下推荐两种最稳健的方法：

### 方案一：使用 NSSM 将其注册为系统服务（推荐）
这种方式可以确保应用在服务器重启后自动启动，且在后台静默运行。

1. **下载 NSSM**：访问 [nssm.cc](https://nssm.cc/download) 下载并解压。
2. **编写启动脚本**：在项目根目录创建 `run_app.bat`：
   ```batch
   @echo off
   cd /d D:\桌面\data_analyst
   call .\venv\Scripts\activate
   streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
   ```
3. **安装服务**：
   打开管理员权限的 PowerShell，进入 nssm 所在目录：
   ```powershell
   .\nssm.exe install EcommerceDashboard "D:\桌面\data_analyst\run_app.bat"
   ```
4. **启动服务**：
   ```powershell
   nssm start EcommerceDashboard
   ```

### 方案二：使用 Task Scheduler (任务计划程序)
1. 打开 **任务计划程序**。
2. 创建基本任务，设置触发器为 "计算机启动时"。
3. 操作选择 "启动程序"，程序脚本指向上面的 `run_app.bat`。
4. 在属性中勾选 "不管用户是否登录都要运行"。

### 方案三：IIS 反向代理 (进阶)
如果你需要通过域名（如 `http://data.yourcompany.com`）访问：
1. 安装 IIS 和 **Application Request Routing (ARR)** 模块。
2. 在 IIS 中启用 Proxy。
3. 创建 Web 站点，配置 **URL 重写** 规则，将流量转发到 `http://localhost:8501`。

---

## 通用部署建议

### 1. 端口开放
确保 Windows 防火墙已入站规则中允许 **8501** 端口的 TCP 流量。

### 2. 云服务器 (Ubuntu/CentOS)
```bash
nohup streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 &
```
