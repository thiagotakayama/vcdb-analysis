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

def concatenate_actions(row, base_actions):
    actions = []
    for col in base_actions:
        if row[col]:
            action_name = col.split('.')[-1]
            actions.append(action_name)
    return ', '.join(actions)

def concatenate_vectors(row, base_vectors):
    vectors = []
    for col in base_vectors:
        if row[col]:
            split = col.split('.')
            vector_name = split[-3].capitalize() + "." + split[-1]
            vectors.append(vector_name)
    return ', '.join(vectors)