import requests
from lxml import etree
import pandas as pd
import re
import time
import random
import os

# 定义请求头信息
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
    )
}

# 定义辅助函数：获取列表首个元素并去除其两端空格
def get_first_text(text_list: list[str]) -> str:
    try:
        return text_list[0].strip()
    except IndexError:
        return ""

# 创建输出目录
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 初始化数据存储结构
COLUMNS = ["序号", "标题", "链接", "评分", "年份和类型", "参演人员"]
df = pd.DataFrame(columns=COLUMNS)

# 计算并生成豆瓣电影Top 250分页URL列表
START_OFFSETS = range(0, 250, 25)
URLS = [
    "https://movie.douban.com/top250?start={}&filter=".format(offset)
    for offset in START_OFFSETS
]

# 遍历每个分页URL，抓取并解析电影信息
for index, url in enumerate(URLS, start=1):
    try:
        print(f"Fetching URL: {url}")
        # 发起网络请求
        response = requests.get(url=url, headers=HEADERS)
        response.raise_for_status()

        # 解析响应的HTML文本为ElementTree对象
        html = etree.HTML(response.text)
        movie_lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li')

        # 遍历每个电影li元素，提取并处理电影信息
        for li in movie_lis:
            title = get_first_text(li.xpath("./div/div[2]/div[1]/a/span[1]/text()"))
            link = get_first_text(li.xpath("./div/div[2]/div[1]/a/@href"))
            score = get_first_text(li.xpath("./div/div[2]/div[2]/div/span[2]/text()"))
            yearandtype = get_first_text(li.xpath("./div/div[2]/div[2]/p[1]/text()[2]"))
            actor = get_first_text(li.xpath("./div/div[2]/div[2]/p[1]/text()"))

            print(f"Fetched movie: {title}, Score: {score}, Year and Type: {yearandtype}, Actors: {actor}")
            df.loc[len(df.index)] = [index, title, link, score, yearandtype, actor]

        # 增加一个随机延迟时间
        time.sleep(random.uniform(1, 5))

    except requests.RequestException as e:
        print(f"请求失败：{e}")
    except Exception as e:
        print(f"解析或处理数据时发生错误：{e}")

# 将DataFrame中的数据保存为Excel文件
df.to_excel(os.path.join(output_dir, "豆瓣电影top250数据.xlsx"), sheet_name="豆瓣电影top250数据", na_rep="")

# 读取已生成的Excel文件
df = pd.read_excel(os.path.join(output_dir, "豆瓣电影top250数据.xlsx"), sheet_name="豆瓣电影top250数据")

# 使用 split() 函数拆分年份和类型
df["年份"] = df["年份和类型"].apply(lambda x: re.sub(r"\D", "", x.split("/")[0]).lstrip())
df["类型"] = df["年份和类型"].apply(lambda x: " ".join(x.split("/")[1:]).replace("/", ""))

# 删除旧的“年份和类型”列
df.drop("年份和类型", axis=1, inplace=True)

# 保存更新后的DataFrame到Excel文件
df.to_excel(os.path.join(output_dir, "豆瓣电影top250数据_年份类型拆分.xlsx"), sheet_name="豆瓣电影top250数据", index=False)

print("年份和类型已拆分为独立列,并分别进行了清理,保存到新文件: output/豆瓣电影top250数据_年份类型拆分.xlsx")
print("Excel文件已经生成!")
