import pandas as pd
from google.cloud import bigquery
from colorama import Fore, Style
from pathlib import Path


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw data by
    - removing duplicates
    - filtering columns
    - transforming variables units
    """

    ### 1. removing duplicates
    df = df.drop_duplicates()
    print("✅ duplicates removed")


    ### 2. filtering columns
    ## filtering >30% nulls
    percent_missing  = df.isnull().sum()*100 / len(df)
    columns_below_30 = percent_missing[percent_missing < 30]

    # index to columns
    index_list = columns_below_30.reset_index()["index"].tolist()

    # filtering columns_below_30
    df = df[index_list].copy()
    print(f"✅ >30% nulls removed")


    ## filtering columns that are interesting to the project
    columns_to_keep = {
             "_PACAT3" :  "Physical Activity Categories",
             "_RFHYPE6":  "Adults who have been told they have high blood pressure by a doctor, nurse, or other health professional",
             "_RFCHOL3":  "Adults who have had their cholesterol checked and have been told by a doctor, nurse, or other health professional that it was high",
             "_MICHD"  :  "Respondents that have ever reported having coronary heart disease (CHD) or myocardial infarction (MI)",
             "_LTASTH1":  "Adults who have ever been told they have asthma",
             "_AGEG5YR":  "Fourteen-level age category",
             "_DRDXAR2":  "Respondents who have had a doctor diagnose them as having some form of arthritis",
             "HTM4"    :  "Reported height in meters",
             "WTKG3"   :  "Reported weight in kilograms",
             "_BMI5CAT":  "Four-level BMI categories",
             "_EDUCAG" :  "Calculated education level",
             "_INCOMG1":  "Calculated income level",
             "_PAINDX3":  "Physical Activity Index",
              "SEXVAR"  : "Sex of Respondent",
              "GENHLTH" : "General Health",
              "PHYSHLTH": "Number of Days Physical Health Not Good",
              "MENTHLTH": "Number of Days Mental Health Not Good",
              "CHECKUP1": "Length of time since last routine checkup",
              "EXERANY2": "Exercise in Past 30 Days",
              "EXRACT12": "Type of Physical Activity",
              "EXERHMM1": "Minutes or Hours Walking, Running, Jogging, or Swimming",
              "EXRACT22": "Other Type of Physical Activity Giving Most Exercise During Past Month",
              "CVDINFR4": "Ever Diagnosed with Heart Attack",
              "CVDCRHD4": "Ever Diagnosed with Angina or Coronary Heart Disease",
              "CVDSTRK3": "Ever Diagnosed with a Stroke",
              "CHCOCNC1": "(Ever told) (you had) melanoma or any other types of cancer?",
              "CHCCOPD3": "Ever told you had C.O.P.D. emphysema or chronic bronchitis?",
              "ADDEPEV3": "(Ever told) you had a depressive disorder",
              "CHCKDNY2": "Ever told you have kidney disease?",
              "DIABETE4": "(Ever told) you had diabetes",
              "DECIDE"  : "Because of a physical, mental, or emotional condition, do you have serious difficulty concentrating, remembering, or making decisions?",
              "DIFFALON": "Difficulty doing errands alone",
              "_PHYS14D": "3 level not good physical health status: 0 days, 1-13 days, 14-30 days",
              "_MENT14D": "3 level not good mental health status: 0 days, 1-13 days, 14-30 days",
              "MAXVO21_": "Estimated Age-Gender Specific Maximum Oxygen Consumption",
              "ACTIN13_": "Estimated Activity Intensity for First Activity",
              "STRFREQ_": "Strength Activity Frequency per Week",
              "PA3MIN_" : "Minutes of total Physical Activity per week"
              }
    df_filtered = df[columns_to_keep]
    print("✅ filtered columns")


    ### 3. transforming units of variables
    df["WTKG3"] = df["WTKG3"]/100
    print("✅ variable units transformed")

    print("✅ data cleaned")

    return df

def get_data(
        gcp_project:str,
        query:      str,
        cache_path: Path,
        data_has_header=False
    ) -> pd.DataFrame:
    """
    Retrieve `query` data from BigQuery, or from `cache_path` if the file exists
    Store at `cache_path` if retrieved from BigQuery for future use
    """
    if cache_path.is_file():
        print(Fore.BLUE + "\nLoad data from local CSV..." + Style.RESET_ALL)
        df = pd.read_csv(cache_path, header="infer" if data_has_header else None)
    else:
        print(Fore.BLUE + "\nLoad data from BigQuery server..." + Style.RESET_ALL)
        client    = bigquery.Client(project=gcp_project)
        query_job = client.query(query)
        result    = query_job.result()
        df        = result.to_dataframe()

        # Store as CSV if the BQ query returned at least one valid line
        if df.shape[0] > 1:
            df.to_csv(cache_path, header=data_has_header, index=False)

    print(f"✅ Data loaded, with shape {df.shape}")

    return df

def load_data_to_bq(
        data:        pd.DataFrame,
        gcp_project: str,
        bq_dataset:  str,
        table:       str,
        truncate:    bool
    ) -> None:
    """
    - Save the DataFrame to BigQuery
    - Empty the table beforehand if `truncate` is True, append otherwise
    """

    assert isinstance(data, pd.DataFrame)
    full_table_name = f"{gcp_project}.{bq_dataset}.{table}"
    print(Fore.BLUE + f"\nSave data to BigQuery @ {full_table_name}...:" + Style.RESET_ALL)

    ## Load data onto full_table_name
    data.columns = [f"_{column}" if not str(column)[0].isalpha() and not str(column)[0] == "_" else str(column) for column in data.columns]

    client = bigquery.Client()

    ## Define write mode and schema
    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    # print(f"\n{"Write" if truncate else "Append"} {full_table_name} ({data.shape[0]} rows)")

    ## Load data
    job    = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    result = job.result()  # wait for the job to complete

    print(f"✅ Data saved to bigquery, with shape {data.shape}")
