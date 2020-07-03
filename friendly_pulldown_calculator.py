#!/usr/bin/python

# compatible with lower version python

# adding user input to dictionaries
# specify inputs of pulldowns here (bait/pray protein names, concentrations, and molecular weights):

# dictionary of lists: [bait_protein_names, pray_protein_names],
# for nth pull down, add element n to the dictionary:[bait , pray]
proteins = {}
# dictionary of bait_protein_names : molecular weight in Da
bait_weights = {}
# dictionary of bait_protein_names : molecular concentration in mg/ml
bait_concentrations = {}
# dictionary of pray_protein_names : molecular weight in Da
pray_weights = {}
# dictionary of pray_protein_names : molecular concentration in mg/ml
pray_concentrations = {}

n = input("How many pulldowns ?")
pulldown_inputs_open = True
while pulldown_inputs_open:
    for i in range(int(n)):
        protein_info = []
        protein_info.append(input(str(i+1)+'th bait protein name? '))
        protein_info.append(input(str(i+1)+'th pray protein name? '))
        proteins[i] = protein_info
    for j, pair in proteins.items():
        bait_weights[pair[0]]=float(input('the molecular weight of '+ proteins[j][0] + ' in Da? '))
        bait_concentrations[pair[0]]=float(input('the concentration of '+ proteins[j][0] + ' in mg/ml? '))
        pray_weights[pair[1]]=float(input('the molecular weight of '+ proteins[j][1] + ' in Da? '))
        pray_concentrations[pair[1]]=float(input('the concentration of '+ proteins[j][1] + ' in mg/ml? '))
    pulldown_inputs_open = False

print('\nverify inputs: ')
print(proteins, bait_weights, bait_concentrations, pray_weights, pray_concentrations, sep='\n')
print('\n')

# default values of pulldowns, can be customized if needed:
mol_excess = 5
input_vol = 200  # uL
input_concentration = 0.0833  # unit: mg/ml
bait_amount = 50  # unit: ug
SDS = 40  # uL
DTT_input = 3  # uL
DTT_pulldown = 3  # uL
pulldown_vol = 500  # uL
slurry_vol = 60  # uL


# function: drop duplicate elements in a dictionary
def dict_drop_dup(dict):
    new_dict = {}
    for key,value in dict.items():
        if key not in new_dict.keys():
            new_dict[key] = value
    return new_dict


bait_input = {}
pray_input = {}
for n, pairs in proteins.items():
    bait_input[pairs[0]] = round(input_vol * input_concentration / bait_concentrations[pairs[0]], 2)
    pray_input[pairs[1]] = round(input_vol * input_concentration / pray_concentrations[pairs[1]], 2)

    # 0-bait, 1-pray, 2-bait_mol, 3-pray_mol, 4-pray_amount, 5-bait_vol, 6-pray_vol
    proteins[n].append(50 / bait_weights[pairs[0]])  # 2-bait_mol
    proteins[n].append(mol_excess * proteins[n][2])  # 3-pray_mol
    proteins[n].append(proteins[n][3] * pray_weights[pairs[1]])  # 4-pray_amount
    proteins[n].append(round(bait_amount / bait_concentrations[pairs[0]], 2))  # 5-bait_vol
    proteins[n].append(round(proteins[n][4] / pray_concentrations[pairs[1]], 2))  # 6-pray_vol

# inputs = {**dict_drop_dup(bait_input), **dict_drop_dup(pray_input)}
bait_inputs = dict_drop_dup(bait_input)
pray_inputs = dict_drop_dup(pray_input)
inputs = bait_inputs.copy()
inputs.update(pray_inputs)

# print outputs
print('the input samples:')
print('protein_name', 'protein', 'SDS_buffer', 'DTT', 'buffer', sep='\t'.expandtabs(5))
for protein, vol in inputs.items():
    buffer = input_vol - DTT_input - SDS - vol
    print(protein, vol, SDS, DTT_input, buffer, sep='\t'.expandtabs(10))
print('\n')

# 0-bait, 1-pray, 2-bait_mol, 3-pray_mol, 4-pray_amount, 5-bait_vol, 6-pray_vol
print('the pulldown samples:')
print('bait_name', 'bait', 'pray_name', 'pray', 'slurry', 'DTT', 'buffer', sep='\t'.expandtabs(5))
for n, pairs in proteins.items():
    buffer = round(pulldown_vol - proteins[n][5] - proteins[n][6] - slurry_vol - DTT_pulldown, 2)
    print(pairs[0], proteins[n][5], pairs[1], proteins[n][6], slurry_vol, DTT_pulldown, buffer, sep='\t'.expandtabs(7))
