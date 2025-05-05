import csv
import json
from collections import defaultdict

csv_file = "E:\\Downloads\\subtopics - subtopics.csv.csv"

# Read CSV file with UTF-8 encoding
with open(csv_file, mode="r", encoding="utf-8-sig") as file:
    csv_reader = csv.DictReader(file)

    # Dictionary to store grouped data by "Main Topic"
    json_data = defaultdict(lambda: {"Main Topic": "", "Subtopics": []})

    for row in csv_reader:
        main_topic = row["Main Topic"].strip()  # Extract main topic, removing extra spaces
        subtopic_data = {
            "Subtopic": row["Subtopic"].strip(),
            "Description": row["Description"].strip(),
            "Code Snippets": row["Code Snippets"].strip().split("; ") if row["Code Snippets"].strip() else None
        }

        # Initialize main topic if not already present
        if not json_data[main_topic]["Main Topic"]:
            json_data[main_topic]["Main Topic"] = main_topic

        # Append subtopic under the corresponding main topic
        json_data[main_topic]["Subtopics"].append(subtopic_data)

# Convert defaultdict to a list of dictionaries
final_json = list(json_data.values())

# Save JSON to a file
output_file = "output.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(final_json, json_file, indent=4, ensure_ascii=False)

# Print JSON output
print(json.dumps(final_json, indent=4, ensure_ascii=False))
