from bs4 import BeautifulSoup
from google.cloud import bigquery
from google.oauth2 import service_account

# Parse the HTML
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

# Extract the title, image URL, and content
title = soup.title.get_text()
image_url = soup.img['src']
content = soup.find('div', class_='content').get_text()

# Connect to BigQuery
# client = bigquery.Client()
KEY_PATH = "<<KEY_PATH>>"
# Credentials 객체 생성
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
# 구글 스토리지 클라이언트 객체 생성
client = bigquery.Client(credentials = credentials, project = credentials.project_id)

# Prepare the data
data = [
    {
        'title': title,
        'image_url': image_url,
        'content': content
    }
]

# Insert the data into BigQuery
table_id = '<<BQ_TABLE_ID>>'

errors = client.insert_rows_json(table_id, data)
if errors:
    print('Error inserting rows:', errors)
else:
    print('Data inserted successfully')
