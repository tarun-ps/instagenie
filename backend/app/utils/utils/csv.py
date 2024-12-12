import pandas as pd


def eliminate_unimportant_columns(input_file_path: str, output_file_path: str, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(input_file_path)
    for column in columns:
        if column not in df.columns:
            df.to_csv(output_file_path, index=False)
            return
    df = df[columns]
    df.to_csv(output_file_path, index=False)
    return
