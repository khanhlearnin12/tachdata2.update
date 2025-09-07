import pandas as pd

def replace_na_with_blank(input_path):
    """
    Replaces all 'NA' values (case-insensitive) in an Excel file with blank strings.

    Args:
        excel_file_path (str): The path to the input Excel file.
        sheet_name (int or str, optional): The sheet to read. 0 for the first sheet,
                                          or the name of the sheet. Defaults to 0.
        output_file_path (str, optional): The path to save the modified Excel file.
                                          If None, the original file is overwritten.
                                          Defaults to None.
    """
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(input_path)

        # Replace 'NA' (and 'na', 'Na', 'nA') with an empty string
        # .astype(str) ensures all elements are strings before applying .str.replace()
        # This prevents errors if there are non-string data types in the DataFrame.
        df = df.apply(lambda x: x.astype(str).str.replace('n', ' ', case=False))

        # Determine the output file path
        if output_file_path is None:
            import os
            base = os.path.basename(input_path)
            name, ext = os.path.splitext(base)
            output_file_path = f"{name}_output{ext}"

        # Save the modified DataFrame back to an Excel file
        df.to_excel(output_file_path, index=False) # index=False prevents writing DataFrame index as a column
        print(f"Successfully replaced 'NA' with blanks in '{input_path}' and saved to '{output_file_path}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

        return df

        

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python replaceNA.py <excel_file_path>")
    else:
        replace_na_with_blank(sys.argv[1])

# --- How to Use ---
# Example 1: Replace in 'my_data.xlsx' and overwrite the original file
# replace_na_with_blank('my_data.xlsx')

# Example 2: Replace in 'input.xlsx' (sheet named 'Sheet1') and save to 'output.xlsx'
# replace_na_with_blank('input.xlsx', sheet_name='Sheet1', output_file_path='output.xlsx')

# Example 3: Replace in 'another_file.xlsx' (first sheet) and save to 'another_file_modified.xlsx'
# replace_na_with_blank('another_file.xlsx', output_file_path='another_file_modified.xlsx')~
