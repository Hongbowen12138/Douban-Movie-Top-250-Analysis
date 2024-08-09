import pandas as pd
import plotly.graph_objects as go
import os

# 创建输出目录
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 读取Excel文件
input_file = os.path.join(output_dir, "豆瓣电影top250数据_年份类型拆分.xlsx")
df = pd.read_excel(input_file)

# 按照年份进行分组统计，计算每个年份对应电影的数量
year_counts = df["年份"].value_counts().reset_index()
year_counts.columns = ["年份", "数量"]
year_counts = year_counts.sort_values(by="年份")

# 绘制柱状图
fig = go.Figure(data=[go.Bar(x=year_counts["年份"], y=year_counts["数量"], marker_color='skyblue')])

# 设置图形样式与标题
fig.update_layout(
    title="豆瓣电影Top 250年份与电影数量柱状图",
    xaxis_title="年份",
    yaxis_title="电影数量",
    xaxis=dict(tickmode='linear'),
    template="plotly_white"
)

# 设置悬停文本，显示年份和对应的电影数量
fig.update_traces(hovertemplate="年份: %{x}<br>数量: %{y}")

# 保存并显示交互式柱状图
output_file = os.path.join(output_dir, "豆瓣电影评分分布柱状图.html")
fig.write_html(output_file)
print(f"图表已成功保存为：{output_file}")
fig.show()
