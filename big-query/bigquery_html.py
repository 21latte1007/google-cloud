from bs4 import BeautifulSoup
from google.cloud import bigquery
import os

html = """
<html>
<head>
  <title>Example Title</title>
</head>
<body>
  <img src="example.jpg" alt="Example Image">
  <div class="content">Example Content</div>
</body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

title = soup.title.get_text()
image_url = soup.img['src']
content = soup.find('div', class_='content').get_text()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./key.json"

client = bigquery.Client()

data = [
  {
    'title': title,
    'image_url': image_url,
    'content': content
  }
]

table_id = <GCP BQ table>

client.insert_rows_json(table_id, data)
