import pandas as pd

def add_units_dates(row, parameter):
    if pd.isna(row['timeline.incident.date']):
            return pd.NaT  # Return NaT if the original date is NaT
    if pd.isna(row[f'timeline.{parameter}.value']):
        return pd.NaT 
    value = int(row[f'timeline.{parameter}.value'])
    date = row['timeline.incident.date']
    try:   
        if row[f'timeline.{parameter}.unit.Seconds'] == True:
            return date + pd.DateOffset(seconds=value)
        elif row[f'timeline.{parameter}.unit.Minutes'] == True:
            return date + pd.DateOffset(minutes=value)
        elif row[f'timeline.{parameter}.unit.Hours'] == True:
            return date + pd.DateOffset(hours=value)
        elif row[f'timeline.{parameter}.unit.Days'] == True:
            return date + pd.DateOffset(days=value)
        elif row[f'timeline.{parameter}.unit.Months'] == True:
            return date + pd.DateOffset(months=value)
        elif row[f'timeline.{parameter}.unit.Years'] == True:
            return date + pd.DateOffset(years=value)
    except:
        print(row['timeline.incident.date'], row[f'timeline.{parameter}.value'])

def concatenate_column_names(row, column_names):
    names = []
    for col in column_names:
        if row[col]:
            name = col.split('.')[-1]
            if name.lower() != "unknown":
                names.append(name)
    if len(names) == 0:
        names = ["Unknown"]
    return ', '.join(names)
