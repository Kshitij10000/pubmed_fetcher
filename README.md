# PubMed Fetcher

**PubMed Fetcher** is a command-line tool designed to efficiently retrieve research papers from PubMed based on a user-defined query. It filters results to include only papers with at least one author affiliated with a pharmaceutical or biotech company and outputs the data in a convenient CSV format.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Options](#options)
- [Development Notes](#development-notes)
- [Tools and Libraries](#tools-and-libraries)
- [Contributing](#contributing)
- [License](#license)

## Features

-   **Flexible Querying:** Accepts complex PubMed queries directly from the command line.
-   **Affiliation Filtering:** Filters articles to include only those with authors affiliated with pharmaceutical or biotech companies.
-   **CSV Output:** Outputs results to a CSV file for easy data analysis or prints them to the console.
-   **Debug Mode:** Supports a debug mode for verbose output, aiding in troubleshooting.
-   **Secure Credentials:** Uses environment variables for secure management of API credentials.
-   **Cross-Platform:** Works on any system that supports Python and Poetry.

## Project Structure
Use code with caution.
Markdown
pubmed_fetcher/
├── .env # Environment variables file (not tracked by Git)
├── .gitignore # Files to ignore in Git (e.g., .env)
├── paper_fetcher/ # Core functionality module
│ ├── init.py
│ └── fetcher.py # Module containing core functionality
├── cli.py # Command-line interface script
├── pyproject.toml # Poetry project configuration
└── README.md # Project documentation

## Requirements

-   Python 3.9 or higher
-   [Poetry](https://python-poetry.org/) for dependency management

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/pubmed_fetcher.git
    cd pubmed_fetcher
    ```

2.  **Install Poetry if you haven't already:**

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3.  **Install dependencies using Poetry:**

    ```bash
    poetry install
    ```

4.  **Activate the virtual environment:**

    ```bash
    poetry shell
    ```

## Configuration

1.  **Create a `.env` file** in the root of the project to securely store your API credentials:

    ```bash
    touch .env
    ```

2.  **Add your credentials** to the `.env` file:

    ```dotenv
    EMAIL=your_email@example.com
    API_KEY=your_pubmed_api_key
    ```

3.  **Ensure `.env` is in your `.gitignore`** to prevent it from being committed to version control:

    ```bash
    echo ".env" >> .gitignore
    ```

## Usage

With the environment set up and activated, you can run the tool using Poetry's script command:

```bash
poetry run get-papers-list "your PubMed query here" [options]
Use code with caution.
Example:

poetry run get-papers-list "\"Cardiovascular Diseases\"[MeSH Terms] AND \"Prevention & control\"[Subheading]" -f results.csv
Use code with caution.
Bash
Options
-d, --debug: Enable debug mode to print detailed debug information during execution.

-f FILE, --file FILE: Specify a filename to save the results as a CSV file. If omitted, the output is printed to the console.

-h, --help: Display usage instructions.

Development Notes
Environment Security: Sensitive credentials such as EMAIL and API_KEY are stored in a .env file and loaded using the python-dotenv library. This approach keeps credentials out of the source code.

Virtual Environment: Poetry automatically creates and manages a virtual environment for your project to isolate dependencies and configuration.

Testing: Use poetry run get-papers-list --help to check that the command-line interface works as expected.

Publishing: To publish the module to TestPyPI, follow the Publishing Packages guide after ensuring all functionality is verified locally.

Tools and Libraries
Biopython: For interacting with the PubMed API.

Poetry: For dependency management, packaging, and virtual environment.

python-dotenv: For loading environment variables from a .env file.

argparse: For parsing command-line arguments.

Contributing
We welcome contributions! If you'd like to contribute to the project, please follow these steps:
Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and commit them with clear, concise messages.
Push your branch to your fork.
Submit a pull request to the main repository.

License
This project is licensed under the MIT License.