from io import StringIO
from typing import Any

import pandas as pd


import pandas as pd
from io import StringIO


def md_to_df(data: Any) -> pd.DataFrame:
    # Convert markdown to DataFrame
    if isinstance(data, str):
        lines = data.split("\n")
        header = [x.strip() for x in lines[0].split("|")]
        for head in header:
            print(head)
        data_lines = [x.strip() for x in lines[2:-1]]

        # Ensure the number of fields in the header and data lines match
        num_header_fields = len(header)
        data_lines = [line.split("|")[:num_header_fields] for line in data_lines]

        df = pd.DataFrame(data_lines, columns=header)
        return df

    return data
