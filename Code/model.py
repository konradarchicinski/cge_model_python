import numpy as np
import pandas as pd
import argparse
from pathlib import Path
from gekko import GEKKO
from pathlib import Path
import os
import csv

class CGE():
    '''
    Computable general equilibrium (CGE) models are a class of economic models that use 
    actual economic data to estimate how an economy might react to changes in policy, 
    technology or other external factors. CGE models are also referred to as AGE 
    (applied general equilibrium) models.

    In this model assumed two factors influancing economy: Capital (K) and Labour (L).

    Model has been written completly in Python.
    '''

    def __init__(self, capital, labour):

        work_dir = str(Path(os.path.realpath(__file__)).parents[1])

        self.Shock = {'K': capital, 'L': labour}

        self.use = pd.read_csv(work_dir + '\\Data\\production_structure.csv', index_col=0)
        self.xdem = pd.read_csv(work_dir + '\\Data\\consumption_structure.csv', index_col=0)
        self.enfac = pd.read_csv(work_dir + '\\Data\\endowment_of_the_household.csv', index_col=0)
        self.taxrev = pd.read_csv(work_dir + '\\Data\\tax_revenue.csv', index_col=0)
        self.trans = pd.read_csv(work_dir + '\\Data\\transfers.csv', index_col=0)
        
        self.factors = self.use.index
        self.sectors = self.use.columns
        self.households = self.xdem.loc[:, self.xdem.columns != 'GOVR'].columns

        self.beta = pd.DataFrame(index=self.factors, columns=self.sectors)
        self.alpha = pd.DataFrame(index=self.xdem.index, columns=self.xdem.columns)
        self.omega = pd.DataFrame(index=self.enfac.index, columns=self.enfac.columns)
        self.B = {}
        self.A = {}
        self.itax = {}
        self.tr_in = {}
        self.tr_out = {}
        self.p  = {}
        self.S = {}
        self.taxK = {}
        self.taxL = {}
        self.PW = {}
        self.W = {}
        self.INC = {}

        self.m = GEKKO(remote=False)

    
    def parameters(self):

        for sec in self.sectors:
            # Parameters of the Cobb Douglas production function
            for fac in self.factors:
                self.beta[sec][fac] = self.m.Const(
                    self.use[sec][fac] 
                    / sum(self.use[sec])
                )
            # For Production
            self.B[sec] = self.m.Const(
                sum(self.use[sec]) 
                / np.prod(
                    [
                        self.use[sec][fac]**(self.use[sec][fac] / sum(self.use[sec])) 
                        for fac in self.factors
                    ]
                )
            )
            self.p[sec] = self.m.Var(lb=0, value=1)
            self.S[sec] = self.m.Var(value=sum(self.use[sec]))
            self.taxK[sec] = self.m.Var(lb=0, value=0)
            self.taxL[sec] = self.m.Var(lb=0, value=0)
                
        for hou in self.xdem.columns:
            # Parameters of the Cobb Dougas utility function
            for sec in self.sectors:
                self.alpha[hou][sec] = self.m.Const(
                    self.xdem[hou][sec] 
                    / sum(self.xdem[hou])
                )
            self.A[hou] = self.m.Const(
                sum(self.xdem[hou]) 
                / np.prod(
                    [
                        self.xdem[hou][sec]**(self.xdem[hou][sec] / sum(self.xdem[hou])) 
                        for sec in self.sectors
                    ]
                )
            )
            
        for hou in self.enfac.index:
            for fac in self.enfac.columns:
            # Endowments of factors
                self.omega[fac][hou] = self.m.Const(
                    self.enfac[fac][hou] * (1 - self.Shock[fac])
                )
            # Income tax rate (Tax revenues / Household gross income)
            self.itax[hou] = self.m.Const(
                self.taxrev[hou]['GOVR'] 
                / np.sum(
                    [
                        self.omega[fac][hou] for fac in self.enfac.columns
                    ]
                )
            )
            # Transfers
            self.tr_in[hou] = self.m.Const(self.trans[hou].sum())
            self.tr_out[hou] = self.m.Const(self.trans.loc[hou].sum())  

        for hou in self.xdem.columns:
            self.PW[hou] = self.m.Var(lb=0, value=1)
            self.W[hou] = self.m.Var(value=sum(self.xdem[hou]))
            self.INC[hou] = self.m.Var(lb=0, value=sum(self.xdem[hou]))

        self.pK = self.m.Var(lb=0, value=1)
        self.pL = self.m.Var(lb=0, value=1)

    
    def equilibrium(self):

        self.parameters()

        self.equations = {
            'PRF_WG': (
                np.prod(
                    [
                        (self.p[sec] / self.alpha['GOVR'][sec])**(self.alpha['GOVR'][sec]) 
                        for sec in self.sectors
                    ]
                ) 
                / self.A['GOVR'] 
                == self.PW['GOVR']
            ),
            'MKT_WG': (
                self.W['GOVR'] * self.PW['GOVR'] 
                == self.INC['GOVR']
            ),
            'I_INCG': (
                np.sum(
                    [
                        (
                            self.pK * self.omega['K'][hou] 
                            + self.pL * self.omega['L'][hou] 
                            + self.tr_in[hou] 
                            - self.tr_out[hou]
                        ) * self.itax[hou] 
                        for hou in self.households
                    ]
                ) 
                + np.sum(
                    [
                        (self.taxK[sec] * self.pK * self.beta[sec]['K'] * self.p[sec] * self.S[sec]) 
                        / (self.pK * (1+self.taxK[sec])) 
                        for sec in self.sectors
                    ]
                ) 
                + np.sum(
                    [
                        (self.taxL[sec] * self.pL * self.beta[sec]['L'] * self.p[sec] * self.S[sec]) 
                        / (self.pL * (1+self.taxL[sec])) 
                        for sec in self.sectors
                    ]
                ) 
                == self.INC['GOVR']
            )
        }

        for sec in self.sectors:
            # Zero profit conditions (P = MC)
            self.equations[f'PRF_{sec}S'] = (
                (
                    (self.pK *(1+self.taxK[sec]) / self.beta[sec]['K'])**(self.beta[sec]['K']) 
                    * (self.pL * (1+self.taxL[sec]) / self.beta[sec]['L'])**(self.beta[sec]['L'])
                ) 
                / self.B[sec] 
                == self.p[sec]
            )
            # Goods markets clearing
            self.equations[f'MKT_{sec}D'] = (
                np.sum(
                    [
                        self.alpha[hou][sec] * self.PW[hou] * self.W[hou] / self.p[sec] 
                        for hou in self.households
                    ]
                ) 
                + self.alpha['GOVR'][sec]*self.W['GOVR']*self.PW['GOVR'] / self.p[sec] 
                == self.S[sec]
            )

        for hou in self.households:
            # Definition of the consumer price index
            self.equations['CPI_' + hou] = (
                np.prod(
                    [
                        (self.p[sec] / self.alpha[hou][sec])**(self.alpha[hou][sec]) 
                        for sec in self.sectors
                    ]
                ) 
                / self.A[hou] 
                == self.PW[hou]
            )
            # Consumer spends everything on consumption
            self.equations['OUTLAY_' + hou] = self.PW[hou] * self.W[hou] == self.INC[hou]
            # Income determination
            self.equations['INC_' + hou] = (
                (
                    self.pK * self.omega['K'][hou] 
                    + self.pL * self.omega['L'][hou] 
                    + self.tr_in[hou] 
                    - self.tr_out[hou]
                ) 
                * (1-self.itax[hou]) 
                == self.INC[hou]
            )

        # Factor market clearing for K and L
        self.equations['MKT_K'] = (
            np.sum(
                [
                    self.beta[sec]['K'] * self.p[sec] * self.S[sec] / (self.pK * (1+self.taxK[sec])) 
                    for sec in self.sectors
                ]
            ) 
            == np.sum(
                [
                    self.omega['K'][hou] 
                    for hou in self.households
                ]
            )
        )

        self.equations['MKT_L'] = (
            np.sum(
                [
                    self.beta[sec]['L'] * self.p[sec] * self.S[sec] / (self.pL * (1+self.taxL[sec])) 
                    for sec in self.sectors
                ]
            ) 
            == np.sum(
                [
                    self.omega['L'][hou] 
                    for hou in self.households
                ]
            )
        )


        self.m.Equations(list(self.equations.values()))
        self.m.options.SOLVER=1
        self.m.solve()

    
    def results(self):

        self.equilibrium()

        solution = {
            'Gov_wealth': self.W['GOVR'].value[0],
            'Gov_PI': self.PW['GOVR'].value[0],
            'Gov_income': self.INC['GOVR'].value[0],
            'K_price': self.pK.value[0],
            'L_price': self.pL.value[0]
        }
        for sec in self.sectors:
            solution[f'{sec}_supply'] = self.S[sec].value[0]
            solution[f'{sec}_price'] = self.p[sec].value[0]
            solution[f'K_{sec}_tax'] = self.taxK[sec].value[0]
            solution[f'L_{sec}_tax'] = self.taxL[sec].value[0]
        for hou in self.households:
            solution[f'{hou}_Wealth'] = self.W[hou].value[0]
            solution[f'{hou}_CPI'] = self.PW[hou].value[0]
            solution[f'{hou}_Income'] = self.INC[hou].value[0]
        
        work_dir = str(Path(os.path.realpath(__file__)).parents[1])
        with open(work_dir + '\\Data\\solution.csv','w') as f:
            w = csv.writer(f)
            w.writerow(solution.keys())
            w.writerow(solution.values())

        return print(solution)
       
        
def main():
    
    parser = argparse.ArgumentParser(
        description='Program forcasting economy changes based on CGE model theory.'
    )
    parser.add_argument(
        "capital", 
        type=float,
        nargs='?', 
        default=0, 
        help="""
        Capital shock variable in range between 0 and 1, 
        corresponding to the percentage decrease in the sector.
        """
    )
    parser.add_argument(
        "labour",  
        type=float,
        nargs='?',
        default=0,
        help="""
        Labour shock variable in range between 0 and 1, 
        corresponding to the percentage decrease in the sector.
        """
    )
    args = parser.parse_args()

    CGE(args.capital, args.labour).results()


if __name__ == "__main__":

    main()
