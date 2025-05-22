import csv
import json
import sys

# Load the JSON file
with open("bfi2facets.json", "r", encoding="utf-8") as json_file:
    bfi_data = json.load(json_file)

# Extract item details
items = {item["id"]: item for item in bfi_data["BFI-2"]["items"]}

def extract_scores(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    scores = {}
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():  # Check if the line starts with a digit
            parts = line.split("-")  # Split by the hyphen to separate the score
            if len(parts) == 2:
                item_info = parts[0].strip()
                score = parts[1].strip()
                # Extract the item number from the start of the line
                item_number = item_info.split(".")[0].strip()
                if item_number.isdigit() and score.isdigit():
                    scores[int(item_number)] = int(score)

    return scores

# File containing the responses
input_file = sys.argv[1]

# Extract scores
scores = extract_scores(input_file)

# Combine scores with item details
output_data = [
    {
        "id": item_id,
        "statement": items[item_id]["statement"],
        "facet": items[item_id]["facet"],
        "reversed": items[item_id]["reversed"],
        "score": scores[item_id]
    }
    for item_id in sorted(scores.keys())
]

# Save to a CSV file
output_file = "output.csv"
with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["id", "statement", "facet", "reversed", "score"])
    writer.writeheader()
    writer.writerows(output_data)

print(f"Results saved to {output_file}")

input_csv = "output.csv"
updated_csv = "updated_output.csv"

# Rename 'score' to 'response'
with open(input_csv, "r", encoding="utf-8") as infile, open(updated_csv, "w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = [name if name != "score" else "response" for name in reader.fieldnames]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        row["response"] = row.pop("score")
        writer.writerow(row)

print(f"Updated file saved to {updated_csv}")

