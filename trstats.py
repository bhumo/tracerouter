from subprocess import run
import json
import numpy
import matplotlib.pyplot as pyplt
import sys
import os
import time
import re


# Pending functionalities
# 1. Instead of creating files for computing the data use some other way to solve it
# 2. Add the input functionalities to take argument
# 3. Add the TEST_DIR and path and etc functionalities
# 4. The code for running traceroute is slow.



ttl_np_array_list = []
hop_map = {}
MAX_HOP = "30"
TARGET = "www.google.com"
NUM_RUNS = 10
RUN_DELAY = 0
JSON_OUTPUT_PATH_AND_NAME = "data.json"
PDF_GRAPH_PATH_NAME = "stats"

TEST_DIR = ""

class Hop:
    def __init__(self):        
        self.ip_address = set()
        self.ttl = []





def extractHopsFromFile(filename):
    file = open(filename,'r')
    next(file)
    for line in file:
        line = line.strip()
        data = line.replace("  "," ").split(' ')
        hop_number = int(data[0])

        
        if data[1]!= '*' and data [4] != '*':
            #extract the IPs

            hop_object = Hop()
            if hop_map.get(hop_number):
                hop_object = hop_map[hop_number]
            ip_add_tuple = (data[1], data[2])
            hop_object.ip_address.add(ip_add_tuple)
            # hop_object.ip_address.append(data[1])
            # hop_object.ip_address.append(data[2])

            #three packets time     
            length = len(data)   

            for i in range(3,length):
                try:
                    time = float(data[i])
                    hop_object.ttl.append(time)

                except:
                    pass

            # print(hop_object.ip_address)
            # print(hop_object.ttl)
            # print("_______________________")
            hop_map[hop_number] = hop_object
            
        else:
            if data[3] != '*' :
                #this is the case where we have reached the last hop that is my destination
                #now i have to add it
                hop_object = Hop()
                if hop_map.get(hop_number):
                    hop_object = hop_map[hop_number]
                
                line = line.replace("*"," ")
                
                new_data = line.split(' ')
                hop_number = int(new_data[0])
                ip_add_tuple = (new_data[1], new_data[2])
                hop_object.ip_address.add(ip_add_tuple)
                # hop_object.ip_address.append(new_data[1])
                # hop_object.ip_address.append(new_data[2])
                
                #now add the time for the packets
                length = len(new_data)
                for i in range(3,length):
                    time = new_data[i]
                    try:
                        time = float(data[i])
                        hop_object.ttl.append(time)
                    except:
                        pass
                hop_map[hop_number] = hop_object


def create_json_output_file(hop_map):
    file = open(JSON_OUTPUT_PATH_AND_NAME,'w')
    json_output = create_json_from_hops_map(hop_map)
    json.dump(json_output,file, indent= 5)
    file.close()


def create_json_from_hops_map(hop_map):
    """
        json = [
  {'avg': 0.645,
  'hop': 1,
  'hosts': [['172.17.0.1', '(172.17.0.1)']],
  'max': 2.441,
  'med': 0.556,
  'min': 0.013},
 {'avg': 6.386,
  'hop': 2,
  'hosts': [['testwifi.here', '(192.168.86.1)']],
  'max': 16.085,
  'med': 5.385,
  'min': 3.108}]
    """
    json_output = []
    sorted_keys = sorted(hop_map.keys())
    for hop in sorted_keys:
        
        hop_obj = hop_map[hop]

        ttl_np_array = numpy.array(hop_obj.ttl)
        ttl_np_array_list.append(hop_obj.ttl)
        numpy.set_printoptions(precision=3)
        avg = numpy.average(ttl_np_array)
        hosts = list(hop_obj.ip_address)
        maxi = max(hop_obj.ttl)       
        med = numpy.median(ttl_np_array)
        mini = min(hop_obj.ttl)
        out = {
            "avg" : avg,
            "hop" : hop,
            "hosts": hosts,
            "max" : maxi,
            "med": med,
            "min" : mini
        }
        json_output.append(out)

    return json_output

def create_box_plot():
    mean_style ={
        'marker':'o',
        'markerfacecolor': 'black'
    }
      
    pyplt.boxplot(ttl_np_array_list, showmeans= True, meanprops=mean_style)

def show_box_plot():
    pyplt.show()

def save_box_plot():
    pyplt.savefig(PDF_GRAPH_PATH_NAME+'.pdf')

# def create_output_files(traceRoute_Output,N):

    # length = N
    # for i in range (0,N):
    #     file_name = 'tr_run-'+ str(i+1) + '.out'
    #     file = open(file_name,'wb')
    #     #opening the file in write byte mode so that we can directly add the output to the file
    #     file.write(traceRoute_Output[i])
    #     file.close()
        
    #     extractHopsFromFile(file_name)

def get_file_names(N):
    for i in range(0,N):
        file_name = 'tr_run-'+ str(i+1) + '.out'
        extractHopsFromFile(file_name)


def run_traceroute():
     traceRoute_Output = []
     for i in range(0,NUM_RUNS):
         opt = run(["traceroute", TARGET, '-m', MAX_HOP],capture_output=True).stdout
         extractHopsFromList((get_string_list_from_byte_arr(opt)))
         time.sleep(RUN_DELAY)
         
    #traceroute output will contain byte array
    #decode the byte array into str list
     #extractHopsFromList(traceRoute_Output)
     

def get_string_list_from_byte_arr(bytearray):
    print(bytearray.decode('utf-8').replace("  "," ").split("\n"))
    return bytearray.decode('utf-8').replace("  "," ").split('\n')

def extractHopsFromList(traceRoute_Output):
    length = len(traceRoute_Output)
    
    for i in range(1,length):
        
        line = traceRoute_Output[i]
        line = line.strip()
        data = line.split(' ')
        
        try:
            hop_number = int(data[0])
        except:
            continue

        
        if data[1]!= '*' and data [4] != '*':
            #extract the IPs

            hop_object = Hop()
            if hop_map.get(hop_number):
                hop_object = hop_map[hop_number]
            ip_add_tuple = (data[1], data[2])
            hop_object.ip_address.add(ip_add_tuple)
            # hop_object.ip_address.append(data[1])
            # hop_object.ip_address.append(data[2])

            #three packets time     
            data_length = len(data)   

            for i in range(3,data_length):
                try:
                    time_ttl = float(data[i])
                    hop_object.ttl.append(time_ttl)

                except:
                    pass

            # print(hop_object.ip_address)
            # print(hop_object.ttl)
            # print("_______________________")
            hop_map[hop_number] = hop_object
            
        else:
            if data[3] != '*' :
                #this is the case where we have reached the last hop that is my destination
                #now i have to add it
                hop_object = Hop()
                if hop_map.get(hop_number):
                    hop_object = hop_map[hop_number]
                
                line = line.replace("*","")
                                
                line = line.strip()
                new_data = line.split(' ')
                # print(new_data)
                # time.sleep(int(10))
                hop_number = int(new_data[0])
                ip_add_tuple = (new_data[1], new_data[2])
                hop_object.ip_address.add(ip_add_tuple)
                # hop_object.ip_address.append(new_data[1])
                # hop_object.ip_address.append(new_data[2])

                #now add the time for the packets
                length = len(new_data)
                for i in range(3,length):
                    time_ttl = new_data[i]
                    try:
                        time_ttl = float(data[i])
                        hop_object.ttl.append(time_ttl)
                    except:
                        pass
                hop_map[hop_number] = hop_object

def print_help_message():
    print("usage: trstats.py [-h] [-n NUM_RUNS] [-d RUN_DELAY] [-m MAX_HOPS] -o OUTPUT -g GRAPH [-t TARGET] [--test TEST_DIR]")
    print("Run traceroute multiple times towards a given target host optional arguments:")
    print("-h, --help)",end = "    ")
    print("show this help message and exit")
    print("-n NUM_RUNS",end = "    ")
    print("Number of times traceroute will run")
    print("-d RUN_DELAY",end = "    ")
    print("Number of seconds to wait between two consecutive runs")
    print("-m MAX_HOPS",end = "    ")
    print("Number of times traceroute will run")
    print("-o OUTPUT",end = "    ")
    print("Path and name of output JSON file containing the stats")
    print("-g GRAPH",end = "    ")
    print("Path and name of output PDF file containing stats graph")
    print("-t TARGET",end = "    ")
    print("--test TEST_DIR",end = "    ")
    print("A target domain name or IP address (required if --testis absent)", end="  ") 
    print("Directory containing num_runs text files, each of which contains the output of a traceroute run. If present, this will override all other options and traceroute will not be invoked. Stats will be computed over the traceroute output stored in the text files")
# 
# 
args = sys.argv
length_of_args = len(args)
if length_of_args == 1:
    print_help_message()
    sys.exit(0)
i=1
while i<length_of_args:
    argument = args[i]
    
    if(argument == "-h" or argument == "--help"):
        print_help_message()
        sys.exit(0)
        
    if(argument == "-t"):
        #specify the target
        TARGET = args[i+1]
        i = i+1
        continue

    if(argument == "--test"):
        #stop everything and read from the file only
        #assuming we will get the test dir
        # let's validate it
        i=i+1
        path = args[i]
        dir_list = os.listdir(path)
 
        for fileName in dir_list:
            extractHopsFromFile(path+"/"+fileName)
            create_json_output_file(hop_map)
            create_box_plot()
            save_box_plot()
            show_box_plot()
        sys.exit(0)
        
    if(argument == "-n"):
        # -n is the NUM_RUNS for the tracerouter
        NUM_RUNS = int(args[i+1])
        i=i+1
        continue
    
    if (argument == "-d"):
        # -d is the run delay i.e., how much time to wait for the next traceruote to start
        RUN_DELAY = int(args[i+1])
        i=i+1
        continue
        
    if (argument == "-m"):
        #-m is the max hop
        MAX_HOP = args[i+1]
        i=i+1
        continue
        
    if(argument == "-o" or argument == "-O"):
      # path of the json output file
        JSON_OUTPUT_PATH_AND_NAME = args[i+1]
        i=i+1
        continue
   
    if(argument == "-g"):
        # Path and name of output PDF file containing stats graph 
        PDF_GRAPH_PATH_NAME = args[i+1]
        i=i+1
        continue
        
 
    i= i+1

run_traceroute()
create_json_output_file(hop_map)
create_box_plot()
save_box_plot()
# show_box_plot()









