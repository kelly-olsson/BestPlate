from io import StringIO
from typing import Any

import pandas as pd


import pandas as pd
from io import StringIO


def md_to_df(data: Any) -> pd.DataFrame:
    # Convert markdown to DataFrame
    if isinstance(data, str):
        lines = data.strip().split("\n")
        header_line = lines[0]
        header = [x.strip().capitalize() for x in header_line.split("|")]

        # Process the data lines, ensuring they have the same number of fields as headers
        data_lines = [x.strip() for x in lines[2:-1]]
        data_lines = [line.split("|")[:len(header)] for line in data_lines]

        # Create a DataFrame with extracted header and data
        df = pd.DataFrame(data_lines, columns=header)

        # Remove columns that have empty headers or entirely empty values
        df = df.loc[:, ~df.columns.str.isspace() & (df.columns != '')]
        df = df.dropna(axis=1, how='all')

        return df

    return data
