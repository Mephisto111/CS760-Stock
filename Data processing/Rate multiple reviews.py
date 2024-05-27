# 处理每个数据集
for file_name in file_names:
    print(f"Processing file: {file_name}")
    data = pd.read_csv(file_name)

    for index, row in data.iterrows():
        print(f"Processing comment {index + 1}/{len(data)} in {file_name}")
        data.at[index, 'Response'] = get_scores(row['comment'])
        time.sleep(1)  # 延迟1秒避免速率限制

    # 将当前数据集追加到all_data中
    all_data = pd.concat([all_data, data], ignore_index=True)

# 保存所有结果到一个文件
output_path = '评分_all_data.csv'
all_data.to_csv(output_path, index=False)

print("Processing completed. Results saved to 评分_all_data.csv")
