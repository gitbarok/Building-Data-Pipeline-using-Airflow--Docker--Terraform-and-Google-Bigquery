import pandas as pd
import os

from google.cloud import bigquery
from google.oauth2 import service_account


def load_to_bq(filename):
    # Define Variable
    SERVICE_ACCOUNT_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    PROJECT_ID = "tactile-vehicle-351405"
    TABLE_ID = f"{PROJECT_ID}.jti_ulm_scrape.jtiulm_paper_details"

    df = pd.read_csv(filename)

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_CREDENTIALS
    )
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

    job = client.load_table_from_dataframe(df, TABLE_ID)
    job.result()
    print("There are {0} rows added/changed".format(len(df)))


if __name__ == "__main__":
    load_to_bq()
