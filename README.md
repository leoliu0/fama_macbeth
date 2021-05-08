# fama_macbeth
A Python implementation of cross-sectional Fama Macbeth Regression with Newey-West Standard Error

## Usage
get the famamacbeth.py and

```python
from famamacbeth import fm

res = fm(df,i,t,formula,nw)

```
It takes five arguments. df is stock-date panel. i is the variable name for stock (e.g. permno) and t is the name for date variable. formula is statsmodel formula, for example,

```python
formula = "ret ~ 1 + mkt + smb + hml"
```

nw is the number of newey-west lags you would like to include (omit nw to estimate without nw).

After calculation, the results can be seen from params.

```python
res.params # contains estimates for your factor(s).
res.tvalues # contains test statistics for your factor(s).
```

The implementation is rather naive. Feel to open an issue if you would like more functionalities. Ideally when it gets mature I can push it to PyPi.
