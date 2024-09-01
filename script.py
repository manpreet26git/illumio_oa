import socket
import csv
import argparse
from pathlib import Path
import sys

def get_args() -> argparse.Namespace:
    """Get the values for the commandline arguments"""
    parser = argparse.ArgumentParser(
        description="Parse Logs"
    )
    
    parser.add_argument('--logs_file_path', metavar='PATH',
                        help='Path to plain text log file',
                        type=Path, default=None, required=True)
    
    parser.add_argument('--tags_file_path', metavar='PATH',
                        help='Path to plain text tag file',
                        type=Path, default=None, required=True)
    
    return parser.parse_args()

def get_prot_name_from_prot_num(prot_num, prot_num_to_name):
    """
        returns protocol name corresponding to a number if the protocol name exists in tags file 
        else returns empty string
    """
    return prot_num_to_name.get(prot_num, "")

def get_tag(dst_port, prot_num, dst_port_prot_num_to_tag):
    return dst_port_prot_num_to_tag.get((dst_port, prot_num), "")

def main():
    args = get_args()

    file_paths = args
    if not file_paths:
        print('Please specify log file path and tags file path')
        sys.exit(0)

    logs_file_name = file_paths.logs_file_path
    tags_file_name = file_paths.tags_file_path


    # outputs required
    # tag to count
    tag_to_count: dict[str, int] = {}
    # dst port and protocol to count
    dst_port_prot_to_count: dict[tuple, int] = {}

    # parsing csv file containg tags 
    # check for whitespaces, parse only 3 in one line
    dst_port_prot_num_to_tag:dict[tuple, str] = {}
    prot_num_to_name:dict[str, int] = {}
    tags:set[str] = set()
    try: 
        with open(tags_file_name, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
            for row in csvreader:
                # preprocessing data
                if len(row) >= 3:
                    dst_port = int(row[0])
                    prot_name = row[1].lower()
                    try:
                        prot_num = socket.getprotobyname(prot_name)
                        tag = row[2].lower()
                        prot_num_to_name.update({prot_num : prot_name})
                        dst_port_prot_num_to_tag.update({(dst_port, prot_num) : tag})
                        dst_port_prot_to_count.update({(dst_port, prot_name) : 0})
                        tags.add(tag)
                    except:
                        print("invalid protocol name")
    except Exception as e:
        print(e)
        sys.exit(0)


    # parsing log file 
    # assumption that each record is a string with fields separated by spaces.
    # need the dest port which is col 6 need protocol number which is col 7 when zero indexed
    try: 
        with open(logs_file_name, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=' ', skipinitialspace=True)
            for log in csvreader:
                if len(log) >= 8:
                    dst_port = int(log[6]) 
                    prot_num = int(log[7])
                    # tag to count
                    tag = get_tag(dst_port, prot_num, dst_port_prot_num_to_tag)
                    if tag != "":
                        tag_to_count.update({tag: tag_to_count.get(tag, 0) + 1})
                    else:
                        tag_to_count.update({"Untagged": tag_to_count.get("Untagged", 0) + 1})
                    # dst port and protocol name to count
                    
                    if (dst_port, prot_num) in dst_port_prot_num_to_tag.keys():
                        prot_name = get_prot_name_from_prot_num(prot_num, prot_num_to_name) 
                        dst_port_prot_to_count.update({(dst_port, prot_name) : dst_port_prot_to_count.get((dst_port, prot_name), 0) + 1})
    except Exception as e:
        print(e)
        sys.exit(0)       


    print("Tag Counts:")
    print("Tag, Count")
    for tag in tags:
        if tag in tag_to_count.keys():
            print(tag, tag_to_count[tag])
        else:
            print(tag, 0)
    if "Untagged" in tag_to_count.keys():
            print("Untagged", tag_to_count["Untagged"])

    print("")
    print("Port/Protocol Combination Counts:")
    print("Port,Protocol,Count") 
    for tuple_dst_port_prot, count in dst_port_prot_to_count.items():
        print(tuple_dst_port_prot[0], tuple_dst_port_prot[1], count)


if __name__ == "__main__":
    '''
        Supply command line arguments in this form: --logs_file_path path_to_logs_file --tags_file_path path_to_tags_file
    '''
    main()