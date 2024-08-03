import json
import pandas as pd
from pathlib import Path
from helper import add_units_dates, concatenate_actions, concatenate_vectors


def get_transformed_dataset():
    dtypes = json.loads(Path("data/dtypes.json").read_text())
    df = pd.read_csv("data/vcdb.csv", dtype=dtypes)
    
    # Remove columns with only empty values
    df.dropna(axis="columns", how="all", inplace=True)
    
    # Filter old incidents
    since = 2013
    until = 2024
    df.drop(df.loc[df["timeline.incident.year"] < since].index, inplace=True)
    df.drop(df.loc[df["timeline.incident.year"] > until].index, inplace=True)
    
    # Add column with incident date
    df["timeline.incident.date"] = pd.to_datetime(
        df.rename(columns={
            "timeline.incident.year": "year", 
            "timeline.incident.month": "month", 
            "timeline.incident.day": "day"}
            )
            [["year", "month", "day"]], errors="coerce")
    
    # Add columns for milestones dates 
    stages = ["discovery", "compromise", "exfiltration", "containment" ]
    for stage in stages:
        df[f"timeline.{stage}.date"] = df.apply(add_units_dates, args=(stage,), axis=1)
    
    # Add column for Action
    action_names = [x for x in list(df) if x.startswith("action.") and len(x.split(".")) == 2]
    df["Actions"] = df.apply(concatenate_actions, args=(action_names,), axis=1)
    
    # Add column for Vector
    vector_names = [x for x in list(df) if (".vector.") in x  and len(x.split(".")) == 4]
    df["Vectors"] = df.apply(concatenate_vectors, args=(vector_names,), axis=1)
    
    # Add column for Countries
    country_names = [x for x in list(df) if x.startswith("victim.country")]
    df["Countries"] = df.apply(concatenate_actions, args=(country_names,), axis=1)
    
    return df