from google.cloud import bigquery
from google.oauth2 import service_account

KEY_PATH = "<<KEY_PATH>>"
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials = credentials, project = credentials.project_id)

dataset_id = '<<DATASET_ID>>'

bucket_name = '<<BUCKET_NAME>>'
file_name = '<<FILE_NAME>>'
    
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
        uri,
        table_ref,
        job_config=job_config
    )
    print('Started job {}'.format(load_job.job_id))
    load_job.result()
    print('Job finished.')
    destination_table = client.get_table(dataset_ref.table(table_id))
    print('Loaded {} rows.'.format(destination_table.num_rows))

else:
    print('Nothing To Do')
