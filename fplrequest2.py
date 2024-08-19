import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch FPL data: {e}")
        raise

def save_data_to_json(data, file_path='fpl_data.json'):
    try:
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
        logging.info(f"Full FPL data has been saved to {file_path}")
    except IOError as e:
        logging.error(f"Failed to save FPL data to JSON file: {e}")

def explore_data(data):
    logging.info("Exploring FPL data...")
    
    # Print top-level keys
    logging.info(f"Top-level keys: {list(data.keys())}\n")
    
    # Print some details from each top-level key
    for key in data:
        logging.info(f"Key: {key}, Type: {type(data[key])}, Number of Items: {len(data[key]) if isinstance(data[key], list) else 'N/A'}")
        if isinstance(data[key], list) and len(data[key]) > 0:
            logging.info(f"First item under {key}: {json.dumps(data[key][0], indent=2)}\n")
        else:
            logging.info(f"Value under {key}: {json.dumps(data[key], indent=2)}\n")

# Example usage
if __name__ == "__main__":
    try:
        # Fetch the data
        data = fetch_fpl_data()
        
        # Save the full data to a JSON file
        save_data_to_json(data)
        
        # Explore the data
        explore_data(data)
    except Exception as e:
        logging.error(f"An error occurred: {e}")