import random


# function to generate a list of dictionaries with random keys and values
def generate_list_of_dicts():
    list_of_dicts = []
    for _ in range(random.randint(2, 10)):
        num_of_keys = random.randint(1, 5)
        new_dict = {chr(random.randint(97, 122)): random.randint(0, 100) for _ in range(num_of_keys)}
        list_of_dicts.append(new_dict)
    return list_of_dicts


# function to merge dictionaries and find maximum values for common keys
def merge_and_find_max(list_of_dicts):
    common_dict = {}
    for i, d in enumerate(list_of_dicts, 1):
        for key, value in d.items():
            if key in common_dict:
                if value > common_dict[key]:
                    common_dict[key + '_' + str(i)] = value
                    del common_dict[key]
            else:
                common_dict[key] = value
    return common_dict


# main function to orchestrate the workflow
def main():
    list_of_dicts = generate_list_of_dicts()
    print("List of dicts:", list_of_dicts)

    common_dict = merge_and_find_max(list_of_dicts)
    print("Common dict:", common_dict)


main()