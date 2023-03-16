[![Python](https://github.com/RAHB-REALTORS-Association/constant-sync/actions/workflows/python.yml/badge.svg?branch=main)](https://github.com/RAHB-REALTORS-Association/constant-sync/actions/workflows/python.yml)

# ConstantSync

ConstantSync is a Python script designed to synchronize contacts from an SQL Server database to Constant Contact. The script retrieves contacts from the SQL Server database, compares them with the contacts in Constant Contact, and updates, adds, or removes contacts accordingly.

## Requirements

- `Python 3.9`, `Python 3.10`, or `Python 3.11`
- `pyodbc 4.0.35` package for SQL Server connection
- `requests` package for HTTP requests to Constant Contact API

## Installation

1. Clone this repository:

```
git clone https://github.com/RAHB-REALTORS-Association/constant-sync.git
```

2. Change to the `constant-sync` directory:

```
cd constant-sync
```

3. Install the required packages:

```
pip install pyodbc requests wheel
```

4. Configure your API keys, database connection settings, and other necessary settings in the `settings.py` file.

5. (Optional) If needed, update the SQL query in the `database.py` file to match your database schema.

## Usage

Run the `main.py` script to synchronize the contacts:

```
python main.py
```

The script will first authenticate with Constant Contact using the OAuth 2.0 protocol. If authorization is required, the script will prompt you to enter the callback URL with the authorization code.

Once authenticated, the script will retrieve contacts from the SQL Server database and compare them with the contacts in Constant Contact. It will then update existing contacts, add new ones, and remove any stale contacts as necessary.

## Troubleshooting

If you encounter any issues or errors while running the script, please check the following:

1. Ensure that your API keys and database connection settings in `settings.py` are correct.

2. Make sure you have the correct versions of the required packages installed (`pyodbc` and `requests`).

3. Verify that your SQL query in `database.py` is valid and returns the expected results.

If you still experience issues, please refer to the project's documentation or submit an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
