# Simple Poetry API Testing Framework by Tymek

## System requirements
Mac/Linux with Python 3.12 installed.
### Mac:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.12
```
### Ubuntu:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.12 -y
```

## Prepare Python environment
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Run Tests
```bash
pytest
```

## How the Framework Simplifies URL Generation

In the provided `PoetryApiClient` code, the `_build_route` method automatically constructs the URL based on a list of input classes (`Author`, `Title`, `LineCount`, `PoemCount`, etc.) and an optional list of outputs. For example:

```python
response = client.call_api(
    inputs = [Title("Ozymandias", absolute=True)],
    outputs = [Output.AUTHOR, Output.TITLE, Output.LINECOUNT],
    raw_text = True
)
```

This method:

1. Collects the **input fields** (e.g., `"title"`).
2. Collects the **search terms** from the `value` property (e.g., `"Ozymandias"`), optionally appending `:abs` for absolute searches.
3. Joins them into a single route string (e.g., `"/title/Ozymandias/author,title,linecount"`).
4. Appends optional outputs or a `.text` suffix if a raw text response is requested.

This approach ensures consistency across test cases. All the tester must do is specify the inputs and expected outputs, and the library handles proper URL encoding and route construction under the hood.

## Test Cases table

| **Test Case** | **Steps** | **Expected Result** | **Validation** |
|--------------|----------|--------------------|--------------|
| **1. Retrieve poem by specific title** | 1. Instantiate `PoetryApiClient`<br>2. Call `call_api` with inputs=[Title("Ozymandias")] and the desired outputs<br>3. Send GET request | - Status code is `200`<br>- Single poem returned with correct `title`, `author`, `linecount` | - **Status Code**: check for 200<br>- **Response Body**: verify JSON matches expected poem<br>- **Headers**: `content-type` |
| **2. Negative test (absolute author)** | 1. Instantiate `PoetryApiClient`<br>2. Call `call_api` with inputs=[Author("Shakespeare", absolute=True)]<br>3. Send GET request | - JSON body contains `status=404` and `reason="Not found"` | - **Negative Testing**: confirm error message<br>- **Response Body**: check for `{"status":404,"reason":"Not found"}` |
| **3. Fetch poem by Title/Author/LineCount/PoemCount** | 1. Instantiate `PoetryApiClient`<br>2. Call `call_api` with inputs=[Title("Winter"), Author("Shakespeare"), LineCount("14"), PoemCount("1")]<br>3. Send GET request | - Status code is `200`<br>- JSON body with 1 poem having correct poem content. | - **Status Code**: check for 200<br>- **Response Body**: verify fields match expected data |
| **4. Negative test mixing PoemCount and Random** | 1. Instantiate `PoetryApiClient`<br>2. Call `call_api` with inputs=[PoemCount("2"), Random("2")]<br>3. Send GET request | - JSON body with `status="405"` and `reason` about mixing `poemcount` & `random` | - **Negative Testing**: confirm error message<br>- **Response Body**: check for `"status":404"` and message about unsupported combination. |

## Types of Validation

1. **Status Code Validation**  
   Ensures the HTTP status code is as expected (often `200` for success, even if the API sometimes returns an error in the response body).

2. **Response Body Validation**  
   Confirms the JSON (or text) content contains correct fields and values for the requested resource or correct error messages for negative tests.

3. **Response Header Validation**  
   Checks if the response headers (like `Content-Type`) align with expectations (e.g., JSON vs. plain text).

4. **JSON Schema Validation**  
   Verifies the structure of the JSON response (parses using json() method). This helps ensure the data format doesn’t break clients.

5. **Negative Testing**  
   Purposefully sends invalid, conflicting, or unexpected parameters to confirm the API returns appropriate error codes or messages.


