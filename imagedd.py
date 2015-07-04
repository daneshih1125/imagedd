#!/usr/bin/python
import commands
import os
import sys

def get_image_partitions(image):
    if not os.path.isfile(image): 
        return None 
    FDISK_COL = 'Device                                                       Boot   Start     End Sectors  Size Id Type'
    fdisk_res = commands.getoutput("fdisk -l " + image)
    fdisk_lines = fdisk_res.split('\n')
    try:
        start_idx = fdisk_lines.index(FDISK_COL) + 1
    except:
        print "no partition"
        sys.exit(1)
    partitions = [x for x in fdisk_lines[start_idx:] if x != '' ]
    return partitions

def print_partitions(partitions):
    for idx, info in enumerate(partitions):
        print("%d " % (idx + 1) + info)
    print("input number of partition")

def cmd_dd(dd_list): 
    for dd_info in dd_list:
        item = dd_info.split()
        print(item)
        dd_name = item[0]
        dd_skip = item[1]
        dd_count = item[3]
        cmd = "dd if=%s of=%s bs=512 skip=%s count=%s" % (sys.argv[1], dd_name, dd_skip, dd_count)
        print(cmd)
        os.system(cmd)
    
def dd_partition(partitions):
    print_partitions(partitions)
    dd_no = int(raw_input('Input:'))
    cmd_dd([partitions[dd_no-1]]);

if __name__ == '__main__':
    image_partitions = get_image_partitions(sys.argv[1])
    #print_partitions(image_partitions)
    dd_partition(image_partitions)
    #print(image_partitions)
