from subprocess import run

class Hop:
    ip_address = []
    ttl = []

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
    for i in hop_map:
        print(i)
        print(hop_map[i].ip_address)
        print(hop_map[i].ttl)



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
no_of_runs = 10
traceRoute_Output = []
for i in range(0,no_of_runs):
    traceRoute_Output.append(run(["traceroute", host, '-m', max_hop],capture_output=True).stdout)

create_output_files(traceRoute_Output,no_of_runs)





