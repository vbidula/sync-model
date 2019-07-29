import numpy as np
from multiprocessing import Process
from time import sleep
import pandas as pd
import json
import os

import constants as c
from models import *
from synchrotron import *
from table_model import TableModel

import warnings
warnings.filterwarnings("ignore")


print("Electron distribution defining...")

##########CHOOSE ELECTRON DISTRIBUTION HERE(by uncommenting)###########
# dist = Powerlaw(
#     elec = c.elec1,
#     glow = c.glow,
#     ghigh = c.ghigh,
# )
# dist = SmoothBPL(
#     elec1 = c.elec1,
#     elec2 = c.elec2,
#     gbreak = c.gbreak,
#     glow = c.glow,
#     ghigh = c.ghigh,
# )
dist = Expcutoff(
    elec = c.elec1,
    beta = c.beta,
    glow = c.glow,
    ghigh = c.ghigh,
)
#######################################################################
# dist.getColsDict()

if c.Escale == 'log':
    E = np.logspace(c.Emin, c.Emax, num = c.Epoints+1)
elif c.Escale == 'lin':
    E = np.linspace(c.Emin, c.Emax, num = c.Epoints+1)
else:
    raise Exception("The Escale parameter is specified wrong.")

assert c.Nsep > 1, ("Can't separate interval into {} subintervals.".format(c.Nsep,))

nu = keVtoHz(E[1:])
E

pars_dict = getColsDict(dist)
pars_dict

# %%
energy_dict = {}
energy_dict['ENERG_LO'] = E[:-1]
energy_dict['ENERG_HI'] = E[1:]

# === Using multiple cores to calculate table ===
print("Preparing before parallelizing...")
nu_split = np.array_split(nu, c.Nproc)
cores = np.arange(1,c.Nproc+1)
fnames = ['core_'+str(core)+'_calc.txt' for core in cores]
syncs = [Synchrotron(dist, usebar=False) for i in cores]
syncs[0] = Synchrotron(dist, usebar=True)

def calcOnCore(nu_sp, sync, core, filename):
    sd = sync.genTable(nu_sp, c.Nsep)
    with open(filename, 'w+') as file:
        for i in range(0, len(sd['PARAMVAL'])):
            file.write(
                str(sd['PARAMVAL'][i])+'\t'+str(sd['INTPSPEC'][i])+'\n'
            )

procs = []
for core in cores:
    procs.append(
        Process(target=calcOnCore,
                args=(nu_split[core-1], syncs[core-1], core, fnames[core-1]))
    )
for p in procs:
    p.start()

for p in procs:
    p.join()

while True in [p.is_alive() for p in procs]:
    time.sleep(0.5)

print("Creating XSPEC table...")
files = [pd.read_csv(fname, sep='\t', header=None) for fname in fnames]
paramval = [json.loads(pv) for pv in files[0][0]]
intpspec = []

for i in range(len(paramval)):
    curspec = []
    for core in cores:
        curspec += json.loads(files[core-1][1][i])
    intpspec.append(curspec)

spectra_dict = {
    "PARAMVAL": paramval,
    "INTPSPEC": intpspec,
}

for i in range(len(fnames)):
    try:
        os.remove(fnames[i])
    except FileNotFoundError:
        pass

table = TableModel(
    pars_dict,
    energy_dict,
    spectra_dict,
    nintpars = len(pars_dict['NAME']),
    )
table.save_to(c.TableName)

print("Done!")
