## 파일 생성
from google.cloud import storage
from google.cloud import bigquery

def gcs2bq(event, context):
    client = bigquery.Client()

    dataset_id = 'your_dataset'
    bucket_name = event['bucket']
    file_name = event['name']
    
    table_id = file_name.split('.')[0]
    file_ext = file_name.split('.')[-1]

    if file_ext == 'csv':
        uri = 'gs://' + bucket_name + '/' + file_name
        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)

        job_config = bigquery.LoadJobConfig()
        job_config.autodetect = True
        job_config.schema_update_options = [
            bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
        ]
        job_config.create_disposition = [
            bigquery.CreateDisposition.CREATE_IF_NEEDED
        ]

        load_job = client.load_table_from_uri(
            uri, table_ref, job_config=job_config
        )
        
        load_job.result()
        destination_table = client.get_table(dataset_ref.table(table_id))

    else:
        print('Not CSV File')

## 파일 삭제
from google.cloud import storage
from google.cloud import bigquery

def start_func(event, request):
    client = bigquery.Client()
    dataset_id = 'your_dataset'

    bucket_name = event['bucket']
    # file_name = event['name']
    file_name = 'updated_csv_file.csv'
    table_id = file_name.split('.')[0]
    file_ext = file_name.split('.')[-1]
    
    if file_ext == 'csv':
        uri = 'gs://' + bucket_name + '/' + file_name
        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)

        job_config = bigquery.LoadJobConfig()
        job_config.autodetect = True
        job_config.schema_update_options = [
            bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
        ]
        job_config.create_disposition = [
            bigquery.CreateDisposition.CREATE_IF_NEEDED
        ]

        load_job = client.load_table_from_uri(
            uri, table_ref, job_config = job_config
        )

        print('Started job {}'.format(load_job.job_id))
        load_job.result()
        print('Job finished.')
        destination_table = client.get_table(dataset_ref.table(table_id))
        print('Loaded {} rows.'.format(destination_table.num_rows))
    else :
        file = event
        print(f"Processing file: {file['name']}. Not CSV")
    # bucket_name = "test_youngbeom"
    # blob_text = "sample-test"
    # destination_blob_name = "ljk-bucket-sample-txt"
    # upload_blob(bucket_name, blob_text, destination_blob_name)  
    # hello_gcs(event, request)
    # return 'Success!'

def upload_blob(bucket_name, blob_text, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    print(f"upload_blob-1 = {bucket_name} + {blob_text} +  {destination_blob_name} ")
    blob.upload_from_string(blob_text)

# def hello_gcs(event, context):
#     file = event
#     print(f"Processing file: {file['name']}.")
