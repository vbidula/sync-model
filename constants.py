# ===== Importing and defining physical constants =====
pi = 3.141592653589793
e = 4.80320451e-10
c = 29979245800.0
m_e = 9.10938356e-28
h = 6.626e-27

# ===== Parameters for modeling =====
# If 'FROZEN' == True then 'MIN' value will be used
# 'METHOD' (of xspec parameter interpolation) values:
#       0 if linear
#       1 if logarithmic

# Magnet field in Gausses
B = 1

##### CHOOSE ELECTRON DISTRIBUTION HERE #####
DIST = 'powerlaw'
# Possible distributions:
# - 'powerlaw'
# - 'brokenpl'
# - 'smoothbrokenpl'
# - 'expcutoffpl'
#############################################

# First powerlaw index (also used for simple powerlaw)
s1 = {
'NAME': 's1',
'MIN': 1.5,
'MAX': 3,
'FROZEN': False,
'METHOD': 0,
}

# Second powerlaw index
s2 = {
'NAME': 's2',
'MIN': 2,
'MAX': 3.5,
'FROZEN': False,
'METHOD': 0,
}

# Power of power of exponent in ExoCutoffPL
beta = {
'NAME': 'beta',
'MIN': 1,
'MAX': 1.5,
'FROZEN': True,
'METHOD': 0,
}


# Energy (integration interval) (powers)
glow = {
'NAME': 'glow',
'MIN': 1,
'MAX': 5,
'FROZEN': True,
'METHOD': 0,
}

ghigh = {
'NAME': 'ghigh',
'MIN': 4,
'MAX': 7,
'FROZEN': False,
'METHOD': 0,
}

# Energy break point(also power)
gbreak = {
'NAME': 'gbreak',
'MIN': 5,
'MAX': 6,
'FROZEN': True,
'METHOD': 0,
}

# ===== Other settings =====
# Data energy axis in keV
Escale = 'log' #'log' of 'lin'; if 'log' then Emin, Emax - powers
Emin = -3
Emax = 1
Epoints = 500   # Array length of E

# The number of subintervals - more precisely integration but takes much more time
Nsep = 5

Nvals = 25  # The number of tabulated values for each parameter
Pdelta = 1e-2   # Parameter delta used in fit
Nproc = 3  #The number of parallel processes to be started for table generating
# (do not specify this number greater than the number of avaiable processor cores)
TableName = "сtest.fits"  # Output
