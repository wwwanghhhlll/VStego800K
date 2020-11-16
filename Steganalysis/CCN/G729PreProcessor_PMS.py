# -*- coding: utf-8 -*-
import argparse
import os, math
from enum import Enum
import numpy as np

Feature = "FEAT"
G729A = "g729a"

FRAMESIZE_729A = 10
pitch_min = 20
pitch_max = 143
indexthre = 197


def print_info(s):
    print(s)


def print_error(s):
    print(s)


def get_file_list():
    global args
    if os.path.isfile(args.input):
        return [args.input]
    elif os.path.isdir(args.input):
        file_list = []
        for file in os.listdir(args.input):
            full_path = os.path.join(args.input, file)
            if os.path.isfile(full_path):
                file_list.append(full_path)
        return file_list
    else:
        return None


def process_file(fileName):
    def extract_frame(content):
        ####### ACW [a,b]
        if type(content) == str:
            content_t = [int(item.encode('hex'), 16) for item in content]
        else:
            content_t = content
        a = ((content_t[2] << 2) & 0xfc) | ((content_t[3] >> 6) & 0x03)
        b = content_t[6] & 0x1f

        return [a, b]

    global args

    file = open(fileName, "rb")
    content = file.read()
    file.close()

    feat = []
    num_frame = int(len(content) / FRAMESIZE_729A)

    for i in range(num_frame):
        feat.append(extract_frame(content[i * FRAMESIZE_729A: i * FRAMESIZE_729A + 7]))

    feat = np.array(feat, dtype=int)

    basename = os.path.splitext(os.path.basename(fileName))[0]
    np.savetxt(os.path.join(args.output, "%s_2_feat.txt" % (basename)), feat, fmt='%d')

if __name__ == "__main__":
    global args

    parser = argparse.ArgumentParser(description='G729A编码文件参数提取工具')
    parser.add_argument("--input", default="/data/s_test/test_negative_g", help="输入文件/文件夹", type=str)
    parser.add_argument("--output", default="/data/data_QCCN/t_negative", help="输出文件夹", type=str)
    parser.add_argument("-t", "--type", help="输出类型（G729A或FEAT，默认FEAT）", type=str, default=Feature)

    args = parser.parse_args()
    if args.type.lower() == G729A.lower():
        args.type = G729A
    elif args.type.lower() == Feature.lower():
        args.type = Feature
    else:
        print_error("输入参数type必须为G729A或FEAT")
        exit(1)

    if not os.path.isdir(args.output):
        print_error("output not exists!")
        exit(1)

    print_info("Reading files in foler...")
    file_list = get_file_list()
    if file_list == None:
        print_error("Input error！")
        exit(1)
    else:
        print_info("%d files to be processed" % len(file_list))

    print_info("Start FEAT extraction...")
    for i in range(len(file_list)):
        file = file_list[i]
        print_info("%d/%d: %s" % (i + 1, len(file_list), file))
        process_file(file)

    print_info("Done.")
