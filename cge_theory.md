# Utility function
CES utility function may be expressed as follows: 

$U(x_1,x_2...x_n) = A\cdot(\sum_{i=1}^{n} a_i^{\frac{1}{\sigma}} x_i^{\frac{\sigma-1}{\sigma}})^{\frac{\sigma}{\sigma-1}}$

Where parameter $a_i \in (0,1)$ is responsible for ... , $A$ is and ... , $\sigma$ is the elasticity of substitution between each good represented by a $x_i$ variables.


# Production function
CES production function may be expressed as follows:
 
$Q(K_t,L_t) = B\cdot(b_K^{\frac{1}{\gamma}} K_t^{\frac{\gamma-1}{\gamma}} + b_L^{\frac{1}{\gamma}}L_t^{\frac{\gamma-1}{\gamma}})^{\frac{\gamma}{\gamma-1}}$

Where parameter $b_i \in (0,1)$ is responsible for the intensity in production, $B$ is and efficiency parameter or in others words factor productivity, $\gamma$ is the elasticity of substitution between capital $K$ and labor $L$.


# Calibration of parameters from exogenous variables (utility and production functions)
Utility function:
- $\sigma$ is obtained from econometric method, literature or conjecture.
- $a_i$ is determined as: $a_i = (\frac{p_i x_i^{\frac{1}{\sigma}}}{\sum_{i=1}^{n}p_i x_i^{\frac{1}{\sigma}}})^{\sigma}$
- $A$ is just $A = \frac{U(x_1,x_2...x_n)}{(\sum_{i=1}^{n} a_i^{\frac{1}{\sigma}} x_i^{\frac{\sigma-1}{\sigma}})^{\frac{\sigma}{\sigma-1}}}$

Production function:
- $\gamma$ is obtained from econometric method, literature or conjecture.
- $b_K$ and $b_L$ is determined as: $b_K = (\frac{w_K K^{\frac{1}{\gamma}}}{w_K K^{\frac{1}{\gamma}} \cdot w_L L^{\frac{1}{\gamma}}})^{\gamma}\quad and \quad b_L = (\frac{w_L L^{\frac{1}{\gamma}}}{w_K K^{\frac{1}{\gamma}} \cdot w_L L^{\frac{1}{\gamma}}})^{\gamma}$
- $B$ is just $B = \frac{Q(K_t,L_t)}{(b_K^{\frac{1}{\gamma}} K_t^{\frac{\gamma-1}{\gamma}} + b_L^{\frac{1}{\gamma}}L_t^{\frac{\gamma-1}{\gamma}})^{\frac{\gamma}{\gamma-1}}}$

