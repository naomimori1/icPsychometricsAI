import json

def create_bfi2_json(input_txt_file, output_json_file, reversed_ids):
    """
    This function reads BFI-2 items from a text file and creates a JSON structure.

    Parameters:
    - input_txt_file: The path to the text file containing BFI-2 items.
    - output_json_file: The path to save the JSON file.
    - reversed_ids: A set or list of ids where the score is reversed.

    """
    bfi_data = {"BFI-2": {"items": []}}

    # Open the input file and read each line (item)
    with open(input_txt_file, 'r') as file:
        for idx, line in enumerate(file, start=1):  # Line number starts from 1
            item_text = line.strip()  # Remove any trailing newlines or spaces

            # Create the item dictionary
            item = {
                "id": idx,
                "statement": item_text,
                "reversed": idx in reversed_ids  # Check if the id is in the reversed list
            }

            # Append the item to the list
            bfi_data["BFI-2"]["items"].append(item)

    # Write the data to the output JSON file
    with open(output_json_file, 'w') as json_file:
        json.dump(bfi_data, json_file, indent=4)

    print(f"BFI-2 data successfully written to {output_json_file}")

# Example usage
input_txt_file = 'items.txt'  # Path to your text file with items
output_json_file = 'bfi2.json'  # Path where you want to save the JSON
reversed_ids = [3, 4, 5, 8, 9, 11, 12, 16, 17, 22, 23, 24, 25, 26, 28, 29, 30, 31, 36, 37, 42, 44, 45, 47, 48, 49, 50, 51, 55, 58]# Example: Set of item ids that are reverse-scored

create_bfi2_json(input_txt_file, output_json_file, reversed_ids)

def add_facets_to_bfi2_json(input_json_file, output_json_file, facet_to_items):
    """
    This function adds facet information to the BFI-2 items in a JSON file.

    Parameters:
    - input_json_file: Path to the existing JSON file with BFI-2 items.
    - output_json_file: Path to save the updated JSON file.
    - facet_to_items: A dictionary where the key is the facet name and the value is a list of item IDs.
    """

    # Load the existing JSON data
    with open(input_json_file, 'r') as json_file:
        bfi_data = json.load(json_file)

    # Loop through the items and add the corresponding facet
    for item in bfi_data["BFI-2"]["items"]:
        # Find which facet this item's ID belongs to
        for facet, items in facet_to_items.items():
            if item["id"] in items:
                item["facet"] = facet
                break  # Once we find the facet, no need to continue checking

    # Save the updated JSON data
    with open(output_json_file, 'w') as json_file:
        json.dump(bfi_data, json_file, indent=4)

    print(f"Facets successfully added and saved to {output_json_file}")


# Example usage
input_json_file = 'bfi2.json'  # Path to the existing JSON file
output_json_file = 'bfi2facets.json'  # Path to save the updated JSON file

# Example facet-to-items mapping (you would replace these with the actual mappings)
facet_to_items = {
    "Sociability": [1, 16, 31, 46],
    "Assertiveness":[6, 21, 36, 51],
    "Energy level": [11, 26, 41, 56],
    "Compassion": [2, 17, 32, 47],
    "Respectfulness": [7, 22, 37, 52],
    "Trust": [12, 27, 42, 57],
    "Organization": [3, 18, 33, 48],
    "Productiveness": [8, 23, 38, 53],
    "Responsibility": [13, 28, 43, 58],
    "Anxiety": [4, 19, 34, 49],
    "Depression":[9, 24, 39, 54],
    "Emotional Volatility": [14, 29, 44, 59],
    "Intellectual_curiosity":[10, 25, 40, 55],
    "Aesthetic_Sensitivity": [5, 20, 35, 50],
    "Creative Imagination": [15, 30, 45, 60]
}

# Add the facets to the BFI-2 JSON
add_facets_to_bfi2_json(input_json_file, output_json_file, facet_to_items)
