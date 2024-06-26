#!/usr/bin/env python

def remove_invalid_tag_name_characters(tag_name):
    from tag_generator.base.constants import TAG_NAME_PATTERN
    return TAG_NAME_PATTERN.sub('', tag_name)

def get_tag_builder():
    from tag_generator.base.constants import TAG_BUILDER_TEMPLATE
    return TAG_BUILDER_TEMPLATE.copy()

def reset_tag_builder(tag_builder= {}) -> None:
    from tag_generator.base.constants import TAG_BUILDER_TEMPLATE
    tag_builder.update(TAG_BUILDER_TEMPLATE)
    
def find_row_by_tag_name(df, tag_name):
    row = df[df[r'Tag Name'] == tag_name]
    return row.iloc[0] if not row.empty else None


def extract_kepware_tag_name(opc_item_path):
    if '.' not in opc_item_path:
        return opc_item_path
    return opc_item_path.split('.', 2)[-1]

def extract_area_and_offset(address):
    from tag_generator.base.constants import ADDRESS_PATTERN
    match = ADDRESS_PATTERN.search(address)
    if match:
        first_number_index = match.start()
        area = address[:first_number_index]
        if 'X' in address:
            offset = str(int(address[first_number_index:].lstrip('0') or '0', 16))
        else:
            offset = address[first_number_index:].lstrip('0') or '0'
        return area, offset
    else :
        exit(f"Could not find any numbers in address {address}")

def get_offset_and_array_size(offset):
    array_size = ''
    if '.' in offset:
        array_size = offset.split('.')[1]
        array_size = array_size.lstrip('0')
        offset = offset.split('.')[0]

    return (offset, array_size)

# def set_missing_tag_properties(tags, new_tag) -> None:
#     from tag_generator.base.constants import REQUIRED_KEYS
#     required_keys = REQUIRED_KEYS.copy()

#     def handle_missing_tags(dummy_tag, new_tag):
#         if required_keys == []:
#             return True
#         if r'tags' in dummy_tag:
#             handle_missing_tags(dummy_tag[r'tags'], new_tag)
#         else:
#             remove = required_keys.remove
#             for key in required_keys:
#                 if (key not in new_tag) and (key in dummy_tag) and (dummy_tag[key] != r'Folder'):
#                     new_tag[key] = dummy_tag[key]
#                     remove(key)

#     for dummy_tag in tags:
#         if handle_missing_tags(dummy_tag, new_tag):
#             break


# def build_tag_hierarchy(tags, name_parts):
#     dummy_tags = tags
#     for part in name_parts[:-1]:
#         found = False
#         for tag in dummy_tags:
#             if tag[r'name'] == part:
#                 dummy_tags = tag[r'tags']
#                 found = True
#                 break
#         if not found:
#             new_folder_tag = {
#                 r"name": part,
#                 r"tagType": r"Folder",
#                 r"tags": []
#             }
#             dummy_tags.append(new_folder_tag)
#             dummy_tags = new_folder_tag['tags']
#     return dummy_tags