from subprocess import run
import json
import numpy
class Hop:
    ip_address = []
    ttl = []

class HopLatency:
    hop_number = -1
    average = -1
    median = -1
    maximum = -1
    minimum = -1

Hops_LATENCY_DATA = []

def extractHopsFromFile(filename):
    file = open(filename,'r')
    next(file)
    hop_map = {}
    for line in file:
        line = line.strip()
        data = line.split(' ')
        hop_number = data[0]

        # print(data[0])
        # print('@@@@@@@@@@@@@@@@@')
        if data[2]!= '*' and data [4] != '*':
            #extract the IPs
            hop_object =  Hop()
            hop_object.ip_address.append(data[2])
            hop_object.ip_address.append(data[3])

            #three packets time     
            length = len(data)   

            for i in range(5,length):
                try:
                    time = float(data[5])
                    hop_object.ttl.append(time)

                except:
                    pass

            # print(hop_object.ip_address)
            # print(hop_object.ttl)
            # print("_______________________")
            hop_map[hop_number] = hop_object
    create_json_output_file(hop_map)

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
    average_per_hop = []
    median_per_hop = []
    
    for hop in hop_map:
        hop_obj = hop_map[hop]
        ttl_np_array = numpy.array(hop_obj.ttl)
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
    


def create_output_files(traceRoute_Output,N):

    length = N
    for i in range (0,N):
        file_name = 'tr_run-'+ str(i+1) + '.out'
        file = open(file_name,'wb')
        #opening the file in write byte mode so that we can directly add the output to the file
        file.write(traceRoute_Output[i])
        file.close()
        
        extractHopsFromFile(file_name)


host = 'www.google.com'
max_hop = '35'
no_of_runs = 1
traceRoute_Output = []
for i in range(0,no_of_runs):
    traceRoute_Output.append(run(["traceroute", host, '-m', max_hop],capture_output=True).stdout)

create_output_files(traceRoute_Output,no_of_runs)





