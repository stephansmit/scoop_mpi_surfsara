import os
import subprocess
import sys
import argparse
def make_hostfile(hosts, filename):
    string = "scontrol show hostname " +hosts
    cmd = string.split(" ")
    with open(filename,"w") as stdout:
    	process = subprocess.Popen(cmd, stdout=stdout)
    process.communicate()


def get_hosts(nodelist):
    string = "scontrol show hostname " +nodelist
    cmd = string.split()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate() 
    hosts =filter(None,output.split('\n'))
    return hosts
    
def write_hostfile(hosts, cores, filename):
    lines = map(lambda x: " ".join(x),zip(hosts, cores))
    with open(filename, 'w') as f:
        for line in lines:
            f.write("%s\n" % line)

def calculate_min_tasks_per_node(ntasks, nnodes):
    total = 0
    ntasks_per_node = 0.0
    while (total < ntasks):
        ntasks_per_node += 1
	total = ntasks_per_node*nnodes
    min_ntasks=ntasks_per_node-1 
    ntasks_left=ntasks-min_ntasks*nnodes
    return int(min_ntasks), int(ntasks_left) 


def create_ncores_list(min, left, nnodes):
    cores = [min]*nnodes
    for i in range(0,left):
       cores[i]+=1
    return [str(i) for i in cores]
     

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Create a hostfile for Slurm batchjob')
    parser.add_argument('--filename', help="the filename of the hostfile")
    parser.add_argument('--testmodus', action='store_true', help="run in testmodus")
    parser.add_argument('--ncores', help="number of cores", type=int )
    args = parser.parse_args()  


    if (args.testmodus):
	hoststring = 'tcn[560-563]'
    else:
        try:
	    hoststring = os.environ['SLURM_JOB_NODELIST']
        except: 
            print("This executable works only in a slurmjob otherwise use --testmodus")
            exit()
          

    
    hosts = get_hosts(hoststring)
    nnodes = len(hosts)
    min_tasks, left = calculate_min_tasks_per_node(args.ncores,nnodes)
    cores = create_ncores_list(min_tasks, left, nnodes)
    write_hostfile(hosts, cores, args.filename)



