import csv
import time

import praw
from datetime import datetime
import datetime as dt
from psaw import PushshiftAPI
import pandas as pd
# 使用你的Reddit应用凭证
reddit = praw.Reddit(
    client_id='Poo95RsW5qvee4BzWttxLQ',  # 替换为你的client_id
    client_secret='AJEgqQcdcw_HBAGiFZR_RTME210Frg',  # 替换为你的client_secret
    user_agent='test script by /u/Distinct-Oil5495',
    username = 'Distinct-Oil5495',
    password = 'myq200221'
)

subreddit = reddit.subreddit('stocks')  # 指定子版块
query = "crude"  # 搜索关键词

# 文件路径
filename = "D:\\pa\\oil.csv"
last_post_file = "D:\\pa\\last_post_id.txt"

# 尝试从文件读取最后处理的帖子ID
try:
    with open(last_post_file, 'r') as f:
        last_post_id = f.read().strip()
except FileNotFoundError:
    last_post_id = None

# 批次控制参数
batch_size = 100
total_batches = 5
current_batch = 0

# 开始写入CSV
with open(filename, 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(["Comment Time", "Comment", "Upvotes"])

    # 使用search查询特定关键词的帖子
    searched_posts = list(subreddit.search(query, sort='new', limit=None))
    post_processed = False

    for submission in searched_posts:
        if last_post_id and submission.id == last_post_id:
            post_processed = True
            continue  # 跳过之前处理过的帖子
        if post_processed or not last_post_id:
            # 处理帖子的评论
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comment_time = datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([comment_time, comment.body, comment.score])
            last_processed_id = submission.id  # 更新最后处理的帖子ID

            # 检查是否完成一个批次
            current_batch += 1
            if current_batch % batch_size == 0:
                print(f"Completed batch {current_batch // batch_size} of {total_batches}")
                if (current_batch // batch_size) == total_batches:
                    break  # 完成指定数量的批次
                time.sleep(10)

    # 保存最后处理的帖子ID
    if current_batch > 0:  # 确保有帖子被处理
        with open(last_post_file, 'w') as f:
            f.write(last_processed_id)