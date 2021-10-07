from statsmodels.api import OLS

class adjust():
    def regs(self, per):
        a = self.df[self.df.permno == per]
        if len(a) < 100:
            return None, None
        res = OLS(a['ret'], a[self.factors], hasconst=True).fit()
        return res.params, per

    def __init__(self, name, factor_df, factors, rf='RF'):
        self.name = name
        self.df = msf.merge(factor_df).dropna()
        self.df['ret'] = self.df['ret'] * 100 - self.df[rf]
        self.factors = factors

        params = dict()

        with Pool() as p:
            for pa, per in p.imap(self.regs,
                                  msf.permno.unique(),
                                  chunksize=100):
                if per:
                    params[per] = pa

        beta = pd.DataFrame.from_dict(params).T.reset_index()
        beta.columns = ['permno'] + ['beta' + x for x in self.factors]
        self.df = self.df.merge(beta)
        self.df['ret_' + self.name] = self.df['ret']
        for b, x in zip(['beta' + x for x in self.factors], self.factors):
            self.df['ret_' +
                    self.name] = self.df['ret_' +
                                         self.name] - self.df[b] * self.df[x]


ff3_df = adjust('ff3', ff3, ['Mkt-RF', 'SMB', 'HML'], rf='RF')
ff5_df = adjust('ff5', ff5, ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA'], rf='RF')

ff3_df.to_csv('ff3_ret.csv')
ff5_df.to_csv('ff5_ret.csv')
ff3_df.to_csv('ff3_ret')
