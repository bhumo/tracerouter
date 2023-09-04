from subprocess import run
import json
import numpy
import matplotlib.pyplot as pyplt


# Pending functionalities
# 1. Instead of creating files for computing the data use some other way to solve it
# 2. Add the input functionalities to take argument
# 3. Add the pdf generation functionality
# 4. Add the TEST_DIR and path and etc functionalities



ttl_np_array_list = []
hop_map = {}
MAX_HOP = 30
TARGET = "www.google.com"
NUM_RUNS = 1
RUN_DELAY = 0
OUTPUT = ""
PDF_GRAPH_PATH = ""
PDF_GRAPH_NAME = "stats"
TEST_DIR = ""

class Hop:
    def __init__(self):        
        self.ip_address = []
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

            hop_object.ip_address.append(data[1])
            hop_object.ip_address.append(data[2])

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
                hop_number = new_data[0]
                hop_object.ip_address.append(new_data[1])
                hop_object.ip_address.append(new_data[2])

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


def create_json_output_file(hop_map, filename ='data.json'):
    file = open(filename,'w')
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

    for hop in hop_map:
        
        hop_obj = hop_map[hop]
        ttl_np_array = numpy.array(hop_obj.ttl)
        ttl_np_array_list.append(hop_obj.ttl)
        numpy.set_printoptions(precision=3)
        avg = numpy.average(ttl_np_array)
        hosts = hop_obj.ip_address
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
    pyplt.boxplot(ttl_np_array_list)

def show_box_plot():
    pyplt.show()

def save_box_plot():
    pyplt.savefig(PDF_GRAPH_PATH+PDF_GRAPH_NAME+'.pdf')

def create_output_files(traceRoute_Output,N):

    length = N
    for i in range (0,N):
        file_name = 'tr_run-'+ str(i+1) + '.out'
        file = open(file_name,'wb')
        #opening the file in write byte mode so that we can directly add the output to the file
        file.write(traceRoute_Output[i])
        file.close()
        
        extractHopsFromFile(file_name)

def get_file_names(N):
    for i in range(0,N):
        file_name = 'tr_run-'+ str(i+1) + '.out'
        extractHopsFromFile(file_name)


def run_traceroute():
     for i in range(0,no_of_runs):
         traceRoute_Output.append(run(["traceroute", host, '-m', max_hop],capture_output=True).stdout)

host = 'www.google.com'
max_hop = '35'
no_of_runs = 5
traceRoute_Output = []
# for i in range(0,no_of_runs):
#     traceRoute_Output.append(run(["traceroute", host, '-m', max_hop],capture_output=True).stdout)
# print("TraceRoute is done running")
# create_output_files(traceRoute_Output,no_of_runs)
get_file_names(no_of_runs)
create_json_output_file(hop_map)
create_box_plot()
save_box_plot()
show_box_plot()









