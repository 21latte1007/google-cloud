from google.cloud import bigquery
from google.oauth2 import service_account

KEY_PATH = "<<KEY_PATH>>"
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials = credentials, project = credentials.project_id)

################################################################################
# dataset_id = "{}.your_dataset".format(client.project)

# dataset = bigquery.Dataset(dataset_id)

# dataset.location = "US"

# dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
# print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

################################################################################
# table_id = f"{dataset.dataset_id}.sample"
table_id = "your_dataset.sample6"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField('Index', 'INTEGER'),
        bigquery.SchemaField('Series_reference', 'STRING'),
        bigquery.SchemaField("Period", "DATETIME"),
        bigquery.SchemaField('Data_value', 'FLOAT'),
        bigquery.SchemaField('Suppressed', 'STRING'),
        bigquery.SchemaField('STATUS', 'STRING'),
        bigquery.SchemaField('UNITS', 'STRING'),
        bigquery.SchemaField('Magnitude', 'INTEGER'),
        bigquery.SchemaField('Subject', 'STRING'),
        bigquery.SchemaField('Group', 'STRING'),
        bigquery.SchemaField('Series_title_1', 'STRING'),
        bigquery.SchemaField('Series_title_2', 'STRING'),
        bigquery.SchemaField('Series_title_3', 'STRING'),
        bigquery.SchemaField('Series_title_4', 'STRING'),
        bigquery.SchemaField('Series_title_5', 'STRING'),
        bigquery.SchemaField('No', 'INTEGER')
    ],
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
)
uri = 'gs://<<FILE_URL>>'

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)

load_job.result()

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
