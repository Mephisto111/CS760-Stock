from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
base_url = "https://forums.moneysavingexpert.com/search?domain=discussions&query=oil&sort=-dateInserted&scope=site&startDate=2019-12-31&endDate=2023-12-31&categoryOptions[0][value]=223&categoryOptions[0][label]=Auto-enrolment&categoryOptions[0][data][parentLabel]=Pensions,%20annuities%20&categoryOptions[1][value]=145&categoryOptions[1][label]=Boost%20your%20income&categoryOptions[1][data][parentLabel]=Home&categoryOptions[2][value]=17&categoryOptions[2][label]=Savings%20&categoryOptions[2][data][parentLabel]=Home&categoryOptions[3][value]=303&categoryOptions[3][label]=Ask%20An%20Expert&categoryOptions[3][data][parentLabel]=Home&categoryOptions[4][value]=305&categoryOptions[4][label]=Ask%20An%20Expert:%20Archive&categoryOptions[4][data][parentLabel]=Ask%20An%20Expert&includeChildCategories=true&source=community"
data = []

# 访问搜索结果页面
for i in range(1, 13):
    url = f"{base_url}&page={i}"
    driver.get(url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    discussion_links = [a['href'] for a in soup.select('a.css-3z45ni-ListItem-styles-titleLink')]


    def extract_data(driver, data):
        post_soup = BeautifulSoup(driver.page_source, 'html.parser')
        posts = post_soup.select('.Message.userContent')
        dates = post_soup.select('time')
        for post, date in zip(posts, dates):
            data.append({
                'Message': post.get_text(strip=True),
                'Date': date['datetime'].split('T')[0],
                'Time': date['datetime'].split('T')[1][:5],
            })


    for link in discussion_links:
        driver.get(link)
        time.sleep(10)

        # 提取当前页面的数据
        extract_data(driver, data)

        # 尝试找到并点击下一页链接
        next_page_links = driver.find_elements(By.CSS_SELECTOR, 'a.Next[rel="next"]')
        if next_page_links:
            next_page_links[0].click()
            time.sleep(10)  # 等待页面加载
            # 提取下一页的数据
            extract_data(driver, data)
# 定义一个提取数据的函数
df = pd.DataFrame(data)
df.to_excel('MSE_crude2.xlsx', index=False)

driver.quit()
