print(2)
import re
data_filename = '../outputs_golden/cluster-sam100-ord0-dirTrue.log'
data_filename = '../outputs_newgrammar/log_oeis_2021-06-12_10-29-38_success-14-newgrammar.txt'
f = open(data_filename, mode='r', encoding='utf-8')
log = f.read()
log_length = len(log)
print(type(log), f"{log_length:e}")
print(log[1:3000])
print(23)


log_replica = """ 
======================== 11 passed, 1 warning in 13.89s ========================
Let's finally execute the big program: 
Running equation discovery for all oeis sequences, with these settings:
=>> is_direct = True
=>> order of equation recursion = 0
=>> sample_size = 100
=>> grammar_template_name = polynomial
=>> generator_settings = {p_T: [0.4, 0.6], p_R: [0.6, 0.4]}
=>> optimizer = <function DE_fit at 0x1541cac7f700>
=>> timeout = inf

ModelBox: 29 models
-> C0*exp(C1*n**6), p = 0.0005898240000000002, parse trees = 1, valid = False
-> C0*exp(C1*n**3) + C2, p = 0.001600253853696, parse trees = 4, valid = False
-> C0*exp(C1*n) + C2, p = 0.017805311999999997, parse trees = 6, valid = False
-> C0*n, p = 0.09137664, parse trees = 2, valid = False
-> C0*exp(C1*n), p = 0.05981184, parse trees = 2, valid = False
-> C0*n**4 + C1, p = 0.001327104, parse trees = 2, valid = False
-> C0*n**6, p = 0.0008847360000000002, parse trees = 1, valid = False
-> C0*exp(C1*n**2), p = 0.02304, parse trees = 1, valid = False
-> C0*n + C1, p = 0.038058370007039995, parse trees = 7, valid = False
-> C0*n**4, p = 0.0055296, parse trees = 1, valid = False
-> C0*n + C1*exp(C2*n**3), p = 0.0005308416, parse trees = 1, valid = False
-> C0*n**3, p = 0.013824000000000001, parse trees = 1, valid = False
-> C0*n**2, p = 0.03456, parse trees = 1, valid = False
-> C0*exp(C1*n**4), p = 0.0036864000000000003, parse trees = 1, valid = False
-> C0*n**2 + C1, p = 0.009011036160000001, parse trees = 3, valid = False
-> C0*exp(C1*n**2) + C2*exp(C3*n**4) + C4, p = 8.153726976000003e-06, parse trees = 1, valid = False
-> C0*exp(C1*n**2) + C2, p = 0.00025820135424, parse trees = 2, valid = False
-> C0*n + C1*exp(C2*n**2) + C3, p = 0.000191102976, parse trees = 1, valid = False
-> C0*n**3 + C1, p = 0.0026581707113103362, parse trees = 3, valid = False
-> C0*n**2 + C1*exp(C2*n), p = 0.0013271040000000002, parse trees = 1, valid = False
-> C0*n + C1*exp(C2*n**2), p = 0.001327104, parse trees = 1, valid = False
-> C0*n**4 + C1*exp(C2*n) + C3, p = 2.93534171136e-06, parse trees = 1, valid = False
-> C0*exp(C1*n**3), p = 0.009216, parse trees = 1, valid = False
-> C0*n**2 + C1*exp(C2*n) + C3, p = 0.000193744783540224, parse trees = 2, valid = False
-> C0*n**5 + C1*n, p = 7.3383542784000014e-06, parse trees = 1, valid = False
-> C0*n + C1*exp(C2*n) + C3, p = 0.00031850495999999996, parse trees = 1, valid = False
-> C0*exp(C1*n) + C2*exp(C3*n**7), p = 9.059696640000004e-06, parse trees = 1, valid = False
-> C0*n + C1*exp(C2*n**5), p = 8.493465600000003e-05, parse trees = 1, valid = False
-> C0*n + C1*exp(C2*n), p = 0.0033177599999999995, parse trees = 1, valid = False
Estimating model C0*exp(C1*n**6)
model: 0.494192098337577*exp(-0.0404402296572887*n**6)                       ; p: 0.0005898240000000002  ; error: 128.10894721163822
Estimating model C0*exp(C1*n**3) + C2
model: 4.74410543304981 - 4.69122079738068*exp(-0.516979487839604*n**3)      ; p: 0.001600253853696      ; error: 102.08231309492034
Estimating model C0*exp(C1*n) + C2
model: 0.208269702145254*exp(0.0476291793638861*n) + 4.34876713020518        ; p: 0.017805311999999997   ; error: 100.16165010763935
Estimating model C0*n
model: 0.199109456363876*n                                                   ; p: 0.09137664             ; error: 96.06735881261598
Estimating model C0*exp(C1*n)
model: 1.78795240245205*exp(0.0367577939857759*n)                            ; p: 0.05981184             ; error: 95.87010550814088
Estimating model C0*n**4 + C1
model: 1.51396402192638e-6*n**4 + 3.27869216539917                           ; p: 0.001327104            ; error: 96.47853860614356
Estimating model C0*n**6
model: 1.31831212613065e-9*n**6                                              ; p: 0.0008847360000000002  ; error: 106.00439032782718
Estimating model C0*exp(C1*n**2)
model: 0.223847131784355*exp(-0.298486969498872*n**2)                        ; p: 0.02304                ; error: 128.1115275562621
Estimating model C0*n + C1
model: 0.180071975123876*n + 0.628237075086678                               ; p: 0.038058370007039995   ; error: 95.96569891956865
Estimating model C0*n**4
model: 0.000366947695784603*n**4                                             ; p: 0.0055296              ; error: 526029.8264235925
Estimating model C0*n + C1*exp(C2*n**3)
model: 0.201106770319862*n + 0.845094968840843*exp(-0.327833205027782*n**3)  ; p: 0.0005308416           ; error: 96.07143148270144
Estimating model C0*n**3
model: 0.00011445161559312*n**3                                              ; p: 0.013824000000000001   ; error: 100.88421283814999
Estimating model C0*n**2
model: 0.00501224198464367*n**2                                              ; p: 0.03456                ; error: 98.26595426353474
Estimating model C0*exp(C1*n**4)
model: 0.449057439824999*exp(-0.00428937679687491*n**4)                      ; p: 0.0036864000000000003  ; error: 128.0733307420157
Estimating model C0*n**2 + C1
model: 0.0035188149120248*n**2 + 2.19503911301702                            ; p: 0.009011036160000001   ; error: 96.098148338963
Estimating model C0*exp(C1*n**2) + C2*exp(C3*n**4) + C4
model: 5.0 + 0.406862819385809*exp(-1.32286556049967*n**4) - 4.27097183489554*exp(-0.00521256664575927*n**2); p: 8.153726976000003e-06  ; error: 99.59920983629328
Estimating model C0*exp(C1*n**2) + C2
model: 4.91529370110516 - 3.90648796884165*exp(-0.008015552950007*n**2)      ; p: 0.00025820135424       ; error: 99.88397136239955
Estimating model C0*n + C1*exp(C2*n**2) + C3
model: 0.178459911876078*n + 0.68145972840591 - 0.68045713784704*exp(-5.0*n**2); p: 0.000191102976         ; error: 95.95716697441452
Estimating model C0*n**3 + C1
model: 7.35689770388232e-5*n**3 + 2.83201013638185                           ; p: 0.0026581707113103362  ; error: 96.33962529821125
Estimating model C0*n**2 + C1*exp(C2*n)
model: -0.00433305256957098*n**2 + 2.10588137124915*exp(0.0480278478000397*n); p: 0.0013271040000000002  ; error: 95.73300672465551
Estimating model C0*n + C1*exp(C2*n**2)
model: 0.193993567964459*n + 0.680200867558373*exp(-0.00161246086667881*n**2); p: 0.001327104            ; error: 95.93949398641637
Estimating model C0*n**4 + C1*exp(C2*n) + C3
model: 1.34866347417047e-6*n**4 + 3.89097614590478 - 3.10376076992009*exp(-0.194164595216107*n); p: 2.93534171136e-06      ; error: 95.66073377922129
Estimating model C0*exp(C1*n**3)
model: 0.0219120673071823*exp(-3.82190505312208*n**3)                        ; p: 0.009216               ; error: 128.11999042461466
Estimating model C0*n**2 + C1*exp(C2*n) + C3
model: 0.00302272946677862*n**2 + 2.96267308671149 - 2.49425059916507*exp(-0.146242628833465*n); p: 0.000193744783540224   ; error: 95.792535503911
Estimating model C0*n**5 + C1*n
model: 1.06308706282476e-8*n**5 + 0.174078679247579*n                        ; p: 7.3383542784000014e-06 ; error: 95.96478187423189
Estimating model C0*n + C1*exp(C2*n) + C3
model: 0.178503611344039*n + 0.680101112742143 - 0.6742368901717*exp(-3.9858090536198*n); p: 0.00031850495999999996 ; error: 95.95721536099589
Estimating model C0*exp(C1*n) + C2*exp(C3*n**7)
model: 1.89768969259292*exp(0.035273073543859*n) - 1.49171164076619*exp(-4.23497249416526*n**7); p: 9.059696640000004e-06  ; error: 95.80958040649409
Estimating model C0*n + C1*exp(C2*n**5)
model: 0.199109563274111*n + 0.0111309650535758*exp(-4.27840294626221*n**5)  ; p: 8.493465600000003e-05  ; error: 96.06735634706068
Estimating model C0*n + C1*exp(C2*n)
model: 0.192660626491264*n + 0.784049227772141*exp(-0.0437853240270632*n)    ; p: 0.0033177599999999995  ; error: 95.95617801711771

Parameter fitting for sequence A000001 took 209.85773301217705 secconds.

Final score:
model: 0.494192098337577*exp(-0.0404402296572887*n**6); error: 128.10894721163822
model: 4.74410543304981 - 4.69122079738068*exp(-0.516979487839604*n**3); error: 102.08231309492034
model: 0.208269702145254*exp(0.0476291793638861*n) + 4.34876713020518; error: 100.16165010763935
model: 0.199109456363876*n           ; error: 96.06735881261598
model: 1.78795240245205*exp(0.0367577939857759*n); error: 95.87010550814088
model: 1.51396402192638e-6*n**4 + 3.27869216539917; error: 96.47853860614356
model: 1.31831212613065e-9*n**6      ; error: 106.00439032782718
model: 0.223847131784355*exp(-0.298486969498872*n**2); error: 128.1115275562621
model: 0.180071975123876*n + 0.628237075086678; error: 95.96569891956865
model: 0.000366947695784603*n**4     ; error: 526029.8264235925
model: 0.201106770319862*n + 0.845094968840843*exp(-0.327833205027782*n**3); error: 96.07143148270144
model: 0.00011445161559312*n**3      ; error: 100.88421283814999
model: 0.00501224198464367*n**2      ; error: 98.26595426353474
model: 0.449057439824999*exp(-0.00428937679687491*n**4); error: 128.0733307420157
model: 0.0035188149120248*n**2 + 2.19503911301702; error: 96.098148338963
model: 5.0 + 0.406862819385809*exp(-1.32286556049967*n**4) - 4.27097183489554*exp(-0.00521256664575927*n**2); error: 99.59920983629328
model: 4.91529370110516 - 3.90648796884165*exp(-0.008015552950007*n**2); error: 99.88397136239955
model: 0.178459911876078*n + 0.68145972840591 - 0.68045713784704*exp(-5.0*n**2); error: 95.95716697441452
model: 7.35689770388232e-5*n**3 + 2.83201013638185; error: 96.33962529821125
model: -0.00433305256957098*n**2 + 2.10588137124915*exp(0.0480278478000397*n); error: 95.73300672465551
model: 0.193993567964459*n + 0.680200867558373*exp(-0.00161246086667881*n**2); error: 95.93949398641637
model: 1.34866347417047e-6*n**4 + 3.89097614590478 - 3.10376076992009*exp(-0.194164595216107*n); error: 95.66073377922129
model: 0.0219120673071823*exp(-3.82190505312208*n**3); error: 128.11999042461466
model: 0.00302272946677862*n**2 + 2.96267308671149 - 2.49425059916507*exp(-0.146242628833465*n); error: 95.792535503911
model: 1.06308706282476e-8*n**5 + 0.174078679247579*n; error: 95.96478187423189
model: 0.178503611344039*n + 0.680101112742143 - 0.6742368901717*exp(-3.9858090536198*n); error: 95.95721536099589
model: 1.89768969259292*exp(0.035273073543859*n) - 1.49171164076619*exp(-4.23497249416526*n**7); error: 95.80958040649409
model: 0.199109563274111*n + 0.0111309650535758*exp(-4.27840294626221*n**5); error: 96.06735634706068
model: 0.192660626491264*n + 0.784049227772141*exp(-0.0437853240270632*n); error: 95.95617801711771

Total time consumed by now:211.4071998987347

ModelBox: 29 models
-> C0*exp(C1*n**6), p = 0.0005898240000000002, parse trees = 1, valid = False
-> C0*exp(C1*n**3) + C2, p = 0.001600253853696, parse trees = 4, valid = False
-> C0*exp(C1*n) + C2, p = 0.017805311999999997, parse trees = 6, valid = False
-> C0*n, p = 0.09137664, parse trees = 2, valid = False
-> C0*exp(C1*n), p = 0.05981184, parse trees = 2, valid = False
-> C0*n**4 + C1, p = 0.001327104, parse trees = 2, valid = False
-> C0*n**6, p = 0.0008847360000000002, parse trees = 1, valid = False
-> C0*exp(C1*n**2), p = 0.02304, parse trees = 1, valid = False
-> C0*n + C1, p = 0.038058370007039995, parse trees = 7, valid = False
-> C0*n**4, p = 0.0055296, parse trees = 1, valid = False
-> C0*n + C1*exp(C2*n**3), p = 0.0005308416, parse trees = 1, valid = False
-> C0*n**3, p = 0.013824000000000001, parse trees = 1, valid = False
-> C0*n**2, p = 0.03456, parse trees = 1, valid = False
-> C0*exp(C1*n**4), p = 0.0036864000000000003, parse trees = 1, valid = False
-> C0*n**2 + C1, p = 0.009011036160000001, parse trees = 3, valid = False
-> C0*exp(C1*n**2) + C2*exp(C3*n**4) + C4, p = 8.153726976000003e-06, parse trees = 1, valid = False
-> C0*exp(C1*n**2) + C2, p = 0.00025820135424, parse trees = 2, valid = False
-> C0*n + C1*exp(C2*n**2) + C3, p = 0.000191102976, parse trees = 1, valid = False
-> C0*n**3 + C1, p = 0.0026581707113103362, parse trees = 3, valid = False
-> C0*n**2 + C1*exp(C2*n), p = 0.0013271040000000002, parse trees = 1, valid = False
-> C0*n + C1*exp(C2*n**2), p = 0.001327104, parse trees = 1, valid = False
-> C0*n**4 + C1*exp(C2*n) + C3, p = 2.93534171136e-06, parse trees = 1, valid = False
-> C0*exp(C1*n**3), p = 0.009216, parse trees = 1, valid = False
-> C0*n**2 + C1*exp(C2*n) + C3, p = 0.000193744783540224, parse trees = 2, valid = False
-> C0*n**5 + C1*n, p = 7.3383542784000014e-06, parse trees = 1, valid = False
-> C0*n + C1*exp(C2*n) + C3, p = 0.00031850495999999996, parse trees = 1, valid = False
-> C0*exp(C1*n) + C2*exp(C3*n**7), p = 9.059696640000004e-06, parse trees = 1, valid = False
-> C0*n + C1*exp(C2*n**5), p = 8.493465600000003e-05, parse trees = 1, valid = False
-> C0*n + C1*exp(C2*n), p = 0.0033177599999999995, parse trees = 1, valid = False
Estimating model C0*exp(C1*n**6)
model: 1.91947441485522*exp(-0.00011488411411964*n**6)                       ; p: 0.0005898240000000002  ; error: 2.285887958147634
Estimating model C0*exp(C1*n**3) + C2
model: 1.51020596029971 - 0.506882706926984*exp(-5.0*n**3)                   ; p: 0.001600253853696      ; error: 0.24496532605924654
Estimating model C0*exp(C1*n) + C2
model: 1.51020599166967 - 0.506860591571408*exp(-5.0*n)                      ; p: 0.017805311999999997   ; error: 0.2449657737287258
Estimating model C0*n
model: 0.0455163834145988*n                                                  ; p: 0.09137664             ; error: 0.8249969078540705
Estimating model C0*exp(C1*n)
model: 1.49606911766362*exp(0.000121146150292797*n)                          ; p: 0.05981184             ; error: 0.24998892372042497
Estimating model C0*n**4 + C1
model: 1.49423260134902 - 1.13654562557014e-10*n**4                          ; p: 0.001327104            ; error: 0.2500377125273532
Estimating model C0*n**6
model: 1.89378512871485e-10*n**6                                             ; p: 0.0008847360000000002  ; error: 1.899747603633839
Estimating model C0*exp(C1*n**2)
model: 1.49020525302225*exp(7.05730763479464e-6*n**2)                        ; p: 0.02304                ; error: 0.24996283465006605
Estimating model C0*n + C1
model: 0.000240078152508978*n + 1.49411807391687                             ; p: 0.038058370007039995   ; error: 0.24998799519814596
Estimating model C0*n**4
model: 4.49242296696179e-7*n**4                                              ; p: 0.0055296              ; error: 1.6864384552839553
Estimating model C0*n + C1*exp(C2*n**3)
model: 0.0335858024720876*n + 1.26084307851482*exp(-3.98469047904974e-5*n**3); p: 0.0005308416           ; error: 0.2599533852361969
Estimating model C0*n**3
model: 2.17770202557161e-5*n**3                                              ; p: 0.013824000000000001   ; error: 1.5135969083121399
Estimating model C0*n**2
model: 0.00102445505744168*n**2                                              ; p: 0.03456                ; error: 1.2528223268970873
Estimating model C0*exp(C1*n**4)
model: 1.49403423696498*exp(3.24961835218573e-9*n**4)                        ; p: 0.0036864000000000003  ; error: 0.24993902025527745
Estimating model C0*n**2 + C1
model: 8.68832440474468e-6*n**2 + 1.4929774513238                            ; p: 0.009011036160000001   ; error: 0.2499595585353863
Estimating model C0*exp(C1*n**2) + C2*exp(C3*n**4) + C4
model: 1.49015290981861 - 5.0*exp(-0.90727272451464*n**4) + 4.51347361417905*exp(-0.579653398074892*n**2); p: 8.153726976000003e-06  ; error: 0.2354809855958296
Estimating model C0*exp(C1*n**2) + C2
model: 1.51020596238461 - 0.506882774363969*exp(-5.0*n**2)                   ; p: 0.00025820135424       ; error: 0.2449653260797153
Estimating model C0*n + C1*exp(C2*n**2) + C3
model: -0.00102115112580069*n + 1.5357414487078 - 0.532587675793035*exp(-5.0*n**2); p: 0.000191102976         ; error: 0.24476112136422976
Estimating model C0*n**3 + C1
model: 1.50927179896693 - 4.21756085611236e-8*n**3                           ; p: 0.0026581707113103362  ; error: 0.2500886673546706
Estimating model C0*n**2 + C1*exp(C2*n)
model: 7.31153769297352e-5*n**2 + 1.5291989040607*exp(-0.00241821148384931*n); p: 0.0013271040000000002  ; error: 0.24986075032603894
Estimating model C0*n + C1*exp(C2*n**2)
model: 0.029238267084658*n + 1.35129462789439*exp(-0.000933104298710408*n**2); p: 0.001327104            ; error: 0.2519040529681691
Estimating model C0*n**4 + C1*exp(C2*n) + C3
model: 5.71218294886933e-9*n**4 + 1.49892183618017 - 0.480700556340611*exp(-3.8279600262745*n); p: 2.93534171136e-06      ; error: 0.24521739287628347
Estimating model C0*exp(C1*n**3)
model: 1.49456332997666*exp(1.37345570049082e-7*n**3)                        ; p: 0.009216               ; error: 0.249940851937148
Estimating model C0*n**2 + C1*exp(C2*n) + C3
model: -6.92170589497354e-6*n**2 + 1.51591775192755 - 0.512609910531598*exp(-5.0*n); p: 0.000193744783540224   ; error: 0.24494088480546808
Estimating model C0*n**5 + C1*n
model: -8.21134271689061e-9*n**5 + 0.0668184360932644*n                      ; p: 7.3383542784000014e-06 ; error: 0.6616310496862293
Estimating model C0*n + C1*exp(C2*n) + C3
model: -0.00102157019712173*n + 1.53575542409959 - 0.532591171052966*exp(-5.0*n); p: 0.00031850495999999996 ; error: 0.24476156889425138
Estimating model C0*exp(C1*n) + C2*exp(C3*n**7)
model: -0.549888658640663*exp(-4.27568303195457*n**7) + 1.53717502022798*exp(-0.000705357401755479*n); p: 9.059696640000004e-06  ; error: 0.24483574857348414
Estimating model C0*n + C1*exp(C2*n**5)
model: 0.0360362952248661*n + 1.16941942073319*exp(-5.9992439349621e-8*n**5) ; p: 8.493465600000003e-05  ; error: 0.2778539525051352
Estimating model C0*n + C1*exp(C2*n)
model: -0.0150442221345107*n + 1.51774242175009*exp(0.00820249314294775*n)   ; p: 0.0033177599999999995  ; error: 0.2498505693814555

Parameter fitting for sequence A000002 took 355.9416435677558 secconds.
"""

# =======================SPECS:=======================================
specs_orig = """=>> is_direct = True
=>> order of equation recursion = 0
=>> sample_size = 100
=>> grammar_template_name = polynomial
=>> generator_settings = {p_T: [0.4, 0.6], p_R: [0.6, 0.4]}
=>> optimizer = <function DE_fit at 0x1541cac7f700>
=>> timeout = inf"""
print( "\n"*10)
specs = re.findall("""
=>> is_direct = \w+
=>> order of equation recursion = \d+
=>> sample_size = \d+
=>> grammar_template_name = \w+
=>> generator_settings = [^\n]+
=>> optimizer = [^\n]+
=>> timeout = [\w\.\,]+
""", log)
print('specs:', specs[0])
# =======================End Of SPECS:================================

seq_orig = "Parameter fitting for sequence A000001 took 209.85773301217705 secconds."
start = re.findall("ModelBox: (\d+) models", log)
seqs = re.findall(
        "ModelBox: \d+ models\n"
        "[\w\W]+?Parameter fitting for sequence \w+ took \d+.\d+ secconds.", log)
seq_ids = re.findall("Parameter fitting for sequence (\w+) took \d+.\d+ secconds.", log)
# print('seqs: \n', seqs[:150][0][-1000:], f"{len(seqs):e} {len(seqs[0]):e}")
print('seqs: \n', seqs[0])
print('seqs extracted:', f"{len(seqs)}")
print('length of text of one seq\'s result:', f"{len(seqs[0])}")
print(f'log_length: {log_length:e}')
seq = seqs[0]










f.close()
