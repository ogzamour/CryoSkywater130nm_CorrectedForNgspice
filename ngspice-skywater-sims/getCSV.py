import csv
import sys
inde = [0, 1, 2, 3, 4]

for i in inde:

    input_file = f"/home/oliviag/ngspice-skywater-sims/sim_data_vd/{i}_mosfetvgs_mc_all.dat"
    output_file = f"/home/oliviag/ngspice-skywater-sims/sim_data_vd/{i}_mosfetVGS_MC_all.csv"
    
    
    headers = ["vSweep", "run_num", "vd", "id", "vth0", "u0", "rdsw", "nfactor", "vsat", "eta0"]
    
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        
   
        writer.writerow(headers)
        
       
        next(infile) 
        for line in infile:
           
            row = [val for val in line.strip().split() if val]
            if row:
                writer.writerow(row)
for i in inde:
    input_file = f"/home/oliviag/ngspice-skywater-sims/sim_data_vd/{i}_mosfetvds_mc_all.dat"
    output_file = f"/home/oliviag/ngspice-skywater-sims/sim_data_vd/{i}_mosfetVDS_MC_all.csv"
    

    headers = ["vSweep", "run_num", "vd", "id", "vth0", "u0", "rdsw", "nfactor", "vsat", "eta0"]
    
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        
      
        writer.writerow(headers)
        
  
        next(infile) 
        for line in infile:
            
            row = [val for val in line.strip().split() if val]
            if row:
                writer.writerow(row)
