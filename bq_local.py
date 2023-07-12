from google.cloud import bigquery
from google.oauth2 import service_account

KEY_PATH = "<<KEY_PATH>>"
# Credentials 객체 생성
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
# 구글 스토리지 클라이언트 객체 생성
client = bigquery.Client(credentials = credentials, project = credentials.project_id)

query_job = client.query(
    """
    SELECT
      CONCAT(
        'https://stackoverflow.com/questions/',
        CAST(id as STRING)) as url,
      view_count
    FROM `bigquery-public-data.stackoverflow.posts_questions`
    WHERE tags like '%google-bigquery%'
    ORDER BY view_count DESC
    LIMIT 10"""
)

results = query_job.result()  # Waits for job to complete.

for row in results:
    print("{} : {} views".format(row.url, row.view_count))
