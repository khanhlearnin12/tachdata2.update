import pandas as pd
import os
import sys

def delete_rows_with_blank_columns(excel_file_path, output_file_path=None):
    # Read the Excel file
    df = pd.read_excel(excel_file_path)

    # List of columns to check
    columns_to_check = ['CC_WSR95', 'FDI_PCA_WSR95', 'WUI_WSR95']

    # check if the columns is missing 
    missing = [col for col in columns_to_check if col not in df.columns]
    if missing:
        raise KeyError(f"Missing columns in the input file: {missing}")

    # Remove rows where any of the specified columns are blank or NaN
    df_cleaned = df.dropna(subset=columns_to_check)
    for col in columns_to_check:
        df_cleaned = df_cleaned[df_cleaned[col].astype(str).str.strip() != '']

    # Output file name
    if output_file_path is None:
        base = os.path.basename(excel_file_path)
        name, ext = os.path.splitext(base)
        output_file_path = f"cleaned-{name}{ext}"

    # Save the cleaned DataFrame
    df_cleaned.to_excel(output_file_path, index=False)
    print(f"Rows with blank values in {columns_to_check} deleted. Saved to {output_file_path}")

    return output_file_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Delete_row.py <excel_file_path>")
    else:
        delete_rows_with_blank_columns(sys.argv[1])
