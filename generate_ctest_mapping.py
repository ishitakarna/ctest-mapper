import re
import json
import os
import sys

pattern = r'\[CTEST\] #### (.*?) ####'
file_pattern = r'PASS (\S+)'
test_pattern = r'✓ (.*?) \(\d+ ms\)'
directory_path = sys.argv[1]

def process_file(file, result_mapping):
    test_cases_list = []
    config_list = [] # for all test cases 
    file_name = ""
   
    with open(directory_path + file, 'r') as file:
        for line in file:
            match = re.search(pattern, line.strip())
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)
                config_list.append(data)

            file_match = re.search(file_pattern, line.strip())
            if file_match:
                file_name = file_match.group(1)

            test_cases = re.findall(test_pattern, line.strip())
            if test_cases:
                for case in test_cases:
                    test_cases_list.append(case)

    # { file_name : [ { test_case_name : config_array } ] }
    values_list = []
    for case in test_cases_list:
        mapping = {}
        mapping[case] = config_list
        values_list.append(mapping)

    test_mapping = {}
    test_mapping[file_name] = values_list
    result_mapping.append(test_mapping)

files_in_directory = os.listdir(directory_path)
files = [file for file in files_in_directory if os.path.isfile(os.path.join(directory_path, file))]

result_mapping = []
for file in files:
    process_file(file, result_mapping)

with open('result_mapping.txt', 'w+') as file:
    file.write(json.dumps(result_mapping, indent = 4))
    print("Successfully generated mappings - result_mapping.txt")