# Code Analysis and Processing

This project is designed to crawl, pre-process, and analyze source code submissions from Aizu Online Judge (https://judge.u-aizu.ac.jp/onlinejudge/) system. It includes functionality for tokenizing source code, encoding tokens, and preparing data for further analysis.

## Installation and Usage

1. Clone the repository:

   ```
   git clone https://github.com/leeduyanh/tannat-data.git
   ```

2. Navigate to the project directory:

   ```
   cd tannat-data
   ```

3. Set up the `.env` file in the root directory according to the `.env.template` file.

4. Run the main processing script using the run.sh script:

   ```
   ./run.sh
   ```

   If you encounter permission issues, make the script executable:

   ```
   chmod +x run.sh
   ```

This script will:

- Create a virtual environment if it doesn't exist
- Install the required dependencies
- Activate the virtual environment
- Execute the main.py script, which fetches raw data, pre-processes it, and saves the results
- Deactivate the virtual environment after execution

Note: If you receive a warning about an outdated pip version, you can upgrade pip using the following command after the virtual environment is activated:

```
python -m pip install --upgrade pip
```

## Project Structure

- `src/`: Contains all source code for the project.
  - `main.py`: The main entry point of the application.
  - `crawl/`: Contains modules for fetching data from the online judge system.
    - `constants.py`: Defines constants used in the crawling process.
    - `fetch.py`: Implements functions to fetch data from the API.
    - `raw_data_handler.py`: Handles the processing of raw data.
    - `review_handler.py`: Manages the review data processing.
  - `preprocess/`: Contains modules for preprocessing the fetched data.
    - `filter_tokenize_encode.py`: Implements filtering, tokenization, and encoding of C code.
    - `raw_data_preprocessor.py`: Manages the overall preprocessing workflow.
    - `encoder/`: Contains the token encoding logic.
      - `CTokenEncoder.py`: Implements the encoding of C tokens.
    - `lexer/`: Contains the lexical analysis logic.
      - `CLexer.py`: Implements the lexical analysis of C code.
  - `services/`: Contains utility services.
    - `data_services.py`: Provides data processing services.
    - `json_services.py`: Handles JSON-related operations.
- `run.sh`: Script to set up the environment and run the main application.
- `data/`: Directory where all JSON output files are saved.
- `requirements.txt`: Lists all Python dependencies.
- `README.md`: This file, containing project documentation.

## Dependencies

See `requirements.txt` for a list of dependencies.

## Contributors

tannat:

- Lê Duy Anh
- Võ Nguyễn Đoan Thảo
- Nguyễn Trần Bảo Ngọc
