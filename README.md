Here's a `README.md` file that guides you through setting up and running the provided Python code in a virtual environment:

# Brand Visibility Analysis Tool

This project is designed to analyze brand names related to specific product types using OpenAI's API. The script generates prompts, extracts brand names, recommends the best brand based on context, and calculates visibility scores.

## Prerequisites

- Python 3.8 or higher
- A valid OpenAI API key

## Setup Instructions

### Step 1: Clone the Repository

First, clone this repository to your local machine.

```bash
git clone https://github.com/aidenwong812/brand-visibility-analysis-tool.git
cd brand-visibility-analysis-tool
```

### Step 2: Create a Virtual Environment

Create a virtual environment to manage dependencies for this project.

```bash
python3 -m venv env
```

Activate the virtual environment:

- On Windows:

  ```bash
  .\env\Scripts\activate
  ```

- On MacOS and Linux:

  ```bash
  source env/bin/activate
  ```

### Step 3: Install Dependencies

Once the virtual environment is activated, install the necessary dependencies listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file to store your OpenAI API key securely. Add the following line to the `.env` file:

```plaintext
OPENAI_API_KEY='your_openai_api_key_here'
```

Replace `'your_openai_api_key_here'` with your actual OpenAI API key.

Ensure you have the `python-dotenv` package installed to load environment variables from the `.env` file.

### Step 5: Run the Script

Run the main script to execute the brand name analysis tool.

```bash
python main.py
```

Follow the on-screen prompts to enter the brand name and product type you wish to analyze.

## Additional Information

This script utilizes several libraries, including `openai` and `pydantic`, to interact with OpenAI's GPT models and handle data structures efficiently.

Feel free to customize the code and expand its capabilities as needed. For any questions or issues, please reach out via the project's issue tracker.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
