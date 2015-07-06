#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os, sys, re, commands

dd_unit = 1

def get_image_partitions(image):
    if not os.path.isfile(image): 
        return None 
    fdisk_res = commands.getoutput("fdisk -l " + image)
    idx = fdisk_res.find("Device")

    if idx < 0:
        print "no partition"
        sys.exit(1)

    fdisk_res = fdisk_res[idx:]
    fdisk_lines = fdisk_res.split('\n')

    if (re.search("Blocks", fdisk_lines[0])):
        global dd_unit 
        dd_unit = 2

    partitions = [x for x in fdisk_lines[1:] if x != '' ]
    return partitions

def print_partitions(partitions):
    for idx, info in enumerate(partitions):
        print("%d " % (idx + 1) + info)
    print("input number of partition")

def cmd_dd(dd_list): 
    for dd_info in dd_list:
        item = dd_info.split()
        dd_name = item[0]
        dd_skip = item[1]
        dd_count = int(item[3]) * dd_unit
        cmd = "dd if=%s of=%s bs=512 skip=%s count=%d" % (sys.argv[1], dd_name, dd_skip, dd_count)
        print(cmd)
        os.system(cmd)
    
def dd_partition(partitions):
    print_partitions(partitions)
    dd_no = int(raw_input('Input:'))
    if dd_no == 0:
        cmd_dd(partitions)
    elif dd_no < len(partitions):
        cmd_dd([partitions[dd_no-1]])
    else:
        print("incorrect partition number")

if __name__ == '__main__':
    image_partitions = get_image_partitions(sys.argv[1])
    dd_partition(image_partitions)
