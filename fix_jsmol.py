# re-index the image and link targets of openmopac.net

import os
import re
import difflib

# split the contents of a file based on target separators
def split_at_target(content, head, target, tail):
    content_list = []
    target_list = []

    buffer = ''
    while True:
        match_head = re.search(head, content, re.IGNORECASE)
        if match_head:
            match_tail = re.search(tail, content[match_head.end():], re.IGNORECASE)
            match_target = re.search(target, content[match_head.end():match_head.end()+match_tail.start()], re.IGNORECASE)
            if match_target:
                offset = match_head.end()+match_target.end()
                content_list.append(buffer + content[:offset])
                buffer = ''
                if content[offset] == '"':
                    offset += 1
                    match = re.search('"', content[offset:])
                    target_list.append(content[offset-1:offset+match.end()])
                elif content[offset] == "'":
                    offset += 1
                    match = re.search("'", content[offset:])
                    target_list.append(content[offset-1:offset+match.end()])
                else:
                    match = re.search(' ', content[offset:])
                    target_list.append(content[offset:offset+match.end()])
                content = content[offset+match.end():]
            else:
                buffer += content[:match_head.end()]
                content = content[match_head.end():]
                continue
        else:
            break
    content_list.append(buffer + content)
    return content_list, target_list

# convert a file system path to a unique dictionary key, assuming case insensitivity
def path_to_key(root, file):

    # replace URL space characters & flatten case
    root2 = root.replace("%20", " ").lower()
    file2 = file.replace("%20", " ").lower()

    # split based on both \ and / path delimiters
    root_list = re.split(r'[/\\]+', root2)
    file_list = re.split(r'[/\\]+', file2)

    # remove trivial path elements (.)
    while "." in file_list:
        file_list.remove(".")

    # parse nontrivial path elements (..)
    while ".." in file_list:
        index = file_list.index("..")
        if index > 0:
            del file_list[index-1]
        else:
            del root_list[-1]
        file_list.remove("..")

    return tuple(root_list + file_list)

# fix a URI fragment name from a list of fragment names: name=... in "a" HTML tag or id=... in any HTML tag
def fix_shortcut(old_shortcut, file):

    try:
        with open(file, 'r') as file_handle:
            content = file_handle.read()
    except UnicodeDecodeError:
        with open(file, 'r', encoding='latin-1') as file_handle:
            content = file_handle.read()

    # fix common typos
    content = content.replace("benzenezene","benzene") # specific, common typo

    tags = r'<.*?>'
    tag_list = re.findall(tags, content)

    shortcut_list = []
    for tag in tag_list:
        if tag[1] == '!':
            continue
        match = re.search(r' id=', tag, re.IGNORECASE)
        if tag[1:3].lower() == 'a ' and match is None:
            match = re.search(r' name=', tag, re.IGNORECASE)
        if not match is None:
            offset = match.end()
            if tag[offset] == '"':
                offset += 1
                match_shortcut = re.search('"', tag[offset:])
                shortcut_list.append(tag[offset:offset+match_shortcut.end()-1])
            elif tag[offset] == "'":
                offset += 1
                match_shortcut = re.search('"', tag[offset:])
                shortcut_list.append(tag[offset:offset+match_shortcut.end()-1])
            else:
                match_shortcut = re.search(' ', tag[offset:])
                shortcut_list.append(tag[offset:offset+match_shortcut.end()])

    shortcut_map = {}
    for shortcut in shortcut_list:
        shortcut_map[shortcut.lower()] = shortcut

    old_shortcut = old_shortcut.replace('\n','')

    if not old_shortcut.lower() in shortcut_map:
        print("ERROR: broken shortcut", old_shortcut, "in", file)
        return old_shortcut
#        print(shortcut_map)
#        exit()

    return shortcut_map[old_shortcut.lower()]

# standardize internal targets
def fix_target(root, old_target, target_dict, file):
    # special cases
    if "mailto:" in old_target or "javascript:" in old_target or "data:image" in old_target:
        return old_target

    # strip delimiter
    new_target = old_target
    if new_target[0] == '"' or new_target[0] == "'":
        new_target = new_target[1:-1]

    # check for external targets
    if not (new_target[:4].lower() == 'http' and new_target[:20].lower() != 'http://openmopac.net'):

        # separate shortcut
        has_shortcut = False
        if '#' in new_target:
            has_shortcut = True
            shortcut = new_target.split('#')[1]
            new_target = new_target.split('#')[0]
            if shortcut == '':
                has_shortcut = False

        # search for absolute target
        if new_target[:21].lower() == 'http://openmopac.net/':
            new_target = new_target[21:]
            target_key = path_to_key('httpdocs', new_target)
            if target_key in target_dict:
                new_target = target_dict[target_key]
            else:
                path = target_key[0]
                for i in range(1,len(target_key)):
                    path += '/' + target_key[i]
#                if path[-4:] == '.txt':
#                    print(f"cp stub.txt \"{os.path.join(root, old_target[1:-1])}\"")
                print(f"ERROR: invalid target from abs in {root}/{file},", path)
                return old_target
#                exit()

            # fix shortcut
            if has_shortcut:
                new_shortcut = fix_shortcut(shortcut, new_target)
                new_target += '#' + new_shortcut

            # remove httpdocs head
            new_target = new_target[8:]
        # link to homepage
        elif new_target[:20].lower() == 'http://openmopac.net':
            new_target = '/index.html'
        # in-page shortcuts
        elif has_shortcut and new_target == '':
            new_shortcut = fix_shortcut(shortcut, os.path.join(root, file))
            new_target = '#' + new_shortcut
        # search for relative target
        else:
            target_key = path_to_key(root, new_target)
            if target_key in target_dict:
                new_target = target_dict[target_key]
            else:
                path = target_key[0]
                for i in range(1,len(target_key)):
                    path += '/' + target_key[i]
#                if path[-4:] == '.txt':
#                    print(f"cp stub.txt \"{os.path.join(root, old_target[1:-1])}\"")
                print(f"ERROR: invalid target from rel in {root}/{file},", path)
                return old_target
#                exit()

            # fix shortcut
            if has_shortcut:
                new_shortcut = fix_shortcut(shortcut, new_target)
                new_target += '#' + new_shortcut

            # adjust target to remove root
            root_list = root.split('/')
            target_list = new_target.split('/')
            while len(root_list) > 0:
                if root_list[0] == target_list[0]:
                    del root_list[0]
                    del target_list[0]
                else:
                    del root_list[0]
                    target_list.insert(0,'..')

            # reassemble target
            new_target = target_list[0]
            for i in range(1,len(target_list)):
                new_target += '/' + target_list[i]

    # remove spaces
    new_target = new_target.replace(" ","%20")

    # return with standard delimiter
    return '"' + new_target + '"'

# revert the split_at_target operation
def merge_from_target(content_list, target_list):
    content = ''
    for i in range(len(target_list)):
        content += content_list[i] + target_list[i]
    content += content_list[-1]
    return content

# build a local target dictionary
target_dict = {}
for (root, dirs, files) in os.walk('httpdocs'):
    for file in files:
        file_path = os.path.join(root, file)
        file_key = path_to_key(root, file)
        target_dict[file_key] = file_path

# loop over all subdirectories of the website
for (root, dirs, files) in os.walk('httpdocs'):
    # temporary skips
    if 'httpdocs/jsmol' in root:
        continue

    # loop over all files in each subdirectory
    for file in files:
        if file[-4:].lower() == '.htm' or file[-5:].lower() == '.html':
#            print(f"HTML file: {root}/{file}")

            # read file contents
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as file_handle:
                    content = file_handle.read()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as file_handle:
                    content = file_handle.read()

            fix1 = r'jmolInitialize("java","JmolAppletSigned0.jar")'
            fix2 = r'jarPath: "../../jsmol/java",'
            find1 = r'"../../jsmol/'
            replace1 = r'"/jsmol/'
            content = content.replace(fix1,'')
            content = content.replace(fix2,'')
            content = content.replace(find1, replace1)

            # overwrite file with corrected content ...
            with open(file_path, 'w', encoding='utf-8') as file_handle:
                file_handle.write(content)
