# sync-model

A program for synchrotron spectra modelling focused on table-model
creating for XSPEC.

## Instalation

1. Download the repository to your computer.

2. Run
```
make
```
from the project directory to compile the libraries required by main program.

3. Install all required packages: `numpy`, `scipy`, `pandas`, `progressbar2`.

## Usage

### Electron distribution choosing
There are 4 models for electron distribution available. It may be specified in the variable `DIST`. Here's the list of all currently possible distributions:

1. `'powerlaw'`:    
      ![equation](https://render.githubusercontent.com/render/math?math=\frac{dN_e}{dt}=\gamma^{-s})

2. `'brokenpl'`:    
      ![equation](https://render.githubusercontent.com/render/math?math=\frac{dN_e}{dt}=\gamma^{-s_1},\text{%20if%20}\gamma\textless\gamma_{br})  
      ![equation](https://render.githubusercontent.com/render/math?math=\frac{dN_e}{dt}=\gamma^{-s_2}\cdot\gamma^{s_2-s_1}_{br},\text{%20if%20}\gamma\textgreater\gamma_{br})

3. `'smoothbrokenpl'`:    
      ![equation](https://render.githubusercontent.com/render/math?math=\frac{dN_e}{dt}=\gamma^{-s_1}\Big(\frac{1}{1%2B(\frac{\gamma}{\gamma_{br}})^2}\Big)^{\frac{s_2-s_1}{2}})

4. `'expcutoff'`:    
      ![equation](https://render.githubusercontent.com/render/math?math=\frac{dN_e}{dt}=\gamma^{-s_1}e^{-(\frac{\gamma}{\gamma_{br}})^\beta})

### Parameters specifying
Other settings may be modified in the file `constants.py`. All distributions are described by five parameters:
```
beta = {
'NAME': 'beta',
'MIN': 0.5,
'MAX': 1.5,
'FROZEN': True,
'METHOD': 0,
}
```
1. `'NAME'`(string) - a name which will be used by XSPEC.

2. `'MIN'`, `'MAX'`(float) - minimum and maximum values for the tabulated parameter.
(in other words, the parameter will be changing from `'MIN'` to `'MAX'`).

3. `'FROZEN'`(boolean) - option to prevent parameter changing. If `True` - the `'MIN'` value will be used.

4. `'METHOD'`(int) - method of parameter interpolation in XSPEC. `0` for linear, `1` for logarithmic.

Only parameters for particular electron distribution have to be specified. For instance, `Powerlaw` distribution doesn't need parameter 'beta' to be specified.

There is also a possibility to define a range for energy axis in `Escale`, `Emin`, `Emax`, `Epoints`:
- `Escale` - Scale of energy axis. Possible values: `'log'`, `'lin'`. If `Escale = 'log'` then `Emin`, `Emax` - powers of 10.
- `Emin`, `Emax` - upper and lower limits.
- `Epoints` - array length of energy axis. This value should not be lower than a number of channels in your data.

Other parameters:
- `Nsep` - number of subintervals for integration. More precisely integration but takes much more time. In most of cases `Nsep = 5` is enough.
- `Nvals` - number of tabulated values for each parameter. For example if parameter `beta` changes from `'MIN' = 0.5` to `'MAX' = 1.5` and `Nvals = 5` then in generated table the parameter will be taking values `0.5, 0.75, 1.0, 1.25, 1.5`. (in other words `Nvals` is a _level of discretization_ of parameter)
- `Pdelta` - Parameter delta used in fit (parameter determination precision)
- `Nproc` - The number of parallel processes to be started for table generating. Do not specify this number greater than the number of available logical processors.
- `TableName` - name of the table that will be generated.


### Running
To start the program simply run:
```
python3 main.py
```
in terminal.
