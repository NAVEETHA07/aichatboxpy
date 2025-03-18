from apify_client import ApifyClient
import csv
import json
import pandas as pd
from apify_client._errors import ApifyApiError

# Initialize the ApifyClient with your correct API token
API_TOKEN = "apify_api_GhGN1Z6qjbWvnJjoSUAEtAF1GtN11t04TLcJ"  # Replace with your valid API token

if not API_TOKEN or "<" in API_TOKEN:  # Check if the token is provided or not
    raise ValueError("API token is missing or not set correctly. Please update the API token.")

client = ApifyClient(API_TOKEN)

# Prepare the Actor input
run_input = {
    "position": "web developer",
    "country": "US",
    "location": "San Francisco",
    "maxItems": 50,
    "parseCompanyDetails": False,
    "saveOnlyUniqueItems": True,
    "followApplyRedirects": False,
}

try:
    # Run the Actor and wait for it to finish
    print("Running the Apify actor...")
    run = client.actor("hMvNSpz3JnHgl5jkh").call(run_input=run_input)
    print("Actor finished running successfully.")

    # Initialize lists to store the results
    results = []

    # Fetch the Actor results from the run's dataset
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append(item)

    # Check if results exist
    if not results:
        print("No results were returned from the Apify actor.")
        exit(0)

    # Save results in CSV format
    csv_file = "results.csv"
    keys = results[0].keys() if results else []
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved in {csv_file}")

    # Save results in JSON format
    json_file = "results.json"
    with open(json_file, mode='w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print(f"Results saved in {json_file}")

    # Save results in Excel format
    excel_file = "results.xlsx"
    df = pd.DataFrame(results)
    df.to_excel(excel_file, index=False)

    print(f"Results saved in {excel_file}")

except ApifyApiError as e:
    print(f"Apify API error occurred: {e}")
except ValueError as ve:
    print(f"Configuration error: {ve}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")