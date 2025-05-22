import json

# Function to invert responses (1 becomes 5, 2 becomes 4, etc.)
def invert_response(response):
    return 6 - int(response)

# Function to compute the mean of the responses
def compute_mean(responses):
    valid_responses = [int(r) for r in responses if r]
    return sum(valid_responses) / len(valid_responses) if valid_responses else None

# Function to collect user responses
def collect_user_responses(bfi_items):
    responses = {}
    
    print("Please answer the following questions using a scale from 1 to 5:")
    print("1: Strongly Disagree")
    print("2: Disagree a little")
    print("3: Neutral")
    print("4: Agree a little")
    print("5: Strongly Agree\n")
    
    # Iterate through the BFI-2 items
    for item in bfi_items:
        while True:
            try:
                response = int(input(f"{item['id']}. I am someone who {item['statement']} (1-5): "))
                if response < 1 or response > 5:
                    raise ValueError
                responses[item['id']] = response
                break
            except ValueError:
                print("Invalid response. Please enter a number between 1 and 5.")
    
    return responses

# Function to calculate domain scores
def calculate_domain_scores(responses):
    # Compute means for each domain
    BFI2_E_Sociability = compute_mean([responses[1], invert_response(responses[16]),
                                       invert_response(responses[31]), responses[46]])
    BFI2_E_Assertiveness = compute_mean([responses[6], responses[21], 
                                         invert_response(responses[36]), invert_response(responses[51])])
    BFI2_E_EnergyLevel = compute_mean([invert_response(responses[11]), invert_response(responses[26]),
                                       responses[41], responses[56]])
    BFI2_E = compute_mean([BFI2_E_Sociability, BFI2_E_Assertiveness, BFI2_E_EnergyLevel])

    BFI2_A_Compassion = compute_mean([responses[2], invert_response(responses[17]),
                                      responses[32], invert_response(responses[47])])
    BFI2_A_Respectfulness = compute_mean([responses[7], invert_response(responses[22]),
                                          invert_response(responses[37]), responses[52]])
    BFI2_A_Trust = compute_mean([invert_response(responses[12]), responses[27],
                                 invert_response(responses[42]), responses[57]])
    BFI2_A = compute_mean([BFI2_A_Compassion, BFI2_A_Respectfulness, BFI2_A_Trust])

    BFI2_C_Organization = compute_mean([invert_response(responses[3]), responses[18],
                                        responses[33], invert_response(responses[48])])
    BFI2_C_Productiveness = compute_mean([invert_response(responses[8]), invert_response(responses[23]),
                                          responses[38], responses[53]])
    BFI2_C_Responsibility = compute_mean([responses[13], invert_response(responses[28]),
                                          responses[43], responses[58]])
    BFI2_C = compute_mean([BFI2_C_Organization, BFI2_C_Productiveness, BFI2_C_Responsibility])

    BFI2_N_Anxiety = compute_mean([invert_response(responses[4]), responses[19], 
                                   responses[34], invert_response(responses[49])])
    BFI2_N_Depression = compute_mean([invert_response(responses[9]), invert_response(responses[24]),
                                      responses[39], responses[54]])
    BFI2_N_EmotionalVolatility = compute_mean([responses[14], invert_response(responses[29]),
                                               invert_response(responses[44]), responses[59]])
    BFI2_N = compute_mean([BFI2_N_Anxiety, BFI2_N_Depression, BFI2_N_EmotionalVolatility])

    BFI2_O_IntellectualCuriosity = compute_mean([responses[10], invert_response(responses[25]),
                                                 responses[40], responses[55]])
    BFI2_O_AestheticSensitivity = compute_mean([invert_response(responses[5]), responses[20],
                                                responses[35], invert_response(responses[50])])
    BFI2_O_CreativeImagination = compute_mean([responses[15], invert_response(responses[30]),
                                               invert_response(responses[45]), responses[60]])
    BFI2_O = compute_mean([BFI2_O_IntellectualCuriosity, BFI2_O_AestheticSensitivity, BFI2_O_CreativeImagination])

    return {
        'BFI2_E': BFI2_E,
        'BFI2_A': BFI2_A,
        'BFI2_C': BFI2_C,
        'BFI2_N': BFI2_N,
        'BFI2_O': BFI2_O
    }

# Function to load the BFI-2 items from a JSON file
def load_bfi_items_from_json(json_file):
    with open(json_file, "r") as f:
        bfi_data = json.load(f)
    return bfi_data["BFI-2"]["items"]

# Path to the JSON file containing BFI-2 items
json_file = "bfi2facets.json"

# Load BFI-2 items from the JSON file
bfi_items = load_bfi_items_from_json(json_file)

# Collect user responses
responses = collect_user_responses(bfi_items)

# Calculate domain scores
domain_scores = calculate_domain_scores(responses)

# Display the results
print("\nDomain scores:")
for domain, score in domain_scores.items():
    print(f"{domain}: {score}")

