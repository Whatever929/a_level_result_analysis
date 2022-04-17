import numpy as np
from pathlib import Path
import pandas as pd
import glob
import re

CSV_PATH = Path("./csv/statistics")
OUTPUT_PATH = Path("./csv/clean")

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Fix one particular csv
problem_csv = "csv\statistics\Cambridge A Level results statistics - November 2017 (PDF, 96KB).csv"
df = pd.read_csv(problem_csv)
df.columns = df.columns.str.replace("ungrade", "ungraded")
df = df.drop('ungra', axis=1)
df.to_csv(problem_csv, index=False)


as_payload = {}
for i in CSV_PATH.glob("*AS*"):
    as_payload[i.stem] = pd.read_csv(i)


a_payload = {}
for i in CSV_PATH.glob("*[Aa] [Ll]evel*"):
    a_payload[i.stem] = pd.read_csv(i)


def standardize_columns(df_payload):
    column_set = set()

    for i in df_payload.values():
        if "Unnamed: 0" in i.columns and "Subject" not in i.columns:
            i.columns = i.columns.str.replace("Unnamed: 0", "Subject")
        column_set = column_set.union(set(i.columns))

    # Check that all entries have same columns.
    for i in df_payload.values():
        assert set(i.columns) == column_set

def concat_df(df_payload, col_to_check, invalid_value):
    df_list = []
    key_list = []

    for i, v in df_payload.items():
        v = remove_invalid_rows(v, col_to_check, invalid_value)
        year = re.search("20\d\d", i).group(0)
        month = re.search("June|November|March", i).group(0)
        df_list.append(v)
        key_list.append(year + " " + month)

    df_clean = pd.concat(df_list, keys=key_list)
    df_clean.index = df_clean.index.rename(['Series', 'Series_index'])
    return df_clean


def remove_invalid_rows(df, col_to_check, invalid_value):
    df = df.drop(df[df[col_to_check] == invalid_value].index)
    return df


standardize_columns(a_payload)
df_clean_a = concat_df(a_payload, "A*", "A*")
df_clean_a.to_csv(OUTPUT_PATH / "a_level_stat.csv")

standardize_columns(as_payload)
df_clean_as = concat_df(as_payload, "a", "a")
df_clean_as.to_csv(OUTPUT_PATH / "as_level_stat.csv")
