import json

def json_load(filename):
    """Load data from a JSON file and return it."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file {filename}.")
        return None

def json_save(filename, data):
    """Save data to a JSON file."""
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error: Failed to save data to {filename}. Reason: {e}")
