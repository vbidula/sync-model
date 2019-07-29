from astropy.io import fits
import constants as c
import os

# import imageio  #for nickname, can be removed
# im = imageio.imread('nickname.png')


class TableModel:

    def __init__(self, pars, energy, spectra, nintpars=0):
        '''
        pars, energy, spectra - dictionaries with keys corresponding to tables
            column names.
        '''
        self.nintpars = nintpars

        self.hdul = fits.HDUList()
        #--- HDU list creating  and main header specifying ---#
        self.hdul.append(fits.ImageHDU())
        self.hdul[0].header['HDUCLASS'] = 'OGIP'
        self.hdul[0].header['HDUCLAS1'] = 'XSPEC TABLE MODEL'
        self.hdul[0].header['HDUVERS'] = '1.0.0'
        self.hdul[0].header['MODLNAME'] = 'sync'
        self.hdul[0].header['MODLUNIT'] = 'ph sm-2 s-1'
        self.hdul[0].header['REDSHIFT'] = False
        self.hdul[0].header['ADDMODEL'] = True
        #--- PARAMETERS table creating ---#
        self.hdul.append(
            fits.BinTableHDU.from_columns(
                self.parColDefs(pars), name='PARAMETERS'
                )
            )
        self.hdul[1].header['HDUCLASS'] = 'OGIP'
        self.hdul[1].header['HDUCLAS1'] = 'XSPEC TABLE MODEL'
        self.hdul[1].header['HDUCLAS2'] = 'PARAMETERS'
        self.hdul[1].header['HDUVERS'] = '1.0.0'
        self.hdul[1].header['NINTPARM'] = self.nintpars
        self.hdul[1].header['NADDPARM'] = 0
        #--- ENERGIES table creating ---#
        self.hdul.append(
            fits.BinTableHDU.from_columns(
                self.enColDefs(energy), name='ENERGIES'
                )
            )
        self.hdul[2].header['HDUCLASS'] = 'OGIP'
        self.hdul[2].header['HDUCLAS1'] = 'XSPEC TABLE MODEL'
        self.hdul[2].header['HDUCLAS2'] = 'ENERGIES'
        self.hdul[2].header['HDUVERS'] = '1.0.0'
        #--- SPECTRA table creating ---#
        self.hdul.append(
            fits.BinTableHDU.from_columns(
                self.specColDefs(spectra), name='SPECTRA'
                )
            )
        self.hdul[3].header['HDUCLASS'] = 'OGIP'
        self.hdul[3].header['HDUCLAS1'] = 'XSPEC TABLE MODEL'
        self.hdul[3].header['HDUCLAS2'] = 'MODEL SPECTRA'
        self.hdul[3].header['HDUVERS'] = '1.0.0'

    @staticmethod
    def parColDefs(pars):
        return((
            fits.Column(
                name='NAME',
                format='12A',
                array=pars['NAME'],
            ),
            fits.Column(
                name='METHOD',
                format='J',
                array=pars['METHOD'],
            ),
            fits.Column(
                name='INITIAL',
                format='E',
                array=pars['INITIAL'],
            ),
            fits.Column(
                name='DELTA',
                format='E',
                array=pars['DELTA'],
            ),
            fits.Column(
                name='MINIMUM',
                format='E',
                array=pars['MINIMUM'],
            ),
            fits.Column(
                name='BOTTOM',
                format='E',
                array=pars['BOTTOM'],
            ),
            fits.Column(
                name='TOP',
                format='E',
                array=pars['TOP'],
            ),
            fits.Column(
                name='MAXIMUM',
                format='E',
                array=pars['MAXIMUM'],
            ),
            fits.Column(
                name='NUMBVALS',
                format='J',
                array=pars['NUMBVALS'],
            ),
            fits.Column(
                name='VALUE',
                format=str(c.Nvals) + 'E',
                array=pars['VALUE'],
            ),
        ))

    @staticmethod
    def enColDefs(energy):
        return((
            fits.Column(
                name='ENERG_LO',
                format='E',
                array=energy['ENERG_LO'],
            ),
            fits.Column(
                name='ENERG_HI',
                format='E',
                array=energy['ENERG_HI'],
            ),
        ))

    def specColDefs(self, spectra):
        return((
            fits.Column(
                name='PARAMVAL',
                format=str(self.nintpars)+'E',
                array=spectra['PARAMVAL'],
            ),
            fits.Column(
                name='INTPSPEC',
                format=str(c.Epoints)+'E',
                array=spectra['INTPSPEC'],
                unit='ph cm-2 s-1',
            ),
        ))

    def save_to(self, name='new_table.fits'):
        try:
            os.remove(name)
            self.hdul.writeto(name)
        except FileNotFoundError:
            self.hdul.writeto(name)
