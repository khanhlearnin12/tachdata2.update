
# GEMINI.md

## Project Overview

This project is a data cleaning and processing tool with both a command-line interface (CLI) and a web interface. The tool is built using Python and the Flask framework. The primary purpose of the project is to read Excel files, perform various data cleaning operations, and save the cleaned data to new Excel files.

The core functionalities include:
*   **Deleting rows:** Removing rows from an Excel file based on blank values in specific columns.
*   **Replacing 'NA' values:** Replacing all occurrences of "NA" (case-insensitive) with blank strings.
*   **Converting text to numbers:** Converting columns to numeric types where possible.

The project is structured into two main parts:
1.  **A command-line interface (CLI):** The `main.py` script serves as the entry point for the CLI. It allows users to choose a data cleaning operation and apply it to an Excel file.
2.  **A web interface:** The `app.py` script launches a Flask web application that provides a simple UI for interacting with the data cleaning functionalities. The web interface is exposed to the internet using `ngrok`.

## Building and Running

### Dependencies

The project uses Python and several libraries, including `pandas` and `Flask`. To install the dependencies, you can use pip:

```bash
pip install pandas flask
```

### Running the Command-Line Interface

The CLI is run using the `main.py` script. You need to provide the path to the Excel file you want to process as a command-line argument.

```bash
python main.py <path_to_your_excel_file.xlsx>
```

The script will then prompt you to choose a data cleaning operation.

### Running the Web Interface

The web interface is a Flask application and can be started by running the `app.py` script.

```bash
python app.py
```

This will start a local development server at `http://localhost:5000`.

To expose the web interface to the internet, you can use the `onlinestart.sh` script, which uses `ngrok`.

```bash
./onlinestart.sh
```

## Development Conventions

*   **Code Style:** The Python code generally follows the PEP 8 style guide, although there are some minor inconsistencies.
*   **Modularity:** The data cleaning logic is separated into different modules (`Delete_row.py`, `replaceNA.py`, `texttoNum.py`), which are then used by both the CLI and the web application.
*   **Error Handling:** The `replaceNA.py` script includes basic error handling for file-not-found errors.
*   **Configuration:** The project does not use a dedicated configuration file. Configuration parameters, such as the columns to check in `Delete_row.py`, are hardcoded in the scripts.
*   **Testing:** There are no automated tests in the project.

