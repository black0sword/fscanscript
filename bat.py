import subprocess
import ipaddress
import sys


def execute_fscan(target):
    command = f"fscan -m mssql -h {target}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8")

def parse_b_segments(b_segment):
    segments = b_segment.split('.')
    target_list = []
    start_num , end_num = 0,0
    if segments[-1] == "0/16":
        #多B段扫描
        if '-' in segments[1]:
            start_num = int(segments[1].split('-')[0])
            end_num = int(segments[1].split('-')[1])

    b_num = end_num - start_num
    #print(segments)
    for b_duan in range(b_num+1):
        if b_duan == 0:
            segments[1] = str(start_num)
        else:
            segments[1] = str(start_num + b_duan)

        ip_duan = '.'.join(segments)
        target_list.append(ip_duan)

    return target_list

def batch_scan(targets):
    for target in targets:
        print(f"Scanning target: {target}")
        output = execute_fscan(target)
        print(output)
        print("------------------------------")

# 从命令行参数获取B段地址范围
# "10.224-226.0.0/16"
b_segment = sys.argv[1]  # 从命令行或其他方式获取B段地址范围

# 解析B段地址范围为列表
target_list = parse_b_segments(b_segment)
print(target_list)

batch_scan(target_list)
