# C Code Analysis and Processing

This project is designed to crawl, preprocess, and analyze C code submissions from an online judge system. It includes functionality for tokenizing C code, encoding tokens, and preparing data for further analysis.

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```
   cd <project-directory>
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the main processing script:

```
python main.py
```

This will fetch raw data, preprocess it, and save the results.

## Project Structure

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

## Dependencies

See `requirements.txt` for a list of dependencies.

## License

[Specify your license here]
