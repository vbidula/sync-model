import numpy as np
import constants as c


def gtoE(gamma):
    E = (gamma - 1) * c.m_e * c.c**2
    return(E)


def Etog(E):
    gamma = E / c.m_e / c.c**2 + 1
    return(gamma)


def keVtoHz(E):
    return(2.417e17 * E)


def HztokeV(Hz):
    return(Hz / 2.417e17)


def sNumVals(par):
    return(1 if par['FROZEN'] else c.Nvals)


def upBound(par):
    if par['FROZEN']:
        return(par['MIN'])
    else:
        return(par['MAX'])

def parValue(par, iter=False):
    if par['METHOD']:
        return(np.logspace(par['MIN'], upBound(par),
            num=sNumVals(par) if iter else c.Nvals))
    else:
        return(np.linspace(par['MIN'], upBound(par),
            num=sNumVals(par) if iter else c.Nvals))


def getColsDict(dist):
    pars = dist.get_pars()
    cols_dict = {
        'NAME': tuple([par['NAME'] for par in pars]),
        'METHOD': [par['METHOD'] for par in pars],
        'INITIAL': [par['MIN'] if par['FROZEN'] \
            else (par['MIN'] + par['MAX']) / 2 for par in pars],
        'DELTA': [c.Pdelta for par in pars],
        'MINIMUM': [par['MIN'] for par in pars],
        'BOTTOM': [par['MIN'] for par in pars],
        'TOP': [par['MAX'] for par in pars],
        'MAXIMUM': [par['MAX'] for par in pars],
        'NUMBVALS': [sNumVals(par) for par in pars],
        'VALUE': [parValue(par) for par in pars],
        'ITERVALUE': [parValue(par, iter=True) for par in pars]
    }
    return(cols_dict)


class PowerLaw:
    def __init__(self, **kwargs):
        self.s = kwargs['s']
        self.glow = kwargs['glow']
        self.ghigh = kwargs['ghigh']

    def __call__(self, gamma, s, *args):
        return gamma**(-s)

    def get_pars(self):
        return((
            self.s,
            self.glow,
            self.ghigh,
        ))

class BrokenPL:

    def __init__(self, **kwargs):
        self.s1 = kwargs['s1']
        self.s2 = kwargs['s2']
        self.gbreak = kwargs['gbreak']
        self.glow = kwargs['glow']
        self.ghigh = kwargs['ghigh']


    def __call__(self, gamma, s1, s2, gbreak, *args):
            if gamma < 10**gbreak:
                return gamma**(-s1)
            else:
                return gamma**(-s2) * gbreak**(s2-s1)

    def get_pars(self):
        return((
            self.s1,
            self.s2,
            self.gbreak,
            self.glow,
            self.ghigh,
        ))


class SmoothBPL:

    def __init__(self, **kwargs):
        self.s1 = kwargs['s1']
        self.s2 = kwargs['s2']
        self.gbreak = kwargs['gbreak']
        self.glow = kwargs['glow']
        self.ghigh = kwargs['ghigh']


    def __call__(self, gamma, s1, s2, gbreak, *args):
        return(
            (gamma)**(-s1) *
            (1 / (1 + (gamma / 10**gbreak)**2))**((s2 - s1) / 2)
        )

    def get_pars(self):
        return((
            self.s1,
            self.s2,
            self.gbreak,
            self.glow,
            self.ghigh,
        ))



class ExpCutoffPL:
    def __init__(self, **kwargs):
        self.s = kwargs['s']
        self.beta = kwargs['beta']
        self.glow = kwargs['glow']
        # We have to integrate on greater interval to take into account cutoff contribution to the spectra
        kwargs['ghigh']['MIN'] += 1
        kwargs['ghigh']['MAX'] += 1
        self.ghigh = kwargs['ghigh']

    def __call__(self, gamma, s, beta, *args):
        return(
            gamma**(-s) *
            np.exp(-(gamma / 10**(args[1] - 1))**beta)
        )

    def get_pars(self):
        return((
            self.s,
            self.beta,
            self.glow,
            self.ghigh,
        ))
