import re


# need to make more robust to handl chatgpt3.5 random output on file names.
def parse_chat(chat):
    # Get all ``` blocks
    regex = r"(?:\d+\.\s)?[`#]*\s*([^`\n]+)`*\n```(.*?)```"
    matches = re.findall(regex, chat, re.DOTALL)

    files = []
    for match in matches:
        path = match[0]
        code = match[1]

        # Remove digits at the beginning of the path
        path = re.sub(r'^\d+\.', '', path)

        # Remove special characters at the beginning of the path
        path = re.sub(r'^[`#]+', '', path)

        # Remove any trailing special characters or white space
        path = re.sub(r'[`#\s]+$', '', path)

        # Remove first line of code if it's empty
        code = code.split("\n")[1:]
        code = "\n".join(code)      

        files.append((path, code))

    return files


def to_files(chat, workspace):
    workspace['all_output.txt'] = chat

    files = parse_chat(chat)
    for file_path, file_content in files:
        current_dict = workspace
        path_parts = file_path.split("/")
        
        # Go through each part of the file path
        for part in path_parts[:-1]:
            # If this part of the path is not in the current dictionary,
            # add it as a new dictionary
            if part not in current_dict:
                current_dict[part] = {}
            # Move to the dictionary for this part of the path
            current_dict = current_dict[part]
        
        # Add the file to the final dictionary
        current_dict[path_parts[-1]] = file_content



# def parse_chat(chat):# -> List[Tuple[str, str]]:
#     # Get all ``` blocks
#     #regex = r"```(.*?)```"
#     regex = r"(?:\d+\.\s)?[`#]*\s*([^`\n]+)`*\n```(.*?)```" #r"(\d+\.\s(.*?))```(.*?)```"
#     matches = re.findall(regex, chat, re.DOTALL)

#     files = []
#     count = 0
#     for match in matches:
#         #print(match)
#         #path = match.group(1).split("\n")[0]
#         path = match[0]
#         code = match[1]
        
#        # if path starts with 1. or 2. or 3. etc, remove it
#         if path[0].isdigit() and path[1] == ".":
#             path = path[2:]
#         # if path starts with #, remove it
#         if path[0] == "#":
#             path = path[1:]
#         # if path starts with ``` or ` or #, remove it
#         path = path.replace("```", "").replace("`", "").replace("#", "").strip()
        
#         code = code.split("\n")[1:]
#         code = "\n".join(code)    

#         files.append((path, code))
    
#     return files