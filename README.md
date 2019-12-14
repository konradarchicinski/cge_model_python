# CGE modelling in Python

Welcome to our GitHub repository in which we store the core of CGE model written completely in Python language.
We are students from Faculty of Economic Science, University of Warsaw. The above model was the part of final project for one of our courses during studies.

## Description of CGE models

Computable general equilibrium (CGE) models are a class of economic models that use actual economic data to estimate how an economy might react to changes in policy, technology or other external factors. CGE models are also referred to as AGE (applied general equilibrium) models.

A CGE model consists of equations describing model variables and a database (usually very detailed) consistent with these model equations. The equations tend to be neo-classical in spirit, often assuming cost-minimizing behaviour by producers, average-cost pricing, and household demands based on optimizing behaviour. However, most CGE models conform only loosely to the theoretical general equilibrium paradigm. For example, they may allow for:
- non-market clearing, especially for labour (unemployment) or for commodities (inventories)
- imperfect competition (e.g., monopoly pricing)
- demands not influenced by price (e.g., government demands)

A CGE model database consists of:
- tables of transaction values, showing, for example, the value of coal used by the iron industry. Usually the database is presented as an input-output table or as a social accounting matrix (SAM). In either case, it covers the whole economy of a country (or even the whole world, and distinguishes a number of sectors, commodities, primary factors and perhaps types of household. Sectoral coverage ranges from relatively simple representations of capital, labor and intermediates to highly-detailed representations of specific sub-sectors (e.g., the electricity sector in GTAP-Power).
- elasticities: dimensionless parameters that capture behavioural response. For example, export demand elasticities specify by how much export volumes might fall if export prices went up. Other elasticities may belong to the constant elasticity of substitution class. Amongst these are Armington elasticities, which show whether products of different countries are close substitutes, and elasticities measuring how easily inputs to production may be substituted for one another. Income elasticity of demand shows how household demands respond to income changes.

_Source: https://en.wikipedia.org/wiki/Computable_general_equilibrium_