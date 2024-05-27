# -*- coding: utf-8 -*-
"""
Created on Fri May 24 15:29:13 2024

@author: 86188
"""
import pandas as pd
from snownlp import SnowNLP
import re
data = pd.read_csv('random_sample_reddit_comments.csv')

# 从 Response 列中提取 Sentiment score
def extract_sentiment_score(response):
    match = re.search(r'Sentiment score: (-?\d+)', response)
    if match:
        return int(match.group(1))
    return None

data['extracted_sentiment_score'] = data['Response'].apply(extract_sentiment_score)

# 删除含有缺失值的行
data.dropna(subset=['extracted_sentiment_score'], inplace=True)

# 使用 SnowNLP 分析每条评论的情感
sentiment_scores_snownlp = []

for comment in data["comment"]:
    s = SnowNLP(comment)
    sentiment_scores_snownlp.append(s.sentiments)

# 将 SnowNLP 的情感得分转换到 -100 到 100 的区间
def scale_sentiment_score(score):
    scaled_score = score * 200 - 100
    # 将得分调整为 5 的倍数
    return round(scaled_score / 5) * 5

scaled_sentiment_scores = [scale_sentiment_score(score) for score in sentiment_scores_snownlp]

# 添加转换后的情感得分到数据框
data["sentiment_score"] = scaled_sentiment_scores

# 计算每一行的情感得分与提取的 Sentiment score 之间的距离
def calculate_individual_correlation(row):
    distance = abs(row["sentiment_score"] - row["extracted_sentiment_score"])
    # 将距离转换到 0 到 100 的区间，距离越小相关性越高
    max_distance = 200  # 最大可能距离（-100到100）
    scaled_correlation = (1 - distance / max_distance) * 100
    # 将相关性分数调整为 5 的倍数
    return round(scaled_correlation / 5) * 5

# 为每行添加相关性分数
data["relatedness"] = data.apply(calculate_individual_correlation, axis=1)

# 保存结果到 snownlp评分.csv 文件中
data.to_csv('snownlp评分.csv', index=False)


import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk
nltk.download('movie_reviews')
nltk.download('punkt')

# 使用 TextBlob 的默认分析器分析每条评论的情感
sentiment_scores_default = []

for comment in data["comment"]:
    analysis = TextBlob(comment)
    sentiment_scores_default.append(analysis.sentiment.polarity)

# 添加默认分析器的情感得分到数据框
data["calculated_sentiment_score_default"] = sentiment_scores_default

# 使用 NaiveBayesAnalyzer 分析每条评论的情感
sentiment_scores_naive = []

for comment in data["comment"]:
    s = TextBlob(comment, analyzer=NaiveBayesAnalyzer())
    # 计算情感得分为正面概率减去负面概率
    sentiment_score = s.sentiment.p_pos - s.sentiment.p_neg
    sentiment_scores_naive.append(sentiment_score)

# 添加 NaiveBayesAnalyzer 的情感得分到数据框
data["calculated_sentiment_score_naive"] = sentiment_scores_naive

# 保存结果到 TextBlob评分.csv 文件中
data.to_csv('TextBlob评分.csv', index=False)

# 显示更新后的数据框
print(data.head())




import pandas as pd

data1 = pd.read_csv('clean_sampled_data2_modified.csv')
data2 = pd.read_csv('评分_all_data_modified.csv')

# Calculating positive and negative rates for both datasets
positive_rate_1 = (data1['Sentiment score'] > 0).mean()
negative_rate_1 = (data1['Sentiment score'] <= 0).mean()

positive_rate_2 = (data2['Sentiment score'] > 0).mean()
negative_rate_2 = (data2['Sentiment score'] <= 0).mean()

# Creating a table for positive and negative rates
sentiment_rate_table = pd.DataFrame({
    'Dataset': ['Scored item by item', 'Combined ratings'],
    'Positive Rate': [positive_rate_1, positive_rate_2],
    'Negative Rate': [negative_rate_1, negative_rate_2]
})

# Creating distribution tables for Sentiment score and Relatedness
bins_sentiment = [-100, -50, 0, 50, 100]
bins_relatedness = [0, 25, 50, 75, 100]

sentiment_distribution_1 = pd.cut(data1['Sentiment score'], bins=bins_sentiment).value_counts(normalize=True).sort_index()
sentiment_distribution_2 = pd.cut(data2['Sentiment score'], bins=bins_sentiment).value_counts(normalize=True).sort_index()

relatedness_distribution_1 = pd.cut(data1['Relatedness'], bins=bins_relatedness).value_counts(normalize=True).sort_index()
relatedness_distribution_2 = pd.cut(data2['Relatedness'], bins=bins_relatedness).value_counts(normalize=True).sort_index()

# Creating tables for the distributions
sentiment_distribution_table = pd.DataFrame({
    'Scored item by item': sentiment_distribution_1,
    'Combined ratings': sentiment_distribution_2
})

relatedness_distribution_table = pd.DataFrame({
    'Scored item by item': relatedness_distribution_1,
    'Combined ratings': relatedness_distribution_2
})

# Displaying the results
print("Positive and Negative Rates Table:")
print(sentiment_rate_table)
print("\nSentiment Score Distribution Table:")
print(sentiment_distribution_table)
print("\nRelatedness Distribution Table:")
print(relatedness_distribution_table)



import numpy as np
import pandas as pd

# 假设 sentiment_data 是包含情感得分数据的 DataFrame
sentiment_data = pd.read_csv("st.csv")
# 将情感得分转换为数值类型
sentiment_data['Response_textblob'] = sentiment_data['Response_textblob'].str.extract(r'(-?\d+)').astype(float)
sentiment_data['Response_gpt'] = sentiment_data['Response_gpt'].str.extract(r'(-?\d+)').astype(float)
sentiment_data['Response_snownlp'] = sentiment_data['Response_snownlp'].str.extract(r'(-?\d+)').astype(float)


# 计算积极率、消极率及区间分布的函数
def calculate_statistics(sentiment_scores):
    positive_rate = np.mean(sentiment_scores >= 0)
    negative_rate = np.mean(sentiment_scores < 0)
    median = np.median(sentiment_scores)
    mean = np.mean(sentiment_scores)
    intervals = {
        '[-100, -50)': np.mean((sentiment_scores >= -100) & (sentiment_scores < -50)),
        '[-50, -10)': np.mean((sentiment_scores >= -50) & (sentiment_scores < -10)),
        '[-10, 0)': np.mean((sentiment_scores >= -10) & (sentiment_scores < 0)),
        '[0, 10)': np.mean((sentiment_scores >= 0) & (sentiment_scores < 10)),
        '[10, 50)': np.mean((sentiment_scores >= 10) & (sentiment_scores < 50)),
        '[50, 100]': np.mean((sentiment_scores >= 50) & (sentiment_scores <= 100))
    }
    return positive_rate, negative_rate, intervals, median, mean

# 计算每个模型的统计数据
statistics_textblob = calculate_statistics(sentiment_data['Response_textblob'])
statistics_gpt = calculate_statistics(sentiment_data['Response_gpt'])
statistics_snownlp = calculate_statistics(sentiment_data['Response_snownlp'])

# 创建汇总表格
summary_data = {
    'Model': ['TextBlob', 'GPT', 'SnowNLP'],
    'Positive Rate': [statistics_textblob[0], statistics_gpt[0], statistics_snownlp[0]],
    'Negative Rate': [statistics_textblob[1], statistics_gpt[1], statistics_snownlp[1]],
    'Median': [statistics_textblob[3], statistics_gpt[3], statistics_snownlp[3]],
    'Mean': [statistics_textblob[4], statistics_gpt[4], statistics_snownlp[4]],
    '[-100, -50)': [statistics_textblob[2]['[-100, -50)'], statistics_gpt[2]['[-100, -50)'], statistics_snownlp[2]['[-100, -50)']],
    '[-50, -10)': [statistics_textblob[2]['[-50, -10)'], statistics_gpt[2]['[-50, -10)'], statistics_snownlp[2]['[-50, -10)']],
    '[-10, 0)': [statistics_textblob[2]['[-10, 0)'], statistics_gpt[2]['[-10, 0)'], statistics_snownlp[2]['[-10, 0)']],
    '[0, 10)': [statistics_textblob[2]['[0, 10)'], statistics_gpt[2]['[0, 10)'], statistics_snownlp[2]['[0, 10)']],
    '[10, 50)': [statistics_textblob[2]['[10, 50)'], statistics_gpt[2]['[10, 50)'], statistics_snownlp[2]['[10, 50)']],
    '[50, 100]': [statistics_textblob[2]['[50, 100]'], statistics_gpt[2]['[50, 100]'], statistics_snownlp[2]['[50, 100]']]
}

summary_df = pd.DataFrame(summary_data)

# 输出表格
print(summary_df)


# 计算中位数和均值
median_mean_table = pd.DataFrame({
    'Dataset': ['Scored item by item', 'Combined ratings'],
    'Sentiment Score Median': [data1['Sentiment score'].median(), data2['Sentiment score'].median()],
    'Sentiment Score Mean': [data1['Sentiment score'].mean(), data2['Sentiment score'].mean()],
    'Relatedness Median': [data1['Relatedness'].median(), data2['Relatedness'].median()],
    'Relatedness Mean': [data1['Relatedness'].mean(), data2['Relatedness'].mean()]
})

# 显示结果
print("Median and Mean Table:")
print(median_mean_table)