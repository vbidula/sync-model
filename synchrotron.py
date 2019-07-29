from scipy.special import kv
import constants as c
import numpy as np
import scipy.integrate as integrate
import progressbar
import copy
import multiprocessing as mp
from models import getColsDict


class Synchrotron():

    def __init__(self, dist, usebar=True):
        self.dist = dist
        self.usebar = usebar

    @staticmethod
    def Rfunc_old(x):
        return(x**2 / 2 * kv(4 / 3, x / 2) * kv(1 / 3, x / 2)
               - 0.3 * x**3 / 2 * (kv(4 / 3, x / 2)**2 - kv(1 / 3, x / 2)**2))

    @staticmethod
    def Rfunc(x):
        return(
            1.808 * x**(1 / 3) / (1 + 3.4*x**(2/3))**(1/2)
            * (1 + 2.21 * x**(2 / 3) + 0.347 * x**(4 / 3))
            / (1 + 1.353 * x**(2 / 3) + 0.217 * x**(4 / 3))
            * np.exp(-x)
        )

    def Psync(self, nu, gamma):
        # assert gamma >= 1, ("Gamma factor shoul be greater than one.")
        '''
        nu - array like of floats
        gamma - float greater of equal 1
        '''
        nu_c = (3 * c.B * c.e) / (4 * c.pi * c.m_e * c.c) * gamma**2
        # const = 3**(1 / 2) * e**3 * B / m_e / c**2 #We don't need it, just normalization
        return(self.Rfunc(nu / nu_c))

    def get_int_func(self, nu, dist_pars):
        def int_func(gamma):
            return self.Psync(nu, gamma) * self.dist(gamma, *dist_pars)
        return int_func

    def integrate_Sync(self, nu, parset, sep=None):
        '''
        nu - array like of floats
        gmin, gmax - powers of limit values
        '''
        res = []
        if sep == 1 or sep == None:
            for i in range(0, len(nu)):
                res.append(
                    integrate.quad(
                        self.get_int_func(nu[i], parset),
                        10**parset[-2],
                        10**parset[-1],
                        limit=1000,
                    )[0]
                )

        elif sep > 1:
            gbounds = np.linspace(parset[-2], parset[-1], sep)
            for i in range(0, len(nu)):
                sum = 0.0
                for j in range(0, len(gbounds) - 1):
                    sum += integrate.quad(
                        self.get_int_func(nu[i], parset),
                        10**gbounds[j],
                        10**gbounds[j + 1],
                        limit=1000)[0]
                res.append(sum)

        return(res)

    def genTable(self,  nu, sep=None):
        pars = getColsDict(self.dist)['ITERVALUE']
        # glow and ghigh must be always at the end of pars
        npars = len(pars) - 2
        curset = [0 for i in range(len(pars))]
        parsets = []
        spectra = []
        nstart = 0

        if self.usebar:
            max_val = np.sum([bool(par[-1] - par[0]) for par in pars])
            with progressbar.ProgressBar(max_value=c.Nvals**max_val) as bar:
                print("{} distribution integration have started."
                      .format(self.dist.__class__.__name__))
                print("Number of created processes: ", c.Nproc)
                self.recSync(nu, pars, nstart, npars, curset,
                             parsets, spectra, sep=sep, bar=bar)
        else:
            self.recSync(nu, pars, nstart, npars, curset,
                         parsets, spectra, sep=sep)

        return({
            'PARAMVAL': parsets,
            'INTPSPEC': spectra,
        })

    def recSync(self, nu, pars, n, npars, curset, parsets, spectra, sep, bar=None):
        if n < npars:
            for value in pars[n]:
                curset[n] = value
                self.recSync(nu, pars, n + 1, npars, curset,
                             parsets, spectra, sep, bar)
        else:
            for glow in pars[-2]:
                curset[-2] = glow
                for ghigh in pars[-1]:
                    curset[-1] = ghigh
                    parsets.append(copy.copy(curset))
                    spectra.append(
                        self.integrate_Sync(nu, curset, sep=sep)
                    )
                    if self.usebar:
                        bar.update(len(parsets))
