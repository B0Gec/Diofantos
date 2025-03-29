inputa = """
error: 3.203874099327748e-07   model: 1.999*an_1 - 0.999*an_2 + 1.000*n - 0.000
error: 0.08057339090814337     model: 0.999*an_1 + 1.182*sqrt(n) + 0.514*n**2
error: 9.016581762817749       model: 1.579*an_1 - 0.586*an_3 + 4.0                   
error: 9.318342794960778       model: 2.122*an_1 - 1.128*an_2                         
"""
inputa = """
error: 0.8282648275336897      model: 1.659*an_1 - 0.679*an_3 + 0.138       
error: 0.8822377610961187      model: 1.111*an_1 - 0.348*sqrt(n) + 0.014*n**2
error: 1.0438400775820538      model: 2.011*an_1 - 1.000*an_2 + 0.089*n - 0.673
"""
inputa = """
error: 6.518908073445741       model: 0.703*an_1 + 0.144*an_2 + 0.802*n + 0.428
error: 6.667923798151011       model: 0.843*an_1 + 0.113*n + 0.697*sqrt(n**2)
error: 6.8651100137198275      model: 0.877*an_1 + 2.242*sqrt(n) + 0.007*n**2
"""
inputa = """
error: 100000000               model: 3.137*an_1**2*n**2 + 0.464*an_29*n + 2.708*an_34 - 4.134 - 0.150*exp(-4.708*an_2)
error: 100000000               model: -0.335*sqrt(an_1) - 3.925*an_35 + 0.809*n + 0.442 - 2.581*exp(-4.688*an_1**2*n**2)
error: 100000000               model: -0.670*log(0.831*an_1*n**3) - 1.511*log(-1.239*an_1*an_2*n) - 1.441*log(-2.689*n)/n
"""
inputa = """
error: 0.12588616768006808     model: 0.364*an_1 + 1.030*sqrt(n) + 0.001*n**2
error: 0.12897762911839303     model: 0.209*n*exp(0.009*an_2) + 3.468 - 2.088*exp(-0.010*n**2)
error: 0.1314615092910516      model: 0.375*an_1 + 0.223*an_2 + 0.105*n + 1.193
"""
inputa = """
error: 0.020408962209893834    model: 1.000*an_1 + 1.998*an_2                         
error: 0.10008550924094338     model: 2.956*an_1 - 3.824*an_3 - 0.029    
error: 0.12861693170065824     model: 1.025*an_1 + 1.948*an_2 - 0.015*n + 0.087
error: 0.9913482917708217      model: 3.999*an_2 + 0.043                            
"""
inputa = """
error: 128.21192135532627      model: 0.047*an_2*n/log(0.682*n) + 4.376*sqrt(n**2)
error: 137.06989163559825      model: 0.427*an_1 + 0.606*an_2 + 0.286*n + 4.0
error: 152.10646634079606      model: 0.499*an_1 + 0.578*an_2                       
"""
inputa = """
error: 1.284178938772559       model: 2.129*n*exp(0.001*an_2) - 4.0 + 2.832*exp(-0.076*n**2)
error: 1.4784606228448307      model: -3.683*sqrt(n) + 2.863*n                        
error: 1.5307973905466563      model: 0.497*an_1 + 0.235*an_2 + 0.676*n - 0.153
"""
inputa = """
error: 64.80324710689928       model: 2.325*an_1 - 1.708*an_3 - 0.098    
error: 107.28500870095584      model: 3.074*an_1 - 2.297*an_2 + 0.019*n + 0.070
error: 2459.1580161648585      model: 2.950*an_1 - 2.075*an_2                         
"""
inputa = """
(( error: 0.002525008139111645 )) model: 0.447213595476216*exp(0.481211825060702*n); 
((error: 0.0186240574568429 )) model: 0.951314797243003*an_1 + 1.07877431283495*an_2 - 0.00310220163570429*n + 0.0953345047401255; 
(( error: 0.020412500277747485 )) model: 0.988619898406967*an_1 + 1.01841339117341*an_2;
((error: 0.032870959939031316 )) model: 1.59097225190312*an_1 + 0.0708485468372837*an_3 + 0.0170615581419842; 
((error: 0.0522359393934134 model: 2.61803398873063*an_2 + 0.0365332383250534;  ))
error: 1.9089676365051371 model: -1.21180891207712*an_42 + 0.447213603384122*exp(0.481211824756036*n)  
error: 518.3610146655051 model: -4.88498130835069e-15*an_1*an_13 + 1.61803406429953*an_1 + 1.67075656987579 + 0.597718911020645*exp(-3.11870635317679*n); p: 2.9654522234750696e-09 ; 
"""
# F(n) = round(phi^(n+1)/(phi+2)) 
# a(n+1) = (a(n) + sqrt(4*(-1)^n + 5*(a(n))^2))/2
# F(n) = round(log_2(2^(phi*F(n-1)) + 2^(phi*F(n-2))))
# approx. F(n+1) = sqrt((F(n))^2 - F(n-1)^2)
# approx. F(n+2) = 1/(1/F(n) - 1/F(n+1)) 
# a(n) = 2*a(n-2) + a(n-3), n > 2
# F(n + 3) = 2F(n + 2) - F(n)
# a(n)^2 - a(n-1)^2 = a(n+1)*a(n-2)
# F(n + 4) = 3F(n + 2) - F(n) 
# (F(n+2)*F(n+3)) - (F(n+1)*F(n+4)) + (-1)^n = 0
# F(n) = 4*F(n-3) + F(n-6)
# F(n) = 4*F(n-2) - 2*F(n-3) - F(n-6)
# F(n + 8) = 7F(n + 4) - F(n)
# F(n + 12) = 18F(n + 6) - F(n)
# F(n+10) = 11*F(n+5) + F(n)
# F(n+m+1) = F(n)*F(m) + F(n+1)*F(m+1) 
# F(n) = F(k)*F(n-k+3) - F(k-1)*F(n-k+2) - F(k-2)*F(n-k) + (-1)^k*F(n-2k+2)
# a(n) = 2^(n^2+n) - (4^n-2^n-1)*floor(2^(n^2+n)/(4^n-2^n-1)) - 2^n*floor(2^(n^2) - (2^n-1-1/2^n)*floor(2^(n^2+n)/(4^n-2^n-1)))
#  F(n) = F(n-k+2)*F(k-1) + F(n-k+1)*F(k-2) 
# F(n)^2 - F(n+k)*F(n-k) = (-1)^(n+k) * F(k)^2

inputa = """
error: 9.726250818315227e-11   model: 0.999*an_1 - 1.526*n + 2.526*sqrt(n**2)
error: 1.0575367586859861e-06  model: 0.992*an_1 + 0.007*an_2 + 1.007*n - 0.006
    {-2, -1} => discovered (True)   a_n = a_{n-1} + n
error: 0.017956509951151244    model: -0.570*an_1 + 1.166*sqrt(n) + 0.787*n**2
error: 0.01888161417812767     model: 1.509*an_1 - 0.509*an_3 + 1.271     
error: 0.10072564286290261     model: 2.081*an_1 - 1.083*an_2                         
    {-1} => discovered (True)       a_n = 2*a_{n-1} - a_{n-2} + 1 
                                        = 1+1+2+...+(n-1) + 1+1+2+...+(n-2)+(n-1) - ( 1+1+2+...+(n-2) ) + 1 = 1+1+2+...+n 
error: 0.527759355874446       model: 0.544*an_1*n - 0.547*an_2*n + 3.400*exp(0.069*n)
"""

import re
line = "error: 3.203874099327748e-07   model: 1.999*an_1 - 0.999*an_2 + 1.000*n - 0.000"
def line2ara(line):

    def expo(exp):
        expb = f"* 10^{{{int(exp[2:])}}}"  
        return expb
    # print(expo('e-07'))
    # 1/0
    # def expall(line):
    #     exps = re.findall('e[+-]\d{1,2}', line)
    #     newline = line
    #     for exp in exps:
    #         expb = f"* 10^{{{int(exp[2:])}}}"  
    #         newline = re.sub(exp, expb, newline)
    #     return newline
    # print(expo(line))
    def resub(line: str, restr: str, frepl):
        founds = re.findall(restr, line)
        # print('founds in line:', line, founds)
        newline = line
        for found in founds:
            fond = "".join([f"[{i}]" for i in found])
            # print(fond)
            newline = re.sub(fond, frepl(found), newline)
            # print(newline)
        return newline
    line = resub(line, 'e[+-]\d{1,2}', lambda exp: f"* 10^{{{int(exp[1:])}}}")
    line = resub(line, 'an_\d\d', lambda an: f"a_{{n-{int(an[3:])}}}")
    line = resub(line, 'an_\d', lambda an: f"a_{{n-{int(an[3:])}}}")
    line = resub(line, '\*\*\d{1,2}', lambda power: f"^{power[2:]}")
    line = resub(line, '\d\.999', lambda num: f"{int(num[0])+1}.0")
    line = resub(line, '\d\.000', lambda num: f"{int(num[0])}.0")
    line = resub(line, '100000000', lambda num: "10^8")
    line = resub(line, '1000000000.0', lambda num: "10^9")
    line = resub(line, ';', lambda num: f"")

    #  flip sides:
    error = re.findall('error:(.+)model:(.+)', line)
    line = error[0][1] + ' &&& ' + error[0][0] + '\\\\'

    # def an(an_1):
    #     an_1 = re.findall('an_\d{1,2}', an_1)
    #     a_n1 = f"a_{{n-{int(an_1[0][3:])}}}"  
    #     return a_n1
    # # print(an(line))
    # sti = re.sub('model:', '', re.sub('error:', '', line))
    return line
# arline(line)
# print(line2ara(line))

lines = re.findall('(.+)\n', inputa)
for line in lines:
    # print(line)
    print('a_n = ', line2ara(line))


# linea = lines[1]
# print(line2ara(linea))

# print(linea)
# fond = "".join([f"[{i}]" for i in "**2"])
# print(fond)
# print(re.findall('aa\d{1,2}', 'aaa1'))
# print(re.findall(fond, '***2'))
# newline = re.sub(r"[*][2]", f"^2", '****2')
# print(newline)


