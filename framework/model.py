import numpy as np
import pandas as pd
from gekko import GEKKO
m = GEKKO()

Shock = {'K':0, 'L':0.9}

factors = use.index
sectors = use.columns
households = xdem.loc[:, xdem.columns != 'GOVR'].columns

beta = pd.DataFrame(index=factors, columns=sectors)
alpha = pd.DataFrame(index=xdem.index, columns=xdem.columns)
omega = pd.DataFrame(index=enfac.index, columns=enfac.columns)
B, A, itax, tr_in, tr_out, p, S, taxK, taxL, PW, W, INC = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}


###############################################################################################################################


for sec in sectors:
    # Parameters of the Cobb Douglas production function
    for fac in factors:
        beta[sec][fac] = m.Const(use[sec][fac] / sum(use[sec]))
    # For Production
    B[sec] = m.Const(sum(use[sec]) / (np.prod([use[sec][fac]**(use[sec][fac] / sum(use[sec])) for fac in factors])))
    p[sec] = m.Var(lb=0, value=1)
    S[sec] = m.Var(value=sum(use[sec]))
    taxK[sec] = m.Var(value=0)
    taxL[sec] = m.Var(value=0)
        
for hou in xdem.columns:
    # Parameters of the Cobb Dougas utility function
    for sec in sectors:
        alpha[hou][sec] = m.Const(xdem[hou][sec] / sum(xdem[hou]))
    A[hou] = m.Const(sum(xdem[hou]) / np.prod([xdem[hou][sec]**(xdem[hou][sec] / sum(xdem[hou])) for sec in sectors]))
    
for hou in enfac.index:
    for fac in enfac.columns:
    # Endowments of factors
        omega[fac][hou] = m.Const(enfac[fac][hou] * (1 - Shock[fac]))
    # Income tax rate (Tax revenues / Household gross income)
    itax[hou] = m.Const(taxrev[hou]['GOVR'] / (np.sum([omega[fac][hou] for fac in enfac.columns])))
    # Transfers
    tr_in[hou] = m.Const(trans[hou].sum())
    tr_out[hou] = m.Const(trans.loc[hou].sum())  

for hou in xdem.columns:
    PW[hou] = m.Var(lb=0, value=1)
    W[hou] = m.Var(value=sum(xdem[hou]))
    INC[hou] = m.Var(lb=0, value=sum(xdem[hou]))

pK = m.Var(lb=0, value=1)
pL = m.Var(lb=0, value=1)

    
###############################################################################################################################


equations = {
    'PRF_WG': np.prod([(p[sec] / alpha['GOVR'][sec])**(alpha['GOVR'][sec]) for sec in sectors]) / A['GOVR'] == PW['GOVR'],
    'MKT_WG': W['GOVR'] * PW['GOVR'] == INC['GOVR'],
    'I_INCG': np.sum([(pK * omega['K'][hou] + pL * omega['L'][hou] + tr_in[hou] - tr_out[hou]) * itax[hou] for hou in households]) + np.sum([(taxK[sec] * pK * beta[sec]['K'] * p[sec] * S[sec]) / (pK * (1+taxK[sec])) for sec in sectors]) + np.sum([(taxL[sec] * pL * beta[sec]['L'] * p[sec] * S[sec]) / (pL * (1+taxL[sec])) for sec in sectors]) == INC['GOVR']
}

for sec in sectors:
    # Zero profit conditions (P = MC)
    equations[f'PRF_{sec}S'] = ((pK *(1+taxK[sec]) / beta[sec]['K'])**(beta[sec]['K']) * (pL * (1+taxL[sec]) / beta[sec]['L'])**(beta[sec]['L'])) / B[sec] == p[sec]
    # Goods markets clearing
    equations[f'MKT_{sec}D'] = np.sum([(alpha[hou][sec] * PW[hou] * W[hou]) / p[sec] for hou in households]) + (alpha['GOVR'][sec]*W['GOVR']*PW['GOVR']) / p[sec] == S[sec]

for hou in households:
    # Definition of the consumer price index
    equations['CPI_' + hou] = np.prod([(p[sec] / alpha[hou][sec])**(alpha[hou][sec]) for sec in sectors]) / A[hou] == PW[hou]
    # Consumer spends everything on consumption
    equations['OUTLAY_' + hou] = PW[hou] * W[hou] == INC[hou]
    # Income determination
    equations['INC_' + hou] = (pK * omega['K'][hou] + pL * omega['L'][hou] + tr_in[hou] - tr_out[hou]) * (1-itax[hou]) == INC[hou]

# Factor market clearing for K and L
equations['MKT_K'] = np.sum([(beta[sec]['K'] * p[sec] * S[sec]) / (pK * (1+taxK[sec])) for sec in sectors]) == np.sum([omega['K'][hou] for hou in households])

equations['MKT_L'] = np.sum([(beta[sec]['L'] * p[sec] * S[sec]) / (pL * (1+taxL[sec])) for sec in sectors]) == np.sum([omega['L'][hou] for hou in households])


m.Equations(list(equations.values()))
m.options.SOLVER=1
m.solve()


###############################################################################################################################


solution = (
    'Solutions:\n' +
    '------------------------------\n' +
    '%-12s%6s%12.3f\n' % ('Gov wealth', '|', W['GOVR'].value[0]) +
    '%-12s%6s%12.3f\n' % ('Gov PI', '|', PW['GOVR'].value[0]) +
    '%-12s%6s%12.3f\n' % ('Gov income', '|', INC['GOVR'].value[0]) +
    '------------------------------\n' +
    '%-12s%6s%12.3f\n' % ('K price', '|', pK.value[0]) +
    '%-12s%6s%12.3f\n' % ('L price', '|', pL.value[0]) +
    '------------------------------\n'
)   
for sec in sectors:
    solution += '%-12s%6s%12.3f\n' % (f'{sec} supply', '|', S[sec].value[0])
    solution += '%-12s%6s%12.3f\n' % (f'{sec} price', '|', p[sec].value[0])
    solution += '%-12s%6s%12.3f\n' % (f'K {sec} tax', '|', taxK[sec].value[0])
    solution += '%-12s%6s%12.3f\n' % (f'L {sec} tax', '|', taxL[sec].value[0])
solution += '------------------------------\n'
for hou in households:
    solution += '%-12s%6s%12.3f\n' % (hou + ' Wealth', '|', W[hou].value[0])
    solution += '%-12s%6s%12.3f\n' % (hou + ' CPI', '|', PW[hou].value[0])
    solution += '%-12s%6s%12.3f\n' % (hou + ' Income', '|', INC[hou].value[0])
print(solution)