import os
import numpy as np

def calculate_overall_rrms(measured_list, modeled_list):
    """
    Computes overall RRMS by averaging the individual RRMS errors 
    of M distinct curves: RRMS = (1/M) * sum(RRMS_k)
    """
    rrms_k_list = []
    M = len(measured_list)
    
    if M == 0:
        return 0.0, 0.0
        
    for k in range(M):
        meas = np.array(measured_list[k])
        mod = np.array(modeled_list[k])
        
        # 1. Compute the RMS Error for curve k (Numerator)
        rms_error_k = np.sqrt(np.mean((mod - meas) ** 2))
        
        # 2. Compute Mean of Data for curve k (Denominator)
        mean_data_k = np.mean(np.abs(meas))
        if mean_data_k == 0:
            mean_data_k = 1e-9
            
        # 3. Calculate RRMS_k
        rrms_k = rms_error_k / mean_data_k
        rrms_k_list.append(rrms_k)
    
    # 4. Perform the final summation over M curves and divide by M
    overall_mean_rrms = (1.0 / M) * np.sum(rrms_k_list)
    population_std = np.std(rrms_k_list)
    
    return overall_mean_rrms, population_std

def calculate_rrms(meas_curves, mod_curves):
    total_sq_error, total_sq_meas = 0, 0
    for meas, mod in zip(meas_curves, mod_curves):
        min_len = min(len(meas), len(mod))
        total_sq_error += np.sum((meas[:min_len] - mod[:min_len]) ** 2)
        total_sq_meas += np.sum(meas[:min_len] ** 2)
    return np.sqrt(total_sq_error / total_sq_meas) if total_sq_meas > 0 else 0.0

pMeas_Dir = '/home/oliviag/Skywater-130nm-77K-Cryogenic-Models/cryo_data/'
pModel_Dir = '/home/oliviag/ngspice-skywater-sims/pfet_mod/'
nModel_Dir = '/home/oliviag/ngspice-skywater-sims/nfet_mod/'

# PMOS Data Structures
p_device_names = []
p_measured_curves_all = []
p_modeled_curves_all = []
p_RRMS_indv = []

# NMOS Data Structures
n_device_names = []
n_measured_curves_all = []
n_modeled_curves_all = []
n_RRMS_indv = []

# --- GEOMETRY MAPS ---
pairs_vd_pmos = [
    ('pmos_FET_len_8_wid_0p84', 'l_8p0_w_0p84/vd_sweep/'),
    ('pmos_FET_len_0.35_wid_1.6', 'l_0p35_w_1p6/vd_sweep/'),
    ('pmos_FET_len_0p5_wid_0p42', 'l_0p50_w_0p42/vd_sweep/'),
    ('pmos_FET_len_0p35_wid_0p55', 'l_0p35_w_0p55/vd_sweep/'),
    ('pmos_FET_len_0p5_wid_0p64', 'l_0p50_w_0p64/vd_sweep/'),
    ('pmos_FET_len_0p35_wid_5', 'l_0p35_w_5p0/vd_sweep/'),
    ('pmos_FET_len_2_wid_5', 'l_2p0_w_5p0/vd_sweep/'),
    ('pmos_FET_len_4_wid_7', 'l_4p0_w_7p0/vd_sweep/'),
    ('pmos_FET_len_8_wid_1p6', 'l_8p0_w_1p6/vd_sweep/'),
    ('pmos_FET_len_8_wid_5', 'l_8p0_w_5p0/vd_sweep/')
]

pairs_vg_pmos = [
    ('pmos_FET_len_8_wid_0p84', 'l_8p0_w_0p84/vg_sweep/'),
    ('pmos_FET_len_0.35_wid_1p6', 'l_0p35_w_1p6/vg_sweep/'),
    ('pmos_FET_len_0p5_wid_0p42', 'l_0p50_w_0p42/vg_sweep/'),
    ('pmos_FET_len_0p35_wid_0p55', 'l_0p35_w_0p55/vg_sweep/'),
    ('pmos_FET_len_0p5_wid_0p64', 'l_0p50_w_0p64/vg_sweep/'),
    ('pmos_FET_len_0p35_wid_5', 'l_0p35_w_5p0/vg_sweep/'),
    ('pmos_FET_len_2_wid_5', 'l_2p0_w_5p0/vg_sweep/'),
    ('pmos_FET_len_4_wid_7', 'l_4p0_w_7p0/vg_sweep/'),
    ('pmos_FET_len_8_wid_1p6', 'l_8p0_w_1p6/vg_sweep/'),
    ('pmos_FET_len_8_wid_5', 'l_8p0_w_5p0/vg_sweep/')
]

pairs_vd_nmos = [
    ('nmos_FET_len_0p15_wid_1p6', 'l_0p15_w_1p6/vd_sweep/'),
    ('nmos_FET_len_0p19_wid_7', 'l_0p19_w_7p0/vd_sweep/'),
    ('nmos_FET_len_0p25_wid_1p6', 'l_0p25_w_1p6/vd_sweep/'),
    ('nmos_FET_len_1_wid_1p6', 'l_1p0_w_1p6/vd_sweep/'),
    ('nmos_FET_len_1_wid_3', 'l_1p0_w_3p0/vd_sweep/'),
    ('nmos_FET_len_8_wid_1.6', 'l_8p0_w_1p6/vd_sweep/'),
    ('nmos_FET_len_20_wid_0p64', 'l_20p0_w_0p64/vd_sweep/'),
    ('nmos_FET_len_100_wid_100', 'l_100p0_w_100p0/vd_sweep/'),
]

pairs_vg_nmos = [
    ('nmos_FET_len_0p15_wid_1p6', 'l_0p15_w_1p6/vg_sweep/'),
    ('nmos_FET_len_0p19_wid_7', 'l_0p19_w_7p0/vg_sweep/'),
    ('nmos_FET_len_0p25_wid_1p6', 'l_0p25_w_1p6/vg_sweep/'),
    ('nmos_FET_len_1_wid_1p6', 'l_1p0_w_1p6/vg_sweep/'),
    ('nmos_FET_len_1_wid_3', 'l_1p0_w_3p0/vg_sweep/'),
    ('nmos_FET_len_8_wid_1.6', 'l_8p0_w_1p6/vg_sweep/'),
    ('nmos_FET_len_20_wid_0p64', 'l_20p0_w_0p64/vg_sweep/'),
    ('nmos_FET_len_100_wid_100', 'l_100p0_w_100p0/vg_sweep/'),
]

# --- FILE SUB-PAIRS ---
#p_vds_pairs = [('p_vds_sweep_step0.txt', 'idvd_Vg-0p37.csv'), ('p_vds_sweep_step1.txt', 'idvd_Vg-0p74.csv'), ('p_vds_sweep_step2.txt', 'idvd_Vg-1p11.csv'), ('p_vds_sweep_step3.txt', 'idvd_Vg-1p48.csv'), ('p_vds_sweep_step4.txt', 'idvd_Vg-1p85.csv')]
p_vds_pairs = [('p_vds_sweep_step4.txt', 'idvd_Vg-0p37.csv'), ('p_vds_sweep_step3.txt', 'idvd_Vg-0p74.csv'), ('p_vds_sweep_step2.txt', 'idvd_Vg-1p11.csv'), ('p_vds_sweep_step1.txt', 'idvd_Vg-1p48.csv'), ('p_vds_sweep_step0.txt', 'idvd_Vg-1p85.csv')]

p_vgs_pairs = [('p_vgs_sweep_step0.txt', 'idvg_Vd-0p01.csv'), ('p_vgs_sweep_step1.txt', 'idvg_Vd-0p37.csv'), ('p_vgs_sweep_step2.txt', 'idvg_Vd-0p74.csv'), ('p_vgs_sweep_step3.txt', 'idvg_Vd-1p11.csv'), ('p_vgs_sweep_step4.txt', 'idvg_Vd-1p48.csv'), ('p_vgs_sweep_step5.txt', 'idvg_Vd-1p85.csv')]

n_vds_pairs = [('vds_sweep_step0.txt', 'idvd_Vg0p37.csv'), ('vds_sweep_step1.txt', 'idvd_Vg0p74.csv'), ('vds_sweep_step2.txt', 'idvd_Vg1p11.csv'), ('vds_sweep_step3.txt', 'idvd_Vg1p48.csv'), ('vds_sweep_step4.txt', 'idvd_Vg1p85.csv')]
n_vgs_pairs = [('vgs_sweep_step0.txt', 'idvg_Vd0p01.csv'), ('vgs_sweep_step1.txt', 'idvg_Vd0p37.csv'), ('vgs_sweep_step2.txt', 'idvg_Vd0p74.csv'), ('vgs_sweep_step3.txt', 'idvg_Vd1p11.csv'), ('vgs_sweep_step4.txt', 'idvg_Vd1p48.csv'), ('vgs_sweep_step5.txt', 'idvg_Vd1p85.csv')]



for i in range(len(pairs_vd_pmos)):
    measDir, modDirVd = pairs_vd_pmos[i]
    _, modDirVg = pairs_vg_pmos[i]
    this_device_meas, this_device_mod = [], []
    pathMeas, pathModVd, pathModVg = os.path.join(pMeas_Dir, measDir), os.path.join(pModel_Dir, modDirVd), os.path.join(pModel_Dir, modDirVg)
    
    for mod_f, meas_f in p_vgs_pairs:
        try:
            #this_device_mod.append(np.abs(np.loadtxt(os.path.join(pathModVg, mod_f), usecols=3, unpack=True)))
            #this_device_meas.append(np.abs(np.loadtxt(os.path.join(pathMeas, meas_f), skiprows=1, delimiter=',', usecols=2, unpack=True)))
            p_model = np.abs(np.loadtxt(os.path.join(pathModVg, mod_f), usecols=3, unpack=True))
            p_meas = np.abs(np.loadtxt(os.path.join(pathMeas, meas_f), skiprows=1, delimiter=',', usecols=2, unpack=True))
            
            
            this_device_mod.append(p_model)
            this_device_meas.append(p_meas)
        except: pass
    for mod_f, meas_f in p_vds_pairs:
        try:
            #this_device_mod.append(np.abs(np.loadtxt(os.path.join(pathModVd, mod_f), usecols=3, unpack=True)))
            #this_device_meas.append(np.abs(np.loadtxt(os.path.join(pathMeas, meas_f), skiprows=1, delimiter=',', usecols=2, unpack=True)))
            p_model = np.abs(np.loadtxt(os.path.join(pathModVd, mod_f), usecols=3, unpack=True))
            p_meas = np.abs(np.loadtxt(os.path.join(pathMeas, meas_f), skiprows=1, delimiter=',', usecols=2, unpack=True))
            
            this_device_mod.append(p_model)
            this_device_meas.append(p_meas)
        except: pass
    if this_device_meas:
        p_device_names.append(measDir)
        p_measured_curves_all.append(this_device_meas)
        p_modeled_curves_all.append(this_device_mod)

       

for i in range(len(pairs_vd_nmos)):
    measDir, modDirVd = pairs_vd_nmos[i]
    _, modDirVg = pairs_vg_nmos[i]
    this_device_meas, this_device_mod = [], []
    pathMeas, pathModVd, pathModVg = os.path.join(pMeas_Dir, measDir), os.path.join(nModel_Dir, modDirVd), os.path.join(nModel_Dir, modDirVg)
    
    for mod_f, meas_f in n_vgs_pairs:
        try:
            this_device_mod.append(np.abs(np.loadtxt(os.path.join(pathModVg, mod_f), usecols=3, unpack=True)))
            this_device_meas.append(np.abs(np.loadtxt(os.path.join(pathMeas, meas_f), skiprows=1, delimiter=',', usecols=2, unpack=True)))
        except: pass
    for mod_f, meas_f in n_vds_pairs:
        try:
            this_device_mod.append(np.abs(np.loadtxt(os.path.join(pathModVd, mod_f), usecols=3, unpack=True)))
            this_device_meas.append(np.abs(np.loadtxt(os.path.join(pathMeas, meas_f), skiprows=1, delimiter=',', usecols=2, unpack=True)))
        except: pass
    if this_device_meas:
        n_device_names.append(measDir)
        n_measured_curves_all.append(this_device_meas)
        n_modeled_curves_all.append(this_device_mod)

for idx in range(len(p_device_names)):
    p_RRMS_indv.append({'geometry': p_device_names[idx], 'rrms': calculate_rrms(p_measured_curves_all[idx], p_modeled_curves_all[idx])})

for idx in range(len(n_device_names)):
    n_RRMS_indv.append({'geometry': n_device_names[idx], 'rrms': calculate_rrms(n_measured_curves_all[idx], n_modeled_curves_all[idx])})


print("\n" + "="*60)
print(f"{'SKYWATER DEVICE GEOMETRY':<35} | {'COMBINED RRMS':<15}")
print("="*60)
print("--- PMOS DEVICES ---")
for entry in p_RRMS_indv:
    print(f"{entry['geometry']:<35} | {entry['rrms']:.4f}")

print("\n--- NMOS DEVICES ---")
for entry in n_RRMS_indv:
    print(f"{entry['geometry']:<35} | {entry['rrms']:.4f}")

# Pool raw calculations into a single list for joint analysis
p_rrms_values = [e['rrms'] for e in p_RRMS_indv]
n_rrms_values = [e['rrms'] for e in n_RRMS_indv]
combined_rrms_values = p_rrms_values + n_rrms_values

if combined_rrms_values:
    print("\n" + "="*60)
    print(f"{'TOTAL POOLED MEAN RRMS (ALL FETs):':<35} | {np.mean(combined_rrms_values):.4f}")
    print(f"{'TOTAL POOLED STANDARD DEV (σ):':<35} | {np.std(combined_rrms_values):.4f}")
    print("="*60)
else:
    print("\n Error: No datasets were successfully parsed and computed.")