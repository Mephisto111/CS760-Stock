import requests
from bs4 import BeautifulSoup
import pandas as pd

# 初始化 DataFrame 列名
columns = ['Comment', 'Date', 'Time', 'Votes']
data = []  # 初始化存储数据的列表

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

# 遍历第1页到第300页
for page in range(1, 12):
    url = f"https://hotcopper.com.au/threads/crude-price.539751/page-{page}"
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 遍历帖子
    for post in soup.find_all('li', class_='post-message'):
        user_div = post.find('div', class_='user-username')
        username = user_div.a.get_text(strip=True) if user_div and user_div.a else 'Unknown User'

        comment_block = post.find('blockquote', class_='message-text')
        if comment_block:
            for blockquote in comment_block.find_all('blockquote'):
                blockquote.decompose()
            for attribution in comment_block.find_all('div', class_='attribution type'):
                attribution.decompose()
            comment = comment_block.get_text(strip=True, separator=' ')
        else:
            comment = 'No comment'

        post_date_div = post.find('div', class_='post-metadata-date')
        post_date = post_date_div.get_text(strip=True) if post_date_div else 'Unknown Date'

        post_time_div = post.find('div', class_='post-metadata-time')
        post_time = post_time_div.get_text(strip=True) if post_time_div else 'Unknown Time'

        votes_num = post.find('i', class_='votes-num')
        votes = votes_num.get_text(strip=True) if votes_num else '0'

        # 将信息添加到数据列表
        data.append({
            'Comment': comment,
            'Date': post_date,
            'Time': post_time,
            'Votes': votes
        })
        #print(f"Date: {post_date}")
        #print(f"Time: {post_time}")
# 创建 DataFrame 并存储到 Excel 文件
df = pd.DataFrame(data, columns=columns)
df.to_excel('hotcopper_crudenew31.xlsx', index=False)
