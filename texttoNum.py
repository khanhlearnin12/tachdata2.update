import pandas as pd

def convert_text_to_number(excel_file_path, output_file_path=None):
    # Read the Excel file
    df = pd.read_excel(excel_file_path)

    # Convert all columns to numeric where possible
    df_numeric = df.apply(pd.to_numeric, errors='ignore')

    # Output file name
    if output_file_path is None:
        import os
        base = os.path.basename(excel_file_path)
        name, ext = os.path.splitext(base)
        output_file_path = f"numeric-{name}{ext}"

    # Save the DataFrame with numeric columns
    df_numeric.to_excel(output_file_path, index=False)
    print(f"Converted text to numbers where possible. Saved to {output_file_path}")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python texttoNum.py <excel_file_path>")
#     else:
#         convert_text_to_number(sys.argv[1])
