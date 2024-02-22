import random


list_of_dicts = [] # create a variable to store dictionaries and assign an empty list to it
# generate a random number of dictionaries between 2 and 10
for _ in range(random.randint(2, 10)):
    # generate a random number of keys between 1 and 5
    num_of_keys = random.randint(1, 5)
    # create a new dictionary with random keys that are letters and random values that are numbers between 0 and 100
    # random letters for keys are made with chr() method. 97 and 122 are used because chr(97) is 'a' and chr(122) is 'z'
    # random numbers for values are made with random.randint() method
    # then repeat for length of num_of_keys using for loop
    new_dict = {chr(random.randint(97, 122)): random.randint(0, 100) for _ in range(num_of_keys)}
    # append the newly created dictionary to the list_of_dicts
    list_of_dicts.append(new_dict)
print("List of dicts:", list_of_dicts)

# create a variable to store the common dictionary
common_dict = {}
# loop through the list_of_dicts
for i, d in enumerate(list_of_dicts, 1):
    # loop through the keys of the current dictionary
    for key, value in d.items():
        # if the key is already in the common_dict, update the value
        if key in common_dict:
            # if the value is greater than the previous value, update the key with the
            # new key with the max value
            if value > common_dict[key]:
                common_dict[key + '_' + str(i)] = value  # rename common_dict key with dict number with max value
                del common_dict[key]  # remove previous key with lower value
            else:
                continue # if the value is equal to the previous value, continue
        else:
            # if the key is not in the common_dict, add the key and
            # value to the common_dict without changing the value
            common_dict[key] = value
print("Common dict:", common_dict)