import pandas as pd
from statsmodels.api import OLS, WLS
from statsmodels.formula.api import ols
from urllib.request import urlretrieve
from zipfile import ZipFile


class fm():
    def check_uniq(self, df, l):
        return df.groupby(l).size()[lambda s: s > 1]

    def __init__(self, df, i, t, formula, nw=None, weights=None):
        self.i = i
        self.t = t
        self.df = df.sort_values([i, t])
        self.formula = formula
        self.nw = nw
        self.weights = weights
        assert len(self.check_uniq(df, [i, t])) == 0, 'Data is not Panel !'

        ts = sorted(df[t].unique())
        betas = []
        self.rsquared = list()
        self.nobs = list()
        for x in ts:
            sample = df[df[t] == x]
            res = ols(formula, sample).fit()
            betas.append(res.params)

            self.rsquared.append(res.rsquared)
            self.nobs.append(res.nobs)
        self.rsquared = sum(self.rsquared) / len(self.rsquared)
        self.nobs = sum(self.nobs)

        self.params = dict()
        self.tvalues = dict()
        for v in formula.split('~')[1].split('+'):
            v = v.strip()
            if 'C(' in v:  # No dummies
                continue
            if v == '1':  # No intercept
                continue
            beta_df = pd.DataFrame([b[v] for b in betas if v in b],
                                   columns=['var'])
            if nw:
                res = ols('var ~ 1', beta_df).fit(cov_type='HAC',
                                                  cov_kwds={'maxlags': nw})
            else:
                res = ols('var ~ 1', beta_df).fit()
            self.params[v] = res.params['Intercept']
            self.tvalues[v] = res.tvalues['Intercept']


def downloader():
    urlretrieve(
        'http://global-q.org/uploads/1/2/2/6/122679606/q5_factors_monthly_2020.csv',
        'q5.csv')

    urlretrieve(
        'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip',
        'ff3.csv.zip')
    urlretrieve(
        'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip',
        'ff5.csv.zip')
    with ZipFile('ff3.csv.zip') as f:
        f.extractall()

    with ZipFile('ff5.csv.zip') as f:
        f.extractall()
