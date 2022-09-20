import requests
from pathlib import Path
import pandas as pd
import numpy as np


def mapping_onto(path, delimiter, column_to_search, ontology):
    df = pd.read_csv(path, delimiter=delimiter)
    file_name = Path(path).stem

    url = 'https://data.bioontology.org/annotator'
    mapping = []

    for component in df[column_to_search]:
        params = dict(
            text=component,
            ontologies={ontology},
            apikey='BIOPORTAL_API_KEY'
        )
        resp = requests.get(url=url, params=params)
        data = resp.json()

        if len(data) > 0:
            mapping.append(str(data[0]['annotatedClass']['@id']))
        else:
            mapping.append(np.nan)
    df["Automatic_mapping"] = mapping
    df.to_csv(f'{file_name}_{ontology}.csv', index=False)

