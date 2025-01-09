import csv

def reverse(response):
    return 6 - int(response)

def mean(responses):
    valid_responses = [int(r) for r in responses if r]
    return sum(valid_responses) / len(valid_responses) if valid_responses else None

def scores(csv_file):
    contaInvalid = 0
    scores_result = {}

    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames[1:]  # Ignorar a primeira coluna (nome do teste)

        for row in reader:
            test_name = row['teste']
            responses = {int(q): int(row[q]) if row[q].isdigit() else 3 for q in header}

            # Calcular as médias para cada domínio:
            # EXTRAVERSION
            BFI2_E_Sociability = mean([responses[1], reverse(responses[16]),
                                       reverse(responses[31]), responses[46]])
            BFI2_E_Assertiveness = mean([responses[6], responses[21], 
                                         reverse(responses[36]), reverse(responses[51])])
            BFI2_E_EnergyLevel = mean([reverse(responses[11]), reverse(responses[26]),
                                       responses[41], responses[56]])
            BFI2_E = mean([BFI2_E_Sociability, BFI2_E_Assertiveness, BFI2_E_EnergyLevel])

            # AGREEABLENESS
            BFI2_A_Compassion = mean([responses[2], reverse(responses[17]),
                                      responses[32], reverse(responses[47])])
            BFI2_A_Respectfulness = mean([responses[7], reverse(responses[22]),
                                          reverse(responses[37]), responses[52]])
            BFI2_A_Trust = mean([reverse(responses[12]), responses[27],
                                 reverse(responses[42]), responses[57]])
            BFI2_A = mean([BFI2_A_Compassion, BFI2_A_Respectfulness, BFI2_A_Trust])

            # CONSCIENTIOUSNESS
            BFI2_C_Organization = mean([reverse(responses[3]), responses[18],
                                        responses[33], reverse(responses[48])])
            BFI2_C_Productiveness = mean([reverse(responses[8]), reverse(responses[23]),
                                          responses[38], responses[53]])
            BFI2_C_Responsibility = mean([responses[13], reverse(responses[28]),
                                          responses[43], reverse(responses[58])])
            BFI2_C = mean([BFI2_C_Organization, BFI2_C_Productiveness, BFI2_C_Responsibility])

            # NEUROTICISM
            BFI2_N_Anxiety = mean([reverse(responses[4]), responses[19], 
                                   responses[34], reverse(responses[49])])
            BFI2_N_Depression = mean([reverse(responses[9]), reverse(responses[24]),
                                      responses[39], responses[54]])
            BFI2_N_EmotionalVolatility = mean([responses[14], reverse(responses[29]),
                                               reverse(responses[44]), responses[59]])
            BFI2_N = mean([BFI2_N_Anxiety, BFI2_N_Depression, BFI2_N_EmotionalVolatility])

            # OPENNESS
            BFI2_O_IntellectualCuriosity = mean([responses[10], reverse(responses[25]),
                                                 responses[40], reverse(responses[55])])
            BFI2_O_AestheticSensitivity = mean([reverse(responses[5]), responses[20],
                                                responses[35], reverse(responses[50])])
            BFI2_O_CreativeImagination = mean([responses[15], reverse(responses[30]),
                                               reverse(responses[45]), responses[60]])
            BFI2_O = mean([BFI2_O_IntellectualCuriosity, BFI2_O_AestheticSensitivity, BFI2_O_CreativeImagination])

            # Salvar os resultados para o teste atual
            scores_result[test_name] = {
                'BFI2_Extraversion': BFI2_E,
                'BFI2_Agreeableness': BFI2_A,
                'BFI2_Conscientiousness': BFI2_C,
                'BFI2_Neuroticism': BFI2_N,
                'BFI2_Openness': BFI2_O,
            }

    return scores_result

# Testar com o arquivo carregado
file_path = 'sorted_combined_testPsycho_scores.csv' 
domain_scores = scores(file_path)

# Exibir os resultados
for test, scores in domain_scores.items():
    print(f"Scores para {test}:")
    for domain, score in scores.items():
        print(f"  {domain}: {score}")

