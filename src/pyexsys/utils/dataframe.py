from pandas import DataFrame


def select_columns(df: DataFrame, columns: list) -> DataFrame:
    if len(columns) == 0:
        return df
    non_exist_columns = [col for col in columns if col not in df.columns]
    if len(non_exist_columns) > 0:
        raise Exception(f"columns {non_exist_columns} not exist")

    return df[columns]
