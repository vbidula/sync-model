# sync-model

A program for synchrotron spectra modelling focused on table-model
creating for XSPEC.

## Instalation

1. Download the repository to your computer.

2. Install all required packages: `numpy`, `scipy`, `pandas`, `progressbar2`.

## Usage

### Electron distribution choosing
You have to choose electron distribution in the variable `DIST`. Here's the list of all currently possible distributions:
1. `'powerlaw'`:  
  ![equation](https://latex.codecogs.com/gif.latex?\frac{dN_e}{dt}&space;=&space;\gamma^{-s})


### Parameters specifying
All settings are in file `constants.py`. Parameters for distributions have 5 options:
```
beta = {
'NAME': 'beta',
'MIN': 0.5,
'MAX': 1.5,
'FROZEN': True,
'METHOD': 0,
}
```
1. `'NAME'`(string) - name that will be used by XSPEC.

2. `'MIN'`, `'MAX'`(float) - minimum and maximum values for the tabulated parameter.
(in other words, the parameter will be changing from `'MIN'` to `'MAX'`).

3. `'FROZEN'`(boolean) - option to prevent parameter changing. If `True` - the `'MIN'` value will be used.

4. `'METHOD'`(int) - method of parameter interpolation in XSPEC. `0` for linear, `1` for logarithmic.

You have to specify parameters only for particular electron distribution, for example, `Powerlaw` distribution doesn't need parameter 'beta' to be specified.

You can also define range for energy axis in `Escale`, `Emin`, `Emax`, `Epoints`:
- `Escale` - Scale of energy axis. Possible values: `'log'`, `'lin'`. If `Escale = 'log'` then `Emin`, `Emax` - powers of ten.
- `Emin`, `Emax` - upper and lower limits.
- `Epoints` - array length of energy axis. This value should not be lower than number of channels in your data.

Other parameters:
- `Nsep` - number of subintervals for integration. More precisely integration but takes much more time. In most of cases `Nsep = 5` is enough.
- `Nvals` - number of tabulated values for each parameter. For example if parameter `beta` changes from `'MIN' = 0.5` to `'MAX' = 1.5` and `Nvals = 5` then in generated table the parameter will be taking values `0.5, 0.75, 1.0, 1.25, 1.5`. (in other words `Nvals` is a _level of discretization_ of parameter)
- `Pdelta` - Parameter delta used in fit (parameter determination precision)
- `Nproc` - The number of parallel processes to be started for table generating. Do not specify this number greater than the number of available logical processors.
- `TableName` - name of the table that will be generated.


### Running
To start the program simply run:
```
python main.py
```
or
```
python3 main.py
```
in terminal.
