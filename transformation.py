import json
import pandas as pd
from pathlib import Path
from helper import add_units_dates, concatenate_column_names


def get_transformed_dataset():
    dtypes = json.loads(Path("data/dtypes.json").read_text())
    df = pd.read_csv("data/vcdb.csv", dtype=dtypes)
    
    # Remove columns with only empty values
    df.dropna(axis="columns", how="all", inplace=True)
    
    # Filter old incidents
    since = 2013
    until = 2022
    df.drop(df.loc[df["timeline.incident.year"] < since].index, inplace=True)
    df.drop(df.loc[df["timeline.incident.year"] > until].index, inplace=True)
    
    # Filter not confirmed incidents
    df.drop(df.loc[df["security_incident.Confirmed"] == False].index, inplace=True)
    
    # Filter only incidents where a data disclosure was confirmed
    df.drop(df.loc[df["attribute.confidentiality.data_disclosure.Yes"] == False].index, inplace=True)

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
    df["Actions"] = df.apply(concatenate_column_names, args=(action_names,), axis=1)
    
    # Add column for Vector
    vector_names = [x for x in list(df) if (".vector.") in x  and len(x.split(".")) == 4]
    df["Vectors"] = df.apply(concatenate_column_names, args=(vector_names,), axis=1)
    
    # Add column for Countries
    country_names = [x for x in list(df) if x.startswith("victim.country")]
    df["Countries"] = df.apply(concatenate_column_names, args=(country_names,), axis=1)
    
    # Add column Hacking Variety
    hvariety_names = [x for x in list(df) if x.startswith("action.hacking.variety.")]
    df["action.hacking.Variety"] = df.apply(concatenate_column_names, args=(hvariety_names,), axis=1)
    
    # Add column Hacking Variety
    mvariety_names = [x for x in list(df) if x.startswith("action.malware.variety.")]
    df["action.malware.Variety"] = df.apply(concatenate_column_names, args=(mvariety_names,), axis=1)
    return df