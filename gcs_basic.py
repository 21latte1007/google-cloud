from google.cloud import storage
from google.oauth2 import service_account

# 서비스 계정 인증 정보가 담긴 JSON 파일 경로
KEY_PATH = "<<KEY_PATH>>"
# Credentials 객체 생성
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
# 구글 스토리지 클라이언트 객체 생성
client = storage.Client(credentials = credentials, project = credentials.project_id)
# buckets = list(client.list_buckets())

# 버킷 이름
bucket_name = "<<BUCKET_NAME>>"
# 스토리지 클래스 - ex. STANDARD: 표준
storage_class = "STANDARD"
# 버킷 위치 - ex. asia-northeast3: 서울
location = "asia-northeast3"
# 사전 정의된 ACL - ex. public-read 공개 읽기
predefined_acl = "public-read"
# 사전 정의된 객체 ACL - ex. public-read 공개 읽기
predefined_default_object_acl = "public-read"

# 버킷 객체 생성
bucket = client.bucket(bucket_name)
# 스토리지 클래스 설정
bucket.storage_class = storage_class
# 버킷 생성
bucket = client.create_bucket(
    bucket,
    location=location,
    predefined_acl=predefined_acl,
    predefined_default_object_acl=predefined_default_object_acl,
)

# 버킷 ID
bucket.id

################################################
# 파일 업로드
################################################

# 버킷 이름
bucket_name = "<<BUCKET_NAME>>"
# 블랍 이름
blob_name = "<<BLOB_NAME>>"
# 적재할 파일 경로
file_path = "<FILE_PATH>>"

# 버킷 선택
bucket = client.get_bucket(bucket_name)
# 블랍 객체 생성
blob = bucket.blob(blob_name)
# 파일 업로드
blob.upload_from_filename(file_path)

# 버킷에 업로드된 객체의 공개 URL
blob.public_url

################################################
# 파일 다운로드
################################################

# GCP에 저장되어 있는 파일 명
# source_blob_name = '<<BLOB_NAME>>'
# 다운받을 파일을 저장할 경로("local/path/to/file")
# destination_file_name = '<<FILE_PATH>>'

# bucket = client.get_bucket(bucket_name)
# blob = bucket.blob(source_blob_name)

# blob.download_to_filename(destination_file_name)

# 이하 오류 발생하는 코드
# storage_client = storage.Client()
# bucket = storage_client.bucket(bucket_name)

################################################
# 객체를 메모리에 다운로드
################################################

# client = storage.Client()
# bucket = client.bucket(bucket_name)

# blob = bucket.blob(source_blob_name)
contents = blob.download_as_string()
print(contents)

################################################
# 파일 이어서 다운로드
###############################################

# bucket = client.bucket(bucket_name)

# blob = bucket.blob(source_blob_name)
# blob.download_to_filename(destination_file_name, start=start_byte, end=end_byte)

################################################
# 파일 복사
################################################

# destination_bucket_name = "<<BUCKET_NAME>>"
# destination_blob_name = "<<BUCKET_NAME>>"

# source_bucket = client.bucket(bucket_name)
# source_blob = source_bucket.blob(blob_name)
# destination_bucket = client.bucket(destination_bucket_name)

# blob_copy = source_bucket.copy_blob(
#     source_blob, destination_bucket, destination_blob_name
# )

################################################
# 파일 이름 변경
################################################

# new_name = "<<NEW_NAME>>"

# bucket = client.bucket(bucket_name)
# blob = bucket.blob(blob_name)

# new_blob = bucket.rename_blob(blob, new_name)

################################################
# 파일 이동
################################################

# destination_bucket_name = "<<BUCKET_NAME>>"
# destination_blob_name = "<<BLOB_NAME>>"

# source_bucket = client.bucket(bucket_name)
# source_blob = source_bucket.blob(blob_name)
# destination_bucket = client.bucket(destination_bucket_name)

# blob_copy = source_bucket.copy_blob(
#     source_blob, destination_bucket, destination_blob_name
# )
# source_bucket.delete_blob(blob_name)

################################################
# 파일 삭제
################################################

# bucket = client.bucket(bucket_name)
# blob = bucket.blob(blob_name)
# blob.delete()

################################################
