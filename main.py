from scoop import futures
import os 
import subprocess
import numpy as np
from functools import partial

# function that calls the MPI-CODE
def mpi_exec_function(casename, input_file, cores, exec_dir):        
    fin = open(input_file)
    ferr = open(str(casename)+'.err', 'w')
    flog = open(str(casename)+'.log', 'w')
    fout = open(str(casename)+'.out', 'w')
    
    cmd = "/hpc/eb/RedHatEnterpriseServer7/OpenMPI/2.1.1-GCC-6.4.0-2.28/bin/mpirun -np "+str(cores)+" "+os.path.join(exec_dir,'run')+' mpi_input.cfg' #run is the name of the executable
    p = subprocess.Popen(
            cmd, shell=True, stdout=fout, stderr=ferr, cwd=os.getcwd())
    p.communicate()
    ferr.close()
    flog.close()
    fin.close()
    return "Succes"


if __name__ == "__main__":
    os.system("mkdir -p pipe") #make directory (is need for the MPI-CODE to run succesfully)
    
    mpi_exec_dir = os.environ['RANSCODE_RUN']                  #directory of the MPI-CODE
    mpi_input_file = os.path.join(os.getcwd(),"mpi_input.cfg") #input file for #MPI-CODE

    ncores_mpi= 4 #this is the number of cores for running the MPI-CODE
    ncases = 48   #Number of times the MPI-Code is called in total (nthreads in the batchjob will determine how many in parallel)
    cases = np.linspace(1,ncases,ncases-1, dtype=int)
    returnValues = list(futures.map(partial(mpi_exec_function,input_file=mpi_input_file, cores=ncores_mpi, exec_dir=mpi_exec_dir),cases))

