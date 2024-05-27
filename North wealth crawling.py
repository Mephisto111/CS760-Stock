import requests
from lxml import etree
import pandas as pd
import time

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
})
# 设置Cookies
cookies = {
    'qgqp_b_id': '7fd73963095413a1762a480d08031674',
    'ut': 'FobyicMgeV5lCsvMiCrEnniAjmmm8aXkxm6lOnUWrd0wbvfxOmv3VuPv7WoDVcM4mIdpDtJKfA1KtrX5h7ULklcdAiOnwl5X2L-cuYl-IT8M48a7ooJme2ZXsuzMGdqoLP-cUg05u9sUu4W2wHyt3ZJcFeUw4au_hrEydhWuhwV4vZzO2sraGDfBO2C1f42NbiKT6KrPXKazKKGCEQ6AZO2Efs-iblhJrzjNVG9c3PtEVnZ9OPKaBIogPoSXY1Y1pfQlYb8Z4e9dJz_t8yNE2VetQWVtZ7Sj',
    'uidal': '3536077120648128%e8%82%a1%e5%8f%8b19352IF918'
}
session.cookies.update(cookies)
# 确定页码范围
start_page = 41
end_page = 50
pages_per_batch = 10  # 每个批次的页数
pause_after_pages = 10  # 每爬取20页后暂停
pause_duration = 15  # 暂停时长，单位秒

for start in range(start_page, end_page + 1, pages_per_batch):
    all_titles = []
    all_times = []

    for page in range(start, min(start + pages_per_batch, end_page + 1)):
        print(f'Crawling page {page}')
        url = f'https://guba.eastmoney.com/list,of161129_{page}.html'

        try:
            response = session.get(url)  # 使用带有Cookies的Session发起请求
            if response.status_code == 200:
                root = etree.HTML(response.content)
                titles = root.xpath("//*[@id='articlelistnew']/div/span[3]/a//text()")
                times = root.xpath("//*[@id='articlelistnew']/div/span[5]//text()")
                times_clean = times[1:]
                all_titles.extend(titles)
                all_times.extend(times_clean)
            else:
                print(f'Response {response.status_code} for page {page}')
        except Exception as e:
            print(f'Failed to crawl page {page}: {e}')
        time.sleep(10)

    # 保存当前批次的数据到CSV
    if all_titles and all_times:
        batch_data = pd.DataFrame({'title': all_titles, 'time': all_times})
        csv_filename = f'guba_data_pages_{start}_to_{min(start + pages_per_batch - 1, end_page)}.csv'
        batch_data.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f'Saved {csv_filename}')

    # 每爬取指定页数后暂停一段时间
    print(f'Pausing for {pause_duration} seconds...')
    time.sleep(pause_duration)

session.close()
