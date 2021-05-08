class fm():
    def check_uniq(self, df, l):
        return df.groupby(l).size()[lambda s: s > 1]

    def __init__(self, df, i=None, t=None, formula=None, nw=None):
        self.i = i
        self.t = t
        self.df = df.sort_values([i, t])
        self.formula = formula
        self.nw = nw
        assert len(self.check_uniq(df, [i, t])) == 0, 'Data is not Panel !'

        ts = sorted(df[t].unique())
        betas = []
        for x in ts:
            betas.append(ols(formula, df[df[t] == x]).fit().params)
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
