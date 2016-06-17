#  -*- coding: utf-8 -*-
#!/usr/bin/python
import os, subprocess, sys, codecs

def makeDir(dir_name):
    if (not os.path.exists(dir_name)):
        os.makedirs(dir_name)

#排序文件
def sortFile(file_name):

    makeDir('temp')

    tags = os.path.split(__file__)
    filesort = os.path.join(tags[0],'FileSort.jar')

    file_sorted = file_name + ".sort"

    tags = os.path.split(file_name)
    command_line = 'java -jar ' + filesort + ' 2 ' + tags[0] + '/ ' + tags[1] + ' 3'
    print('Excute Command: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

    return file_sorted

def generateRealOffLineResult(basedata, input_file, bus_rel, output):

    if not os.path.exists(basedata):
        print(basedata + ' not exist!')
        return False
    if not os.path.exists(input_file):
        print(input_file + 'not exist!')
        return False
    if not os.path.exists(bus_rel):
        print(bus_rel + ' not exist!')
        return False

    tags = os.path.split(__file__)
    excute_file = os.path.join(tags[0],'BusMatchingResultGenerator.exe')

    command_line = excute_file + ' -m=0 -lon=10 -lat=11 -l=' + basedata + ' -i=' + input_file + ' -b=' + bus_rel+ ' -o=' + output
    print('生成judgement_result.csv: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

    return True

#从bus_file里获取公交车辆关系
def getBusRelations(bus_relation_file):

    if not os.path.exists(bus_relation_file):
        print(bus_relation_file + ' not exists')
        return False, []

    bus_file = codecs.open(bus_relation_file, 'r', 'utf-8')
    line = bus_file.readline()

    bus_relations = dict()

    while line:
        line = line.strip()
        tags = line.split(',')
        #bus_relations[tags[1]] = tags[0]
        if not tags[1] in bus_relations.keys():
            bus_relations[tags[1]] = []
        bus_relations[tags[1]].append(tags[0])
        #bus_relations.append((tags[0],tags[1]))
        line = bus_file.readline()

    bus_file.close()
    #print("BusRelations:")
    #print(bus_relations)

    return True, bus_relations
