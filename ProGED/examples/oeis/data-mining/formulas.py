import pandas as pd


dicti = {
'A000009': [
        'Expansion of Product_{m >= 1} (1 + x^m)',
        'no disco?',
    'unknown defining formula',  
'+) Asymptotics: a(n) ~ exp(Pi l_n / sqrt(3)) / ( 4 3^(1/4) l_n^(3/2) ) where l_n = (n-1/24)^(1/2) (Ayoub)',
'a(n) = P(n) - P(n-2) - P(n-4) + P(n-10) + P(n-14) + ... + (-1)^m P(n-2p_m) + ..., where P(n) is the partition function (A000041) and p_m = m(3m-1)/2 is the m-th generalized pentagonal number (A001318). - Jerome Malenfant, Feb 16 2011',
' More precise asymptotics: a(n) ~ exp(Pi*sqrt((n-1/24)/3)) / (4*3^(1/4)*(n-1/24)^(3/4)) * (1 + (Pi^2-27)/(24*Pi*sqrt(3*(n-1/24))) + (Pi^4-270*Pi^2-1215)/(3456*Pi^2*(n-1/24))). - Vaclav Kotesovec, Nov 30 2015',
' a(n) ~ exp(Pi*sqrt(n/3))/(4*3^(1/4)*n^(3/4)) * (1 + (Pi/(48*sqrt(3)) - (3*sqrt(3))/(8*Pi))/sqrt(n) + (Pi^2/13824 - 5/128 - 45/(128*Pi^2))/n)',
' a(n) ~ exp(Pi*sqrt(n/3) + (Pi/(48*sqrt(3)) - 3*sqrt(3)/(8*Pi))/sqrt(n) - (1/32 + 9/(16*Pi^2))/n) / (4*3^(1/4)*n^(3/4))',
],

'A000040': [ 
        'the Primes', 
        'no disco.?',
' a(n) ~ n * log n ',
'a(n) = n log n + n log log n + (n/log n)*(log log n - log n - 2) + O( n (log log n)^2/ (log n)^2)',
'For n = 1..15, a(n) = p + abs(p-3/2) + 1/2, where p = m + int((m-3)/2), and m = n + int((n-2)/8) + int((n-4)/8). - Timothy Hopper, Oct 23 2010',
],

'A000045': [ 
    ' fibonacci',
    'disco yes',
'F(n) = F(n-1) + F(n-2)',
'F(n) = round(phi^n/sqrt(5))',
'F(n) = round(phi^(n+1)/(phi+2)). - Thomas Ordowski, Apr 20 2012', 
'F(n) = ((1+sqrt(5))^n - (1-sqrt(5))^n)/(2^n*sqrt(5)), ', 
'F(n) ~ phi*F(n-1)', 
'a(n+1) = (a(n) + sqrt(4*(-1)^n + 5*(a(n))^2))/2;', 
'F(n) = round(log_2(2^(phi*F(n-1)) + 2^(phi*F(n-2)))), ', 
'approx. F(n+1) = sqrt((F(n))^2 - F(n-1)^2)', 
'approx. F(n+2) = 1/(1/F(n) - 1/F(n+1)) ', 
'a(n) = 2*a(n-2) + a(n-3), n > 2. - Gary Detlefs, Sep 08 2010', 
'F(n + 3) = 2F(n + 2) - F(n),', 
'i.e.  a(n+1) = (a(n)^2 - a(n-1)^2)/a(n-2), see A121646.', 
'F(n + 4) = 3F(n + 2) - F(n), ', 
'i.e. F(n+4) = ( (F(n+2)*F(n+3)) + (-1)^n ) /F(n+1) ', 
'F(n) = 4*F(n-3) + F(n-6). ', 
'F(n) = 4*F(n-2) - 2*F(n-3) - F(n-6). - Gary Detlefs, Apr 01 2012', 
'F(n + 8) = 7F(n + 4) - F(n), ', 
'F(n + 12) = 18F(n + 6) - F(n)', 
'F(n+10) = 11*F(n+5) + F(n).', 
'    i.e.  F(2n+4) = (F(2n+1) + 2*(-1)^n)/F(n-1) + sqrt(F(2n+1) + F(2n+2) + F(2n+3) + 2*(-1)^n)', 
'     i.e. a(2n+k) = ((-1)^k*a(n+k)^2 - a(n)^2)/a(n)', 
'    e.g. a(2n+1) = ((-1)^1*a(n+1)^2 - a(n)^2)/a(n)', 
'    F(2*n) = F(n+2)^2 - F(n+1)^2 - 2*F(n)^2. - Richard R. Forberg, Jun 04 2011', 
'    F(2*n) = F(n+1)^2 - F(n-1)^2,', 
'    i.e. F(2n+k+1) = F(n)*F(n+k) + F(n+1)*F(n+k+1)', 
'    i.e. F(2n+1) = F(n)^2 + F(n+1)^2', 
'    i.e.  F(3n) = F(n)^3 + F(n+1)^3 - F(n-1)^3 ', 
'    (F(n+3)^ 2 - F(n+1)^ 2)/F(n+2) = (F(n+3)+ F(n+1)) .))', 
'    (-1)^(n+1) = F(n)^2 + F(n)*F(1+n) - F(1+n)^2. ', 
'    F(n) = -F(n+2)(-2 + (F(n+1))^4 + 2*(F(n+1)^3*F(n+2)) - (F(n+1)*F(n+2))^2 2*F(n+1)(F(n+2))^3 + (F(n+2))^4)- F(n+1). ', 
'    i.e. F(1+n) = 3*F(n) (mod p)', 
'      or F(3+n) = [5/p]*F([5/p]+n) (mod p)', 
'F(n+m+1) = F(n)*F(m) + F(n+1)*F(m+1) ', 
' e.g. for m=1  ..  F(n+1+1) = F(n)*F(1) + F(n+1)*F(1+1) ', 
' e.g. for m=4  ..  F(n+4+1) = F(n)*F(4) + F(n+1)*F(4+1) ', 
'F(n) = F(k)*F(n-k+3) - F(k-1)*F(n-k+2) - F(k-2)*F(n-k) + (-1)^k*F(n-2k+2). - Charlie Marion, Dec 04 2014', 
'a(n) = 2^(n^2+n) - (4^n-2^n-1)*floor(2^(n^2+n)/(4^n-2^n-1)) - 2^n*floor(2^(n^2) - (2^n-1-1/2^n)*floor(2^(n^2+n)/(4^n-2^n-1)))', 
'approx. F(n) = (F(k)+F(k-1))*F(n-k-2) + (2*F(k)+F(k-1))*F(n-k-1) ', 
'i.e. F(n+k) = (-(-1)^(n+k) * F(k)^2 + F(n)^2)/F(n-k)', 
],


'A000124': [
        ' Central polygonal numbers, Lazy Caterer', 
        ' (discovered)',
' n(n+1)/2 + 1 ',
'a_n = a_{n-1} + n,',
'a(n+3) = 3*a(n+2) - 3*a(n+1) + a(n),',
'a(n) = 2*a(n-1) - a(n-2) + 1,',
'a(n) = 1 + floor(n/2) + ceiling(n^2/2),',
'a(n) = (n+1)^2 - n*(n+3)/2( nic v resnici),',
'a(n) = floor((n+2)/2)*ceiling((n+2)/2) + floor((n-1)/2)*ceiling((n-1)/2) ',
'a(n) = floor((n+2)**2/4) + floor((n-1)**2/4),',
 ],



'A000219': [ ' planar partitions ', 'no disc',
        'no popular formula',
'a(n) ~ (c_2 / n^(25/36)) * exp( c_1 * n^(2/3) )',
"""a(n) ~ Zeta(3)^(7/36) * exp(3 * Zeta(3)^(1/3) * (n/2)^(2/3) + 1/12) / 
    (A * sqrt(3*Pi) * 2^(11/36) * n^(25/36)) 
    * (1 + c1/n^(2/3) + c2/n^(4/3) + c3/n^2)""",
],

'A000292': [ 'Tetrahedral',   ' (quick checked, discovered)',
'a(n) = n*(n+1)*(n+2)/6 ',
'a(n) = (n+3)*a(n-1)/n,',
'a(n) = 4*a(n-1) - 6*a(n-2) + 4*a(n-3) - a(n-4) for n >= 4,',
'a(n) = (1/6)*floor(n^5/(n^2 + 1)),',
'a(n) = 3*a(n-1) - 3*a(n-2) + a(n-3) + 1,',
'a(n) = a(n-2) + n^2,',
'a(n) = n + 2*a(n-1) - a(n-2),',
'a(n) = (n**3 + 2*n)/3 - a(n-2),',
],

'A000720': [ ' PrimePi(n) aka. number of primes <= n',   '(no disc?)',
' a(n) ~ n/log(n) ,', 
' For n >= 33, a(n) = 1 + Sum_{j=3..n} ((j-2)! - j*floor((j-2)!/j)) (Hardy and Wright); for n >= 1, a(n) = n - 1 + Sum_{j=2..n} (floor((2 - Sum_{i=1..j} (floor(j/i)-floor((j-1)/i)))/j)),', 
' a(n) = Sum_{j=2..n} H(-sin^2 (Pi*(Gamma(j)+1)/j)) where H(x) is the Heaviside step function, taking H(0)=1. - Keshav Raghavan, Jun 18 2016,', 
],

'A001045': [ 'Jacobsthal sequence',   '(quick checked, discovered)',
'  a_n = a_{n-1} + 2*a_{n-2} ',
'   a_n = [2**n/3] ,',
'   a(n) ~ 2^n/3,',
'    a_n = 2^(n-1) - a(n-1),',
'   a(n) = 2*a(n-1) - (-1)^n,',
'   a(n) = (2^n - (-1)^n)/3,',
' a(2*n) = 2*a(2*n-1)-1 for n >= 1, a(2*n+1) = 2*a(2*n)+1, ',
' a(2*n) = (4^n - 1)/3; a(2*n+1) = (2^(2*n+1) + 1)/3,',
' a(n+1) = ceiling(2^n/3) + floor(2^n/3),',
' a(n+1) = (ceiling(2^n/3))^2 - (floor(2^n/3))^2,',
' a(n+1) = A005578(n) + A000975(n-1) = A005578(n)^2 - A000975(n-1)^2,',
' a(n) = ceiling(2^(n+1)/3) - ceiling(2^n/3) = A005578(n+1) - A005578(n),',
' a(n) = floor(2^(n+1)/3) - floor(2^n/3) = A000975(n) - A000975(n-1),',
' a(n) = A000975(n-1) + (1 + (-1)^(n-1))/2,',
' a(n) = (1-(-1)^n)/2 + floor((2^n)/3),',
' a(2*n-1) = a(n)^2 + 2*a(n-1)^2; a(2*n) = a(n+1)^2 - 4*a(n-1)^2,',
' a(m+n) = a(m)*a(n+1) + 2*a(m-1)*a(n), e.g. m=1,',
' a(m)*a(n+1) - a(m+1)*a(n) = (-2)^n*a(m-n), e.g. n=0,',
' a(m)*a(n) + a(m-1)*a(n-1) - 2*a(m-2)*a(n-2) = 2^(m+n-3),',
' a(m+n-1) = a(m)*a(n) + 2*a(m-1)*a(n-1); a(m+n) = a(m+1)*a(n+1) - 4*a(m-1)*a(n-1),',
' a(2*n-1) = a(n)^2 + 2*a(n-1)^2; a(2*n) = a(n+1)^2 - 4*a(n-1)^2,',
],

'A001097': [ 'aka. Twin primes',    '(quick checked, no disc.)',
' no formulas',],

'A001481': [ 'Numbers that are the sum of 2 squares',   '(quick checked, no disc.)',
' a(n) ~ k*n*sqrt(log n) '],

'A001615': [ 'Dedekind psi function: n * Product_{p|n, p prime} (1 + 1/p). ',
        '(quick checked, no disc.)',
' no formulas', ],

'A002572': [ 'Number of partitions of 1 into n powers of 1/2',  ' (quick checked, no disc.)',
'no prominent formula',
'a(n) ~ c_1 * c_0^n,', 
'  a(n) ~ c_1 * c_0^n + c_3 * c_0^n * c_2^n,', 
],

 'A005230': [ " a Stern's sequence",  ' (quick checked, no disc.)',
         'no prominent formula',
 "a(1) = 1, a(n+1) is the sum of the m preceding terms, where m*(m-1)/2 < n <= m*(m+1)/2 or equivalently m = ceiling((sqrt(8*n+1)-1)/2) ",
 " a(n) ~ 2*a(n-1)",
 ],

'A027642': [  'Denominator of Bernoulli number B_n',   '(quick checked, no disc.)',
' no formula ', ]
 }

# start


# formulas = (
#     'A000009', 
#     'A000040',  
#     'A000045',  
#     'A000124',  
#     'A000219',  
#     'A000292',  
#     'A000720',  
#     'A001045',  
#     'A001097',  
#     'A001481',  
#     'A001615',  
#     'A002572',  
#     'A005230',  
#     'A027642',  
# )



maxi = max(len(dicti[key]) for key in dicti)
# print('maxi', maxi)

def renorm_dict(dictx: dict):
    return {key: dictx[key] + (maxi-len(dictx[key]))*[''] for key in dictx} 

def empty_list(listi: list, empty_type=type(0.0), empty=''):
    return [i for i in listi if (i!='' and not isinstance(i, empty_type))]
def empty_dict(dictx: dict, empty_typ=type(0.0), empty=''):
    return {key: empty_list(dictx[key], empty) for key in dictx} 


dicti_norm = renorm_dict(dicti)
# for i in dicti_norm:
#     print(len(dicti_norm[i]))
# print(dicti_norm, len(dicti_norm))
# dicti = {'A09': ['a1', 'b2', 'c3', 'd',], }

df = pd.DataFrame(dicti_norm)
def print_skipping_empty(df, empty_type=type(0.0), empty=''):
    for id_ in df:
        print('\n', id_)
        for formula in empty_list(df[id_], empty_type, empty):
            print(formula)
    return 
# print_skipping_empty(df)

csv_filename = "oeis_formulas.csv"
# print(df)
df.to_csv(csv_filename, index=False)
print_skipping_empty(df)


# # Check after download:
check = pd.read_csv(csv_filename)
print("Read file from csv:")
# print(check)
print_skipping_empty(check)



