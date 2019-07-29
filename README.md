# sync-model

A program for synchrotron spectra modelling and table-model
creating for XSPEC.

## Instalation

1. Download the repository to your computer.

2. Install all required packages: `numpy`, `scipy`, `pandas`, `progressbar2`.

## Usage

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

### Electron distribution choosing
In the current version, you have to choose electron distribution in file `main.py` by uncommenting. Here's an example of `SmoothBPL` distribution choosing:
```
##########CHOOSE ELECTRON DISTRIBUTION HERE(by uncommenting)###########
# dist = Powerlaw(
#     elec = c.elec1,
#     glow = c.glow,
#     ghigh = c.ghigh,
# )
dist = SmoothBPL(
   elec1 = c.elec1,
   elec2 = c.elec2,
   gbreak = c.gbreak,
   glow = c.glow,
   ghigh = c.ghigh,
)
#dist = Expcutoff(
#    elec = c.elec1,
#    beta = c.beta,
#    glow = c.glow,
#    ghigh = c.ghigh,
)
#######################################################################
```


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
