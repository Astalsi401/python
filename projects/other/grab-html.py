import pandas as pd
import requests
from bs4 import BeautifulSoup
response = requests.get("https://astalsi401.github.io/notes/fh4/upgrade.html")
soup = BeautifulSoup(response.content, "html.parser")
soup.encoding = 'utf-8'
result = soup.find_all(["h1"])
print(result)  # 輸出排版後的HTML內容


def OutputCSV():
    grabTest = 'D://documents//python//grab//SAMPLE.csv'
    df_SAMPLE = pd.DataFrame.from_dict(result)
    df_SAMPLE.to_csv(grabTest, index=False)
    print('成功產出'+grabTest)
