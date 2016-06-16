#  -*- coding: utf-8 -*-
#!/usr/bin/python

#BusStat.py
import codecs, os, subprocess, sys
'''
Created on 2016-05-20

@author: RamboWu
'''
def IfContinueOn(tip):
    a = 'O'
    while (not(a in ('Y','y','N','n'))):
        a=input(tip +"?Y/N ")

    if a in ('N','n'):
        return False
    else:
        return True

#产生公交关系
def generateBusRelations(base_data_file, input_file, bus_relation_file):

    command_line = 'BusMatching.exe --offline --baseData ' + base_data_file + ' --inputFile ' + input_file + ' --bus_rel_file ' + bus_relation_file
    print('生成BusRelations: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

#从bus_file里获取公交车辆关系
def getBusRelations(bus_relation_file):
    bus_file = codecs.open(bus_relation_file, 'r', 'utf-8')
    line = bus_file.readline()

    bus_relations = []

    while line:
        tags = line.split(',')
        bus_relations.append(tags[0])
        line = bus_file.readline()

    bus_file.close()
    #print("BusRelations:")
    #print(bus_relations)

    return bus_relations

#把input_file里相关的公交车辆GPS数据打印到tmp文件里，等待排序
def printRelateBus(src_file_name, dest_file_name, bus_relations):
    src_file = codecs.open(src_file_name, 'r', 'utf-8')
    dest_file = codecs.open(tmp_file_name, 'w', 'utf-8')

    line = src_file.readline()
    while line:
        tags = line.split(',')
        if tags[3] in bus_relations:
            dest_file.write(line)
        line = src_file.readline()

    src_file.close();
    dest_file.close();

#根据BusRelations来取出待排序的gps点，然后排序
def generateSortedSample(input_file, output_file, bus_relation_file):

    #从bus_file里获取公交车辆关系
    bus_relations = getBusRelations(bus_relation_file)
    #把input_file里相关的公交车辆GPS数据打印到tmp文件里，等待排序
    printRelateBus(input_file, output_file, bus_relations)
    #排序tmp文件
    sortTmp()

#排序文件
def sortFile(file_name, force = False):
    file_sorted = file_name + ".sort"

    if not force and not IfContinueOn('是否要排序:'+file_name):
        return file_sorted

    tags = os.path.split(file_name)
    command_line = 'java -jar FileSort.jar 2 ' + tags[0] + '/ ' + tags[1] + ' 3'
    print('Excute Command: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

    return file_sorted

def generateRealOffLineResult(basedata, input_file, bus_rel, output, force = False):

    if not force and not IfContinueOn('是否要生成对比Sample文件:' + input_file):
        return

    command_line = 'BusMatchingResultGenerator.exe -m=0 -lon=10 -lat=11 -l=' + basedata + ' -i=' + input_file + ' -b=' + bus_rel+ ' -o=' + output
    print('生成judgement_result.csv: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)
