import random
import time
import datetime
import pandas as pd

pwd = 'D:\Documents\Data\yfinance'
country = ['china', 'hk', 'japan', 'korea', 'usa', 'tw']
industry = ['bio', 'dev', 'dis', 'drug', 'ser', 'oth']
tickerChBio = ['300122.SZ', '300759.SZ', '603392.SS', '002821.SZ', '300957.SZ', '300363.SZ', '002007.SZ', '688202.SS', '002252.SZ', '600161.SS', '688180.SS', '603233.SS', '301047.SZ', '002603.SZ', '002030.SZ', '688366.SS', '688520.SS', '300009.SZ', '000990.SZ', '002653.SZ', '300294.SZ', '600201.SS', '688266.SS', '688298.SS', '300841.SZ', '002287.SZ', '688166.SS', '688526.SS', '688177.SS', '300497.SZ', '300942.SZ', '688278.SS', '688222.SS', '600645.SS', '603718.SS', '605199.SS', '300149.SZ', '002275.SZ', '603229.SS', '300255.SZ', '688670.SS', '688068.SS', '000710.SZ', '002022.SZ', '300653.SZ', '688488.SS', '603896.SS',
               '300705.SZ', '603566.SS', '000504.SZ', '688513.SS', '300204.SZ', '603439.SS', '605116.SS', '002286.SZ', '300871.SZ', '300381.SZ', '603590.SS', '600200.SS', '300181.SZ', '688098.SS', '300238.SZ', '603739.SS', '300966.SZ', '300147.SZ', '003020.SZ', '300858.SZ', '300404.SZ', '300878.SZ', '300049.SZ', '000004.SZ', '002566.SZ', '300583.SZ', '002873.SZ', '002868.SZ', '002898.SZ', '688399.SS', '688315.SS', '688658.SS', '688687.SS', '688221.SS', '688639.SS', '605177.SS', '688217.SS', '688136.SS', '688319.SS', '688578.SS', '688089.SS', '688076.SS', '688767.SS', '301080.SZ', '688317.SS', '688336.SS', '688189.SS']
tickerChDev = ['300760.SZ', '300896.SZ', '300595.SZ', '300003.SZ', '300529.SZ', '603087.SS', '300832.SZ', '002223.SZ', '688029.SS', '300888.SZ', '688301.SS', '002294.SZ', '688139.SS', '300677.SZ', '688050.SS', '300171.SZ', '688617.SS', '688289.SS', '002901.SZ', '688016.SS', '002382.SZ', '300633.SZ', '300298.SZ', '300869.SZ', '300981.SZ', '605369.SS', '300358.SZ', '600587.SS', '688277.SS', '600055.SS', '300573.SZ', '300143.SZ', '603987.SS', '002950.SZ', '603301.SS', '300326.SZ', '688026.SS', '603387.SS', '002932.SZ', '300206.SZ',
               '688580.SS', '300318.SZ', '688085.SS', '300642.SZ', '603222.SS', '300453.SZ', '300061.SZ', '301033.SZ', '688656.SS', '688338.SS', '300273.SZ', '300314.SZ', '300813.SZ', '300289.SZ', '688108.SS', '603309.SS', '688607.SS', '002432.SZ', '688393.SS', '300030.SZ', '300246.SZ', '300562.SZ', '300753.SZ', '688013.SS', '603880.SS', '688329.SS', '688677.SS', '301087.SZ', '688613.SS', '688161.SS', '688389.SS', '688358.SS', '688067.SS', '605186.SS', '688606.SS', '688314.SS', '688310.SS', '688575.SS', '688626.SS', '688198.SS']
tickerChDis = ['601607.SS', '600739.SS', '603939.SS', '600998.SS', '603883.SS', '002727.SZ', '200028.SZ', '000028.SZ',
               '600056.SS', '301017.SZ', '603368.SS', '605266.SS', '002758.SZ', '300937.SZ', '002462.SZ', '002788.SZ', '600833.SS']
tickerChDrug = ['600276.SS', '600436.SS', '000538.SZ', '600196.SS', '000661.SZ', '300142.SZ', '300601.SZ', '002001.SZ', '000963.SZ', '688185.SS', '600332.SS', '600085.SS', '603707.SS', '603456.SS', '000739.SZ', '300558.SZ', '600079.SS', '000513.SZ', '300357.SZ', '600521.SS', '300725.SZ', '000423.SZ', '002422.SZ', '000999.SZ', '000403.SZ', '600511.SS', '600518.SS', '600867.SS', '600380.SS', '600535.SS', '300630.SZ', '603858.SS', '002019.SZ', '002399.SZ', '002626.SZ', '000623.SZ', '600277.SS', '600329.SS', '002773.SZ', '000627.SZ', '600216.SS', '600812.SS', '688321.SS', '605507.SS', '002262.SZ', '600771.SS', '688505.SS', '600267.SS', '002793.SZ', '600566.SS', '301015.SZ', '603567.SS', '002390.SZ', '300702.SZ', '002099.SZ', '603520.SS', '002004.SZ', '300026.SZ', '600211.SS', '600062.SS', '000650.SZ', '600993.SS', '600572.SS', '600195.SS', '600252.SS', '002332.SZ', '002038.SZ', '600420.SS', '300723.SZ', '300119.SZ', '600129.SS', '300267.SZ', '000078.SZ', '300401.SZ', '002737.SZ', '002424.SZ', '600664.SS', '000989.SZ', '002317.SZ', '600750.SS', '002020.SZ', '002900.SZ', '600976.SS', '000597.SZ', '300158.SZ', '002880.SZ', '002219.SZ', '600422.SS', '600789.SS',
                '300006.SZ', '603669.SS', '000915.SZ', '600557.SS', '300109.SZ', '600285.SS', '603367.SS', '002550.SZ', '300683.SZ', '000566.SZ', '300485.SZ', '002437.SZ', '300110.SZ', '600351.SS', '002923.SZ', '300194.SZ', '600222.SS', '002907.SZ', '603538.SS', '300199.SZ', '600488.SS', '300436.SZ', '300039.SZ', '600713.SS', '002349.SZ', '002688.SZ', '600594.SS', '002433.SZ', '300016.SZ', '002198.SZ', '000756.SZ', '688566.SS', '000788.SZ', '000766.SZ', '300239.SZ', '002644.SZ', '603676.SS', '000153.SZ', '002118.SZ', '002107.SZ', '600568.SS', '600479.SS', '600829.SS', '002393.SZ', '000919.SZ', '603351.SS', '300636.SZ', '000908.SZ', '000790.SZ', '000411.SZ', '603168.SS', '002940.SZ', '603811.SS', '002750.SZ', '603079.SS', '002365.SZ', '002412.SZ', '600080.SS', '301075.SZ', '600613.SS', '002728.SZ', '600530.SS', '300452.SZ', '000952.SZ', '300519.SZ', '000705.SZ', '600513.SS', '603998.SS', '002370.SZ', '300086.SZ', '600666.SS', '002864.SZ', '000590.SZ', '300584.SZ', '002817.SZ', '603139.SS', '600781.SS', '002826.SZ', '300534.SZ', '002693.SZ', '603963.SS', '300254.SZ', '600671.SS', '600385.SS', '900904.SS', '688131.SS', '688799.SS', '688117.SS', '688621.SS', '688091.SS', '688276.SS']
tickerChSer = ['300253.SZ', '300451.SZ', '000503.SZ', '300288.SZ',
               '603990.SS', '300550.SZ', '600767.SS', '688555.SS']
tickerChOth = ['603259.SS', '300015.SZ', '300347.SZ', '600763.SS', '603127.SS', '603882.SS', '300676.SZ', '603658.SS', '002044.SZ', '300244.SZ', '300685.SZ',
               '300482.SZ', '300463.SZ', '300406.SZ', '000950.SZ', '300639.SZ', '301060.SZ', '300439.SZ', '603108.SS', '300396.SZ', '600896.SS', '000150.SZ', '603716.SS']
tickerHkBio = ['2269.HK', '6160.HK', '3759.HK', '1801.HK', '1177.HK', '9688.HK', '1548.HK', '1877.HK', '9995.HK', '0013.HK', '9926.HK', '9969.HK', '6826.HK', '2171.HK', '2096.HK', '2137.HK', '1530.HK', '9966.HK', '9939.HK', '1167.HK', '2696.HK', '1952.HK',
               '1873.HK', '1477.HK', '2162.HK', '2616.HK', '1521.HK', '6978.HK', '2256.HK', '6855.HK', '6600.HK', '6996.HK', '0775.HK', '2126.HK', '6998.HK', '2142.HK', '6628.HK', '2181.HK', '6622.HK', '1061.HK', '1672.HK', '3681.HK', '1875.HK', '8158.HK', '0690.HK']
tickerHkDev = ['0853.HK', '1066.HK', '6699.HK', '1302.HK', '2500.HK', '2160.HK', '2235.HK', '9996.HK', '2190.HK', '9997.HK', '6118.HK', '1789.HK', '1763.HK', '1858.HK',
               '1696.HK', '3600.HK', '2216.HK', '1501.HK', '6669.HK', '6609.HK', '2170.HK', '2393.HK', '1358.HK', '1134.HK', '0907.HK', '0876.HK', '1612.HK', '1942.HK', '1120.HK', '8513.HK']
tickerHkDis = ['0241.HK', '1099.HK', '2607.HK', '2192.HK', '3613.HK', '1931.HK', '1345.HK', '3390.HK',
               '2289.HK', '0718.HK', '1110.HK', '0673.HK', '0348.HK', '0574.HK', '0401.HK', '8372.HK', '2211.HK']
tickerHkDrug = ['2196.HK', '3692.HK', '1093.HK', '6185.HK', '0874.HK', '1513.HK', '0867.HK', '9989.HK', '3320.HK', '0512.HK', '0570.HK', '0460.HK', '2186.HK', '2005.HK', '3933.HK', '1666.HK', '2877.HK', '0719.HK', '1349.HK', '2552.HK', '1558.HK',
                '1681.HK', '2348.HK', '0950.HK', '1652.HK', '6896.HK', '2633.HK', '3737.HK', '2161.HK', '0503.HK', '8049.HK', '0455.HK', '0239.HK', '1889.HK', '0897.HK', '1643.HK', '8329.HK', '1312.HK', '3839.HK', '1498.HK', '0858.HK', '1011.HK', '8622.HK', '0911.HK']
tickerHkSer = ['1833.HK', '2158.HK', '6819.HK', '2159.HK']
tickerHkOth = ['2359.HK', '6618.HK', '3347.HK', '6127.HK', '6078.HK', '0708.HK', '1951.HK', '6606.HK', '3309.HK', '1515.HK', '2219.HK', '9960.HK', '3886.HK', '0286.HK', '1846.HK', '2120.HK', '1526.HK', '0383.HK',
               '9906.HK', '8037.HK', '3689.HK', '1989.HK', '2189.HK', '2135.HK', '0722.HK', '2389.HK', '1518.HK', '8225.HK', '1419.HK', '8405.HK', '2293.HK', '8357.HK', '0928.HK', '8143.HK', '8437.HK', '8307.HK', '8161.HK']
tickerJpBio = ['4974.T', '4587.T', '4565.T', '4880.T', '4593.T', '4563.T', '2160.T', '4592.T', '4599.T', '7096.T', '7774.T', '4571.T', '4579.T', '4875.T', '2183.T', '4978.T', '4888.T', '4564.T', '4584.T',
               '4572.T', '2370.T', '4588.T', '4591.T', '4583.T', '2342.T', '4596.T', '2385.T', '4576.T', '4594.T', '4598.T', '4881.T', '6090.T', '4570.T', '7776.T', '2191.T', '4884.T', '6190.T', '2176.T', '4575.T']
tickerJpDev = ['7741.T', '4543.T', '7733.T', '7747.T', '6523.T', '7780.T', '6849.T', '3360.T', '7716.T', '7730.T', '8086.T', '3046.T', '6960.T', '7817.T', '7575.T', '3593.T', '7779.T', '4549.T', '7600.T',
               '4548.T', '7749.T', '7979.T', '6823.T', '3154.T', '7702.T', '7775.T', '7743.T', '7777.T', '6678.T', '3446.T', '3079.T', '4889.T', '7963.T', '5187.T', '7792.T', '4556.T', '3604.T', '7813.T', '7782.T', '5212.T']
tickerJpDis = ['3141.T', '3349.T', '3391.T', '3088.T', '7649.T', '7459.T', '9989.T', '2784.T', '7476.T', '9987.T', '9627.T', '3549.T', '3148.T', '9267.T', '3034.T', '7679.T',
               '2664.T', '3151.T', '4931.T', '3183.T', '8095.T', '4350.T', '2934.T', '3417.T', '7634.T', '3544.T', '2689.T', '2796.T', '7681.T', '9265.T', '9776.T', '7129.T', '2928.S', '3055.S']
tickerJpDrug = ['4519.T', '4502.T', '4568.T', '4503.T', '4578.T', '4523.T', '4507.T', '4151.T', '4528.T', '4506.T', '4536.T', '4516.T', '4581.T', '4552.T', '4530.T', '4540.T', '4887.T', '4521.T', '4553.T', '8129.T', '4534.T',
                '4547.T', '4569.T', '4559.T', '4551.T', '2929.T', '4541.T', '3341.T', '4577.T', '4582.T', '4574.T', '4883.T', '4886.T', '4554.T', '9273.T', '4595.T', '4538.T', '4550.T', '4597.T', '4512.T', '4539.T', '4524.T', '4882.T', '4586.T']
tickerJpSer = ['2413.T', '4483.T', '2175.T', '4480.T', '6095.T', '3902.T', '4820.T', '3733.T', '9438.T',
               '3939.T', '3628.T', '3649.T', '6078.T', '7079.T', '4320.T', '4172.T', '4438.T', '3671.T', '6545.T']
tickerJpOth = ['6869.T', '7071.T', '4694.T', '4544.T', '6197.T', '6099.T', '2395.T', '6062.T', '2150.T', '2309.T', '2372.T', '2374.T', '4671.T', '7707.T', '8769.T', '7061.T', '2373.T',
               '7091.T', '6034.T', '7097.T', '6059.T', '3386.T', '7070.T', '7090.T', '7362.T', '7037.T', '2397.T', '7363.T', '6063.T', '4355.T', '2425.T', '6029.T', '2435.T', '6557.T', '7083.T', '2137.S']
tickerKoBio = ['207940.KS', '068270.KS', '302440.KS', '326030.KS', '006280.KS',
               '005257.KS', '005250.KS', '011000.KS', '005690.KS', '001630.KS', '950210.KS', '002630.KS']
tickerKoDev = ['137310.KS', '145720.KS', '004080.KS']
tickerKoDis = []
tickerKoDrug = ['000100.KS', '008930.KS', '128940.KS', '019175.KS', '019170.KS', '069620.KS', '003090.KS', '185750.KS', '009420.KS', '003850.KS', '102460.KS', '003000.KS', '003520.KS', '001067.KS', '000105.KS', '001065.KS', '007575.KS', '033270.KS', '000640.KS', '170900.KS', '007570.KS', '008490.KS', '271980.KS', '001060.KS', '000020.KS',
                '003060.KS', '001360.KS', '293480.KS', '003220.KS', '249420.KS', '002390.KS', '009290.KS', '005500.KS', '016580.KS', '002620.KS', '096760.KS', '234080.KS', '214390.KS', '063160.KS', '002210.KS', '017180.KS', '004720.KS', '004310.KS', '000230.KS', '000220.KS', '118000.KS', '003120.KS', '002720.KS', '000520.KS', '000225.KS', '000227.KS']
tickerKoSer = []
tickerKoOth = []
tickerUsBio = ['NONOF', 'NVO', 'MRNA', 'CSLLY', 'CMXHF', 'BNTX', 'WXXWY', 'WXIBF', 'REGN', 'VRTX', 'BGNE', 'SGEN', 'GNMSF', 'GMAB', 'DNA', 'ALNY', 'RPRX', 'UCBJF', 'UCBJY', 'TECH', 'INCY', 'ARGX', 'SBMFF', 'IVBXF', 'BMRN', 'XLRN', 'NVAX', 'ZLAB', 'NTLA', 'OBMP', 'NBIX', 'MRTX', 'GNNSF', 'BHVN', 'JAZZ', 'UTHR', 'ASND', 'LEGN', 'CVAC', 'CRSP', 'BBIO', 'ARWR', 'SRPT', 'EXEL', 'BEAM', 'CERT', 'BPMC', 'KOD', 'ALLK', 'CERE', 'DNLI', 'HCM', 'MRVI', 'FATE', 'HALO', 'RARE', 'VIR', 'IMAB', 'ABCM', 'ABCZF', 'ALKS', 'ADPT', 'TGTX', 'ARVN', 'ABCL', 'IONS', 'IOVA', 'KRTX', 'AUPH', 'SANA', 'ARNA', 'ADGI', 'IDRSF', 'RETA', 'ZNTL', 'ITCI', 'LYEL', 'GLPG', 'RLAY', 'VCYT', 'IBRX', 'BVNRY', 'INSM', 'RXRX', 'CYTK', 'SWTX', 'NKTR', 'PPTDF', 'AGIO', 'EXAI', 'KYMR', 'PRTA', 'FOLD', 'APLS', 'ACAD', 'BCRX', 'EDIT', 'PTCT', 'RCUS', 'CCXI', 'SAGE', 'VALN', 'VCEL', 'TIL', 'HRMY', 'ERAS', 'INRLF', 'LGND', 'XNCR', 'ALLO', 'ALXO', 'ATAI', 'CLDX', 'NUVB', 'CCCC', 'VERV', 'MORF', 'ADCT', 'CORT', 'TPTX', 'SEER', 'SRNE', 'DCPH', 'MYOV', 'RVMD', 'IUGNF', 'CDXS', 'GBT', 'RCKT', 'SAVA', 'AMRN', 'TRIL', 'ALEC', 'OXBDF', 'OCGN', 'ISEE', 'CRTX', 'BLI', 'IMCR', 'KDMN', 'DRNA', 'IGMS', 'TVTX', 'ALVR', 'CDMO', 'XENE', 'MOR', 'RGNX', 'BCYC', 'MPSYF', 'VBIZF', 'ENTA', 'CNTA', 'PTGX', 'DAWN', 'AXSM', 'NGM', 'PHMMF', 'INBX', 'INO', 'CLVLY', 'BLUE', 'ZLDPF', 'ZEAL', 'PRTC', 'RUBY', 'REPL', 'QURE', 'AVXL', 'PTCHF', 'CRBU', 'MDGL', 'ATRA', 'CHRS', 'NRIX', 'GBIO', 'TLPPF', 'KRYS', 'ARCT', 'IMGN', 'PCVX', 'SGMO', 'MGNX', 'IPSC', 'KURA', 'DICE', 'QSI', 'MNKD', 'YMAB', 'TNGX', 'PMVP', 'OMGA', 'OLMA', 'INVA', 'ZYME', 'ABSI', 'ARQT', 'GLUE', 'MRUS', 'CERS', 'AVIR', 'HRTX', 'FGEN', 'RNA', 'PRAX', 'RXDX', 'KNTE', 'NUVL', 'RVNC', 'HUMA', 'VNDA', 'ICVX', 'CYDY', 'ACRS', 'FULC', 'GOSS', 'NWBO', 'RAPT', 'BCAB', 'PHAT', 'CGEM', 'JANX', 'ITOS', 'KRON', 'PGEN', 'IMVT', 'KROS', 'TNYA', 'MGTX', 'VTYX', 'SNDX', 'FMTX', 'SRRK', 'RPTX', 'IMGO', 'CNTB', 'MNMD', 'FDMT', 'ZGNX', 'STOK', 'AGEN', 'STRO', 'AMTI', 'VXRT', 'TYRA', 'IDYA', 'CRNX', 'BTAI', 'MEOBF', 'DSGN', 'PRLD', 'STTK', 'CELU', 'IMTX', 'MESO', 'ANAB', 'EWTX', 'GHRS', 'ADAP', 'VBIV', 'AMGXF', 'LXRX', 'AKRO', 'ORMP', 'AFMD', 'KNSA', 'DYN', 'PNT', 'GRPH', 'GRCL', 'ALGS', 'SLN', 'TALS', 'ANNX', 'CARA', 'SLNCF', 'NAUT', 'VERU', 'CRIS', 'RFL', 'MLLCF', 'IMRX', 'MOLN', 'MRSN', 'PHAR', 'FNCH', 'CYT', 'TSHA', 'BYSI', 'PLRX', 'CPRX', 'THRX', 'GRTS', 'PHGUF', 'VOR', 'IVA', 'TARS', 'ORIC', 'GTHX', 'ABOS', 'MCRB', 'DTIL', 'TBPH', 'RLYB', 'NKTX', 'SYGGF', 'OCUL', 'AADI', 'DBVT', 'RYTM', 'ALBO', 'LABP', 'CALT', 'RIGL', 'ABUS', 'CGEN', 'SIGA', 'PHVS', 'AAVXF', 'SPRO', 'CLVS', 'NRXP', 'ADAG', 'BLU', 'PRQR', 'AKBA', 'CLLS', 'SMMT', 'CVM', 'ELYM', 'VACC', 'BOLT', 'PASG', 'AMAM', 'KDNY', 'MIRM', 'ICPT', 'GERN', 'VSTM', 'ALDX', 'BTX', 'ENOB', 'JNCE', 'FHTX', 'EPZM', 'IKNA', 'CMRX', 'ALT', 'PROG', 'GLSI', 'HOWL', 'VKTX', 'ACIU', 'NBTX', 'CDXC', 'VTGN', 'XBIT', 'EFTR', 'JSPR', 'EVLO', 'KZR', 'IPHYF', 'PYXS', 'ATHA', 'IPHA', 'MRNS', 'RLMD', 'SELB', 'AVCTF', 'AUTL', 'KALV', 'APLT', 'PRVB', 'OMER', 'KPTI', 'RANI', 'EPIX', 'HGEN', 'PSTX', 'INKT', 'LCTX', 'CUE', 'OTLK', 'MGTA', 'RLFTF', 'AGLE', 'RAIN', 'VERA', 'URGN', 'IMMP', 'ETNB', 'ATOS', 'SPHRF', 'KMPH', 'CTMX', 'MDCLF', 'SURF', 'PDSB', 'ENZC', 'PRRUF', 'VRCA', 'CLNN', 'INMB', 'BMEA', 'AVTE', 'ZIOP', 'CABA', 'NMTR', 'SQZ', 'MYMD', 'SPHRY', 'FIXX', 'CLSD', 'COGT', 'EYPT', 'OPT', 'PBIGF', 'CDAK', 'BBIXF', 'SPPI', 'CYBN', 'ALPN', 'FBIO', 'FUSN', 'AMPE', 'SBTX', 'OCX', 'MTEM', 'MEIP', 'AKUS', 'VRNA', 'VRDN', 'CADL', 'PIRS', 'BDTX', 'NEXI', 'CTXR', 'ATHX', 'ACHL', 'ANGN', 'XOMA', 'ONCR', 'OYST', 'ONPPF', 'SYRS', 'CBAY', 'TCRR', 'CKPT', 'CGTX', 'LPTX', 'PRTG', 'ACET', 'CTIC', 'AVTX', 'VINC', 'SCNLF', 'ACBM', 'SEEL', 'SRRA', 'OVID', 'ORTX', 'PRTK', 'LIFE', 'CRDF', 'GMDA', 'AVRO', 'FENC', 'MREO', 'MTNB', 'SESN', 'ANVS', 'IMNM', 'TERN', 'TCDA', 'VIRX', 'FREQ', 'SRZN', 'IMUX', 'SNSE', 'LRMR', 'AVEO', 'VECT', 'CLGN', 'INFI', 'INZY', 'WVE', 'NXTC', 'EIGR', 'PBYI', 'ORYZF', 'SLGL', 'ESPR', 'HARP', 'OBSV', 'TNXP', 'GTBP', 'IMPL', 'SGTX', 'CMPX', 'MBIO', 'BCEL', 'TCRX', 'ADVM', 'ALZN',
               'CRVS', 'APTO', 'TFFP', 'GALT', 'TRVN', 'CRMD', 'MIRO', 'PHAS', 'LQDA', 'ELEV', 'DBTX', 'NURPF', 'KLDO', 'ONCT', 'SYBX', 'ATNF', 'LVTX', 'IBIO', 'MNOV', 'GNFT', 'ATNM', 'MIST', 'TYME', 'EQ', 'STSA', 'SCPH', 'DMTTF', 'LBPS', 'ADMA', 'EVAX', 'ENLV', 'TLSA', 'RPHM', 'NYMX', 'GMTX', 'BFRA', 'ANEB', 'ELVAF', 'OSMT', 'VBLT', 'KZIA', 'CASI', 'HOOK', 'ORPH', 'VYGR', 'CFRX', 'SIOX', 'OZYMF', 'FSTX', 'CALA', 'SLS', 'ASMB', 'FBIOP', 'ACHFF', 'LBPH', 'SVRA', 'BLRX', 'HTBX', 'ETON', 'BIVI', 'PYPD', 'NOVN', 'ETTX', 'AYLA', 'CSBR', 'NBSE', 'IMV', 'XERS', 'CRBP', 'DYAI', 'IFRX', 'INAB', 'NCNA', 'LOGC', 'UBX', 'MDNA', 'IPIX', 'IPA', 'KALA', 'ODT', 'RCOR', 'ONCY', 'ARDX', 'VTVT', 'ENTX', 'LTRN', 'MRKR', 'CYCN', 'ELOX', 'BCTX', 'EVGN', 'CMMB', 'HEPA', 'FRLN', 'BCLI', 'PCSA', 'STAB', 'ORGS', 'AGTC', 'XFOR', 'EVFM', 'CBIO', 'OTIC', 'AXLA', 'SPRB', 'DMAC', 'BNOEF', 'EDSA', 'GNPX', 'EYEN', 'LYRA', 'LJPC', 'APRE', 'CDTX', 'AIMD', 'RVXCF', 'DARE', 'ERYP', 'XCUR', 'RZLT', 'MDWD', 'OPNT', 'TBGNF', 'GLYC', 'GNCA', 'ITRM', 'ASLN', 'HCWB', 'IMRA', 'PTN', 'NGENF', 'YMTX', 'JAGX', 'LPCN', 'PSTI', 'ATXS', 'COCP', 'AIM', 'RCAR', 'CMPI', 'CAPR', 'TSOI', 'APM', 'BXPHF', 'CNCE', 'GLTO', 'ABEO', 'YECO', 'IGXT', 'EMMLF', 'ALRN', 'GANX', 'AKTX', 'PPBT', 'BMBIF', 'BPTS', 'CLSN', 'TPST', 'MBRX', 'ACHV', 'TARA', 'AIKI', 'CYAD', 'CNTX', 'ACST', 'LUMO', 'APTX', 'ARMP', 'CLYYF', 'TBPMF', 'ARAV', 'RGBP', 'EMMA', 'AEZS', 'OGEN', 'BPSR', 'ONTX', 'APVO', 'ICCC', 'ELDN', 'ADXS', 'MMIRF', 'OCUP', 'ZSAN', 'TCON', 'ONCS', 'GRAY', 'ADIL', 'ALNA', 'AYTU', 'MBXBF', 'LGVN', 'ABVC', 'MITO', 'CLBS', 'INTI', 'PHGE', 'SNPX', 'ACOGF', 'ARFXF', 'SLNO', 'CUBT', 'GLMD', 'MACK', 'VYNT', 'VYNE', 'CWBR', 'MNPR', 'NNVC', 'SCPS', 'NBRV', 'NERV', 'PMCB', 'AXIM', 'VCNX', 'ATHE', 'SYN', 'CVALF', 'LMNL', 'CLRB', 'ENSC', 'PLX', 'ACXP', 'UPC', 'PRNAF', 'MYNDF', 'WINT', 'NAVB', 'NRBO', 'AWKNF', 'ARDS', 'VRPX', 'RNXT', 'GRTX', 'FWP', 'RDTCF', 'BXRX', 'BCDA', 'RVPH', 'IKT', 'MRZM', 'ADXN', 'IDRA', 'CYCC', 'BBI', 'ACOR', 'DFFN', 'PTE', 'CLCS', 'ADTX', 'OTLC', 'NTRB', 'SRBCF', 'MSSTF', 'ICOTF', 'APLIF', 'SNGX', 'ZHCLF', 'PULM', 'ABIO', 'INDP', 'RGLS', 'CRPOF', 'ANPC', 'FBRX', 'MTCR', 'CNSP', 'KTRA', 'TENX', 'DRMA', 'SLRX', 'ENVB', 'LEXX', 'SONN', 'UNCY', 'SIGY', 'BLPH', 'VIRI', 'PALI', 'ZLDAF', 'KRBP', 'RNAZ', 'BPTH', 'AGTX', 'KTTA', 'TRVI', 'AGE', 'ZIVO', 'VLON', 'ACER', 'QLGN', 'XRTX', 'BVXV', 'PTIX', 'PRED', 'CANF', 'PKTX', 'PHRRF', 'NUGX', 'BNTC', 'BSTG', 'HSTO', 'BVAXF', 'FWBI', 'NLSP', 'ARTH', 'HAVLF', 'ATXI', 'NEVPF', 'TMBR', 'PSYBF', 'PBLA', 'SPHDF', 'WSNAF', 'LIXT', 'PSTV', 'HOTH', 'BRAXF', 'ENZN', 'PVCT', 'GOVX', 'EYEG', 'NBY', 'RGRX', 'CYTO', 'CMNDF', 'SKYE', 'WPDPF', 'XBIO', 'BITRF', 'PHIO', 'MTP', 'CNBX', 'IMRN', 'XTLB', 'NVIV', 'MCURF', 'CYTR', 'TRYPF', 'SILO', 'TTNP', 'MLCT', 'INM', 'BETRF', 'GNBT', 'CELZ', 'INNMF', 'ARTL', 'BLCM', 'BIOAF', 'BICTF', 'QBIO', 'BTHE', 'CRYO', 'CYCCP', 'KNBIF', 'SPRCF', 'BSEM', 'ONPH', 'APOP', 'VPRO', 'VXLLF', 'MYMX', 'BRTX', 'COEP', 'ENTBF', 'NGRC', 'AGNPF', 'GSTC', 'GBLX', 'PRVCF', 'QSAM', 'HMTXF', 'CPMV', 'NMDBF', 'REPCF', 'NBIO', 'ETBI', 'SGBI', 'KALTF', 'TCCR', 'AVXT', 'NSPDF', 'XSNX', 'HCYT', 'LVCLY', 'NTRR', 'USRM', 'NTII', 'PSCBF', 'PCNT', 'NPTX', 'IPCIF', 'BICB', 'TXTM', 'FNAM', 'ISCO', 'RASP', 'BZYR', 'POLXF', 'AMBS', 'AFFY', 'RGIN', 'IMUC', 'RGBPP', 'ATRX', 'IMNPQ', 'RSPI', 'ARTLW', 'PHIOW', 'ENDV', 'GTHR', 'HALB', 'PPCB', 'MRES', 'NSHSF', 'IMUN', 'RCHA', 'VGLS', 'MCET', 'CDXI', 'HSTC', 'NSPXD', 'MRPI', 'MBCI', 'TLOG', 'LCAR', 'PLPL', 'VNTA', 'BIXT', 'NBCO', 'BSSP', 'ADYX', 'HESG', 'NNLX', 'ROTH', 'ITMC', 'EPRSQ', 'PZRXQ', 'CRXM', 'HTDS', 'SNNAQ', 'VRCI', 'NNBP', 'GNLKQ', 'RCPIQ', 'TNGNQ', 'VCEX', 'VIAP', 'MMDCF', 'PTIXW', 'CLNNW', 'RVPHW', 'EFTRW', 'LIXTW', 'NRXPW', 'DTCFF', 'LBPSW', 'CELUW', 'ENTXW', 'KTTAW', 'OTLKW', 'HUMAW', 'GEOVF', 'IMRNW', 'SRZNW', 'ENSCW', 'OCTHF', 'WINTW', 'BCDAW', 'ROIVW', 'XLO', 'XOMAP', 'CTXRW', 'LEXXW', 'LEXTF', 'GOVXW', 'JSPRW', 'SNGXW', 'MMDWF', 'ROIV', 'NLSPW', 'ATNFW', 'IMTXW', 'ZIVOW', 'NTRBW', 'BCTXW', 'SYRSW', 'NOVNW', 'ADILW', 'DRMAW', 'EMMAW', 'AYTUZ', 'XOMAO', 'QSIAW']
tickerUsDev = ['ABT', 'MDT', 'ISRG', 'SYK', 'ESLOY', 'ESLOF', 'EW', 'BDX', 'BSX', 'HOCPF', 'HOCPY', 'SDMHF', 'ALGN', 'SUVPF', 'SARTF', 'BAX', 'ALC', 'RMD', 'CLPBY', 'CLPBF', 'TRUMF', 'TRUMY', 'SAUHF', 'SAUHY', 'ZBH', 'WST', 'OCPNY', 'SONVF', 'SONVY', 'STE', 'BIO', 'BIO-B', 'PODD', 'COO', 'HOLX', 'CZMWF', 'CZMWY', 'TFX', 'ABMD', 'MASI', 'SNN', 'SNNUF', 'RGEN', 'GNGBF', 'GNGBY', 'FSPKF', 'XRAY', 'NVCR', 'BRKR', 'WILYY', 'WILLF', 'CHEOY', 'CHEOF', 'PEN', 'HRC', 'MCRPF', 'GNNDY', 'TNDM', 'GMED', 'SWAV', 'STVN', 'AMBBY', 'INSP', 'VTRLY', 'INMD', 'WRBY', 'NVST', 'IART', 'STAA', 'CNVVY', 'TGLVY', 'ICUI', 'EKTAY', 'NARI', 'LIVN', 'CNMD', 'NVRO', 'MMSI', 'HAE', 'ATRC', 'CLLKF', 'AHCO', 'CTKB', 'AXNX', 'ITGR', 'ANSLY', 'NUVA', 'ANSLF', 'TPGVF', 'NHNKY', 'OM', 'VMTHF', 'NSTG', 'SILK', 'GKOS', 'BFLY', 'IRTC', 'SDC', 'ESTA', 'BLFS', 'QTRX', 'PRCT', 'DGWPF', 'AVNS', 'LUNG', 'FNA', 'CSII', 'RBOT', 'KIDS', 'ATRI', 'NNCSF', 'SGHT', 'APR', 'LMAT', 'ATEC', 'XVIPF', 'TMCI', 'VRAY', 'NNOX', 'ANGO', 'VREX', 'CALZF', 'OMIC', 'SMLR', 'INGN', 'XENT', 'MASS', 'NTUS', 'CRY', 'CYBQY', 'MDXG', 'RPID', 'OSUR', 'SRDX', 'CUTR', 'TMDX', 'SIBN', 'OFIX', 'TCMD', 'PLSE', 'ATRS', 'ANIK', 'NYXH', 'IOBCF', 'AXGN', 'VAPO', 'SAFLF', 'SPNE', 'BTAVF', 'ITMMF', 'ITMR', 'PAVM', 'AKYA', 'APYX', 'IRMD', 'MSON', 'SOLY', 'ZYXI', 'STXS', 'AVHHL', 'ISO', 'OWLT', 'ASXC', 'LUCD', 'ARAY', 'APEN', 'CLPT', 'NPCE', 'UTMD', 'RVP', 'EAR', 'SIEN', 'CVRX', 'RXST', 'IPDQF', 'INFU', 'PROF', 'HBIO', 'SEOVF', 'DNAY',
               'CTSO', 'OPSSF', 'XAIR', 'VMD', 'AFIB', 'LHDX', 'HTLZF', 'CFMS', 'PLLWF', 'UEEC', 'BTCY', 'EDAP', 'TMDI', 'QIPT', 'TELA', 'SOMNF', 'IIN', 'IVC', 'MLSS', 'TLIS', 'NMRD', 'SRGA', 'BWAY', 'DMTRF', 'IRIX', 'EYES', 'KRMD', 'PXMBF', 'FONR', 'XTNT', 'VERO', 'MOVE', 'NVNO', 'ELMD', 'RCEL', 'PDEX', 'PYNKF', 'BIOL', 'ISR', 'BSGM', 'TBRIF', 'FEMY', 'RWLK', 'LNSR', 'POAI', 'VVOS', 'IGAP', 'NEPH', 'DCTH', 'AVGR', 'SRTS', 'ECOR', 'VPTDF', 'SSKN', 'MYO', 'RHNMF', 'BIEL', 'SNWV', 'AZYO', 'MODD', 'BLOZF', 'AEMD', 'NVCN', 'AMEUF', 'FZMD', 'MBOT', 'NURO', 'EKSO', 'LXXGF', 'BBLG', 'RSLS', 'NMTC', 'YBGJ', 'DXR', 'PAVMW', 'INVO', 'RTSL', 'NAOV', 'FORZ', 'MDGS', 'ATBPF', 'TLTFF', 'RDGL', 'HSDT', 'LNDZF', 'NSPR', 'GBS', 'INND', 'SINT', 'PEYE', 'ALRT', 'GMVD', 'DYNT', 'PMEDF', 'ODYY', 'PETV', 'VIVE', 'AHPI', 'RSCF', 'NUWE', 'RMED', 'THMO', 'IINN', 'EMITF', 'ASAPF', 'CLABF', 'SNANF', 'ECIA', 'PBIO', 'RMSL', 'LLBO', 'ORTIF', 'MHTX', 'CMXC', 'QTVLF', 'CBSC', 'MICR', 'IMTH', 'FLURF', 'ADMT', 'UAHC', 'GTHP', 'BRSF', 'OCLG', 'NUMD', 'SNDD', 'ABMT', 'POSC', 'SHOM', 'WCUI', 'BIIO', 'EMED', 'LCDX', 'VYCO', 'REMI', 'CHYPF', 'IMEXF', 'WHSI', 'VSMD', 'PGUZ', 'LBLTF', 'KLYG', 'CRRVF', 'VICA', 'ESMC', 'QTXB', 'EQUR', 'ECGI', 'GHSTD', 'BLFE', 'PDMI', 'BGMD', 'EMDF', 'ACAI', 'CYDX', 'EVARF', 'VRSEF', 'IGNT', 'HLTY', 'CEOS', 'MFST', 'HRAL', 'AVTI', 'SCIE', 'RGBOQ', 'GVDI', 'IINNW', 'MDGSW', 'XTNTW', 'BDXB', 'BBLGW', 'GMVDW', 'NVNOW', 'PAVMZ', 'BSX-PA', 'EYESW', 'NSPRZ', 'PETVW', 'IRME']
tickerUsDis = ['WBA', 'MCK', 'ABC', 'ALBHF', 'ALBBY', 'CAH', 'HSIC', 'SHTDY', 'SHTDF', 'SHPMY', 'SHPMF', 'RADLY', 'TSUSF', 'MAHLY', 'ARRJF', 'ZRSEF', 'PDCO', 'SAEYY', 'PBH', 'OMI', 'RAD', 'PETS', 'YI', 'HITI', 'FFLWF', 'LFMD', 'NVACF',
               'GNLN', 'GEG', 'PNPL', 'MEDS', 'CJJD', 'BIMI', 'KIARF', 'RXMD', 'GABLF', 'SSY', 'EXHI', 'HADV', 'HEWA', 'RLLVF', 'CHME', 'CNBI', 'OXIHF', 'PHRX', 'DECN', 'ITNS', 'CAFS', 'OMHE', 'ALST', 'AEGY', 'FSPM', 'SCRCQ', 'IWINF', 'LFMDP', 'HITTF']
tickerUsDrug = ['JNJ', 'RHHVF', 'RHHBY', 'RHHBF', 'PFE', 'LLY', 'MRK', 'AZNCF', 'AZN', 'ABBV', 'NVSEF', 'NVS', 'BMY', 'SNYNF', 'SNY', 'AMGN', 'MKKGY', 'MKGAF', 'GLAXF', 'ZTS', 'GSK', 'GILD', 'CHGCY', 'CHGCF', 'BAYZF', 'BAYRY', 'TKPHF', 'TAK', 'DSNKY', 'DSKYF', 'BIIB', 'ALPMF', 'ALPMY', 'HZNP', 'CTLT', 'OTSKY', 'ESALF', 'SGIOF', 'ESALY', 'SGIOY', 'SFOSF', 'KYKOF', 'VTRS', 'PPD', 'ELAN', 'GIKLY', 'GIFOF', 'GRFS', 'CSPCY', 'RCDTF', 'TEVA', 'OPHLY', 'BHC', 'RDY', 'CASBF', 'OGN', 'GNHAF', 'EVTCY', 'EVOTF', 'IPSEY', 'BIOVF', 'APNHY', 'HKMPY', 'CURLF', 'PRGO', 'ORINF', 'SNPHY', 'HLUKF', 'HLUYY', 'CGC', 'RGEDF', 'TLRY', 'GTBIF', 'TCNNF', 'PTKFF', 'TAIPY', 'HYPMY', 'EBS', 'IZQVF', 'TSMRF', 'TARO', 'INVVY', 'PCRX', 'DVAX', 'CRLBF', 'SHPHF', 'IRWD', 'CRON', 'BAYP', 'SUPN', 'ACB', 'ORGO', 'VEGPF', 'VRNOF', 'SNDL', 'AAWH', 'BKUH', 'AYRWF', 'BGAIF', 'CCHWF', 'PROC', 'ENDP', 'TRSSF', 'RDUS', 'PAHC', 'AMPH', 'AMRX', 'PLNHF', 'COLL', 'FFNTF', 'ABSCF', 'PETQ', 'OGI', 'AMYT', 'EGRX', 'TKNO', 'JUSHF', 'HLTRF', 'KHTRF', 'ZOM', 'ANIP', 'AERI', 'XXII', 'AVDL', 'FLXN', 'HEXO', 'MAYNF', 'EOLS', 'BDSI', 'ADMS', 'PLXP', 'THTX', 'NUNZ', 'TXMD', 'AGYTF', 'VLNCF', 'INCR', 'GRAMF', 'NLTX', 'ATNX', 'MDDVF', 'BILZF', 'RDHL', 'EOFBF', 'ACRDF', 'DRRX', 'HROW', 'ACRHF', 'KMDA', 'ABTI', 'MRMD', 'CWBHF', 'SLDB', 'GAEGF', 'GDNSF', 'IMCC', 'MMNFF', 'CRDL', 'RGC', 'FLGC', 'CLVR', 'CNPOF', 'NXSCF', 'CNTMF', 'AQST', 'ALID', 'BNIGF', 'ADMP', 'ZYNE', 'CBWTF', 'OPTN', 'ATHJF', 'INNPF', 'SOLCF', 'ORXOY', 'MOTNF', 'QLI', 'CNVCF', 'PCLOF', 'INLB', 'YCBD', 'SCYX', 'ERBB', 'RVVTF', 'ROMJF', 'RWBYF', 'RAFA', 'TLLTF', 'ACRX', 'LCI', 'AGRX', 'PKANF', 'LOVFF', 'NEPT', 'COPHF', 'GRVI', 'SHWZ', 'SISI', 'PRPH', 'CRXT', 'MDVL', 'MGCLF', 'CNTTQ', 'REPH', 'MJNA', 'CNGGF', 'TGODF', 'ALEAF', 'ICNAF', 'LOWLF', 'COSM', 'BIOYF', 'CXXIF', 'XPHYF', 'CNTRF', 'UNRV', 'DBCCF', 'TGGI', 'AVTBF', 'MYCOF', 'DXBRF', 'MVMDF', 'LSFP', 'CRYM', 'GRYN', 'VPHIF', 'ZOEIF', 'HUGE', 'MEDIF', 'IVIXF', 'NXGWF', 'SPBBF', 'TRUFF', 'CPHRF', 'SLGWF', 'CANSF', 'MEDXF', 'RMTI', 'HSTRF', 'STMH', 'ASPCF', 'INIS', 'SBFM', 'JUPW', 'LVCNF', 'ASRT', 'EXDI', 'VEXTF', 'BMMJ', 'NDVAF', 'CYTH', 'VIBEF', 'HERTF', 'EVOK', 'ITHUF', 'KHRNF', 'PMXSF', 'CPIX', 'ELTP', 'CURR',
                'FLHLF', 'HCAND', 'SCNA', 'CHALF', 'ACUR', 'AUSAF', 'BUDZ', 'JUVAF', 'AXRX', 'DLTNF', 'FLWPF', 'VVCIF', 'ACNNF', 'ETRGF', 'CBDHF', 'FLOOF', 'ALIM', 'WRHLF', 'HEMP', 'CLCFF', 'AVCNF', 'OILFF', 'CENBF', 'HBORF', 'TCNAF', 'GENH', 'MJNE', 'PTPI', 'INQD', 'CNNC', 'EXPFF', 'CVSI', 'GHSI', 'TGIFF', 'PRFX', 'CPHI', 'NSVGF', 'CHYL', 'USMJ', 'EDXC', 'GRUSF', 'ELLXF', 'SKYI', 'AZFL', 'CDCLF', 'LVRLF', 'GPFT', 'PHCG', 'RDDTF', 'CLSH', 'NLBS', 'VIVXF', 'CTABF', 'SCNNF', 'KOAN', 'EMHTF', 'PRXTF', 'HYEX', 'QEBR', 'CHOOF', 'NPHC', 'LVVV', 'MNKKQ', 'HRVOF', 'SXTC', 'SNOA', 'ATTBF', 'SBUDF', 'SRUTF', 'ELIXF', 'WUHN', 'CVGRF', 'MCOA', 'DUTV', 'UNVC', 'FIORF', 'LMLLF', 'AQSZF', 'CTTH', 'THCBF', 'MMJJF', 'SYUP', 'NUGS', 'MCIC', 'ISCNF', 'CANL', 'BMCS', 'PKPH', 'MPXOF', 'GTSIF', 'AGFAF', 'KGKG', 'GRPS', 'CBDS', 'CANB', 'BHNGF', 'CNFHF', 'TAUG', 'PHBI', 'NRXCF', 'CBDY', 'HENC', 'IGEX', 'NLVVF', 'BBRRF', 'LTTSF', 'VYYRF', 'SNNC', 'CPIVF', 'CBDNF', 'GBHPF', 'SEHCF', 'VNNYF', 'GENPF', 'NMLSF', 'VEGGF', 'JTBK', 'CWWBF', 'CANQF', 'OWPC', 'LRSV', 'LUFFF', 'CADMF', 'CAAOF', 'PACRF', 'TRLFF', 'IONKF', 'BIEI', 'TNRG', 'GSAC', 'THCT', 'IGPK', 'SPLIF', 'BHHKF', 'GRCU', 'SILFF', 'HPMM', 'BBBT', 'TLGTQ', 'NWYU', 'REZNF', 'TPPRF', 'MMJFD', 'EVRRF', 'EEVVF', 'DVLP', 'NXEN', 'BIOIF', 'CRFTF', 'RPNRF', 'STSN', 'ACUS', 'BSPK', 'VFRM', 'ANTCF', 'MYHI', 'AREVF', 'POTVF', 'GCAN', 'WSRC', 'PKBFF', 'EMGE', 'VDQSF', 'MGWFD', 'RMRK', 'KAYS', 'CPMD', 'HBRM', 'CNNXF', 'EVIO', 'VRTHF', 'RCMW', 'SLNX', 'CHMJF', 'ETST', 'NWPN', 'OVATF', 'PEMTF', 'GBLP', 'APPB', 'BLEVF', 'HEME', 'CSUI', 'SNNVF', 'SHMN', 'ANAS', 'HHPHF', 'TNPH', 'FAGI', 'CBGL', 'MJARF', 'TMSH', 'SIGO', 'MRRCF', 'NOUV', 'NGMC', 'NEUN', 'SPLM', 'QMDT', 'PJET', 'RVVQF', 'NNRX', 'GMVP', 'MNZO', 'QRXPF', 'POTN', 'CHNC', 'PZOO', 'HMPQ', 'TRCNF', 'RBII', 'OWCP', 'MSMY', 'MMJFF', 'EXMT', 'UBQU', 'FTEG', 'EAPH', 'ECOX', 'PRCNF', 'VDRM', 'DKSC', 'GGBXF', 'KGET', 'ADVT', 'CBDL', 'VCBDQ', 'RGST', 'WLDFF', 'IVITF', 'JWCAF', 'CVHIF', 'FITX', 'FWDG', 'KALY', 'CBGI', 'CNABQ', 'CNNA', 'JUPWW', 'KHRWF', 'GRMWF', 'NXGB', 'KHRWF', 'NHPHF', 'ECGS', 'SFLM', 'CRLWF', 'CYTHW', 'TCNWF', 'GLASF', 'CRXTW', 'PROCW', 'OMID', 'LVTTF', 'GHBWF', 'CLVRW', 'ELAT', 'INSO', 'TSVTV']
tickerUsSer = ['UNH', 'CVS', 'ANTM', 'CI', 'HUM', 'VEEV', 'MTHRY', 'CNC', 'TDOC', 'CERN', 'TXG', 'GDRX', 'MOH', 'DOCS', 'PIAHY', 'PANHF', 'NTEDY', 'OMCL', 'CHNG', 'INOV', 'RCM', 'BHG', 'HQY', 'PGNY', 'PINC', 'CMPUY', 'ONEM', 'PMCUF', 'SDGR', 'ALHC', 'OSCR', 'DH', 'PHR', 'MPLN', 'CLOV', 'AGTI', 'SGFY', 'CVET', 'ACCD', 'HCAT', 'SHCR', 'EVH', 'PRVA', 'MGLN', 'AMWL', 'SLGC', 'SMFR', 'MDRX', 'OPRX', 'SUSRF', 'HLTH', 'SNCE', 'CRWRF', 'NXGN', 'SOPH', 'HSTM', 'GTS', 'SLP', 'CMAX', 'TRHC', 'CNVY', 'CPSI', 'SY', 'FORA', 'COGZF', 'DOCRF', 'CSLT', 'ICAD', 'UPH', 'FBAYF', 'RSLBF', 'NH', 'NSAV', 'CLNH', 'RQHTF', 'MDXL',
               'EMOR', 'AUGX', 'TREIF', 'MTBCP', 'MTBC', 'MOST', 'HCTI', 'VHIBF', 'KERN', 'HDVY', 'STRM', 'MBCHF', 'HLYK', 'MITI', 'NEWUF', 'MNNDF', 'ZCMD', 'HDSLF', 'MSRT', 'ICCT', 'PBSV', 'MDNWF', 'CNONF', 'RYAHF', 'WORX', 'MDBIF', 'CRBKF', 'HRAA', 'CSOC', 'CRVW', 'DTRK', 'HSCHF', 'CDXFF', 'PFHO', 'VASO', 'EWLL', 'SPLTF', 'ICCO', 'CTVEF', 'HLTT', 'FUAPF', 'PPJE', 'CMPD', 'WTEQF', 'VNTH', 'HITC', 'USAQ', 'KALO', 'BNVIF', 'REFG', 'MDRM', 'ORHB', 'EKGGF', 'BNVID', 'NMXS', 'VMCS', 'AHGIF', 'EBYH', 'EVAHF', 'MDWK', 'LFCOF', 'PASO', 'ACNV', 'ESSI', 'SHCRW', 'CMAXW', 'CHNGU', 'KERNW', 'SLGCW', 'LVCE', 'SMFRW', 'UTRS']
tickerUsOth = ['TMO', 'DHR', 'DHR-PB', 'SMMNY', 'SEMHF', 'HCA', 'ILMN', 'LZAGY', 'LZAGF', 'IDXX', 'DXCM', 'IQV', 'A', 'RYLPF', 'PHG', 'MTD', 'JDHIF', 'FSNUY', 'FSNUF', 'LH', 'SSMXY', 'ERFSF', 'ICLR', 'WAT', 'PKI', 'CRL', 'FMS', 'DGX', 'EXAS', 'BMXMF', 'SKHHY', 'SKHCF', 'QGEN', 'DVA', 'GH', 'OSH', 'UHS', 'NTRA', 'AGL', 'SYNH', 'THC', 'SHC', 'CHE', 'ORPEF', 'EHC', 'MEDP', 'NVTA', 'EVGRF', 'TWST', 'PACB', 'QDEL', 'NEO', 'AMED', 'ACHC', 'OPCH', 'ME', 'AMN', 'LHCG', 'OCDX', 'SEM', 'NEOG', 'LFST', 'ENSG', 'CDNA', 'BUHPF', 'OLK', 'SGRY', 'AMEH', 'MYGN', 'FLGT', 'OPK', 'LTGHY', 'HSKA', 'MD', 'MODV', 'CANO', 'RDNT', 'CMPS', 'CSTL', 'LNTH', 'SENS', 'HCSG', 'NFH', 'BNR', 'BNGO', 'CYH', 'USPH', 'ADUS', 'AVAH', 'TVTY', 'BKD', 'GTH', 'JYNT', 'WLYYF', 'NRC', 'NHC', 'MXCT', 'INNV', 'RNLX', 'DMTK', 'RTNXF', 'PSNL', 'BVS', 'VIVO', 'LWSCF', 'CCRN', 'HNGR', 'PNTG', 'NOTV', 'ATIP', 'TALK', 'CO', 'EXETF', 'AXDX', 'FLDM', 'AWH', 'FTRP', 'SERA', 'NVYTF', 'DRIO', 'QTNT', 'CELC', 'SMTI', 'ICCM', 'CODX', 'MFCSF', 'CNTG', 'BDSX', 'TLMD', 'XGN', 'VNRX', 'CHHHF',
               'BGLC', 'OTRK', 'AKU', 'ENZ', 'PNHT', 'TTOO', 'IBXXF', 'STIM', 'FVE', 'ANIX', 'GBNH', 'SLHG', 'LKYSF', 'CCM', 'EPWCF', 'LDXHF', 'CCEL', 'MHIVF', 'AIH', 'CHEK', 'NHLG', 'AVCO', 'BIOQ', 'CLIFF', 'IONM', 'OPGN', 'DVCR', 'EDTXF', 'NDRA', 'CEMI', 'CSU', 'SQIDF', 'VLXC', 'BIOC', 'BMRA', 'ONVO', 'PRPO', 'GENE', 'ISPC', 'NVOS', 'PMD', 'TRIB', 'APDN', 'RYMDF', 'CGNSF', 'HTGM', 'SQL', 'NMHLY', 'IZOZF', 'IDXG', 'NVLPF', 'IMAC', 'GENN', 'TPIA', 'NVMDF', 'MOTS', 'TOMDF', 'BICX', 'PMSNF', 'TDSGF', 'SZLSF', 'GWHP', 'JNHMF', 'GBCSD', 'AMS', 'GBCS', 'BMKDF', 'AVCRF', 'STRR', 'RHE', 'BNKL', 'JMPHF', 'COPRF', 'SCAL', 'NSTM', 'JRSS', 'GRST', 'NOVC', 'TLIF', 'CLRD', 'IDTA', 'TOKIF', 'SPIN', 'DIGP', 'FCHS', 'KONEF', 'USNU', 'ABMC', 'MSGP', 'IVRO', 'GNOW', 'NAFS', 'XCRT', 'ICBU', 'NLAB', 'NRTSF', 'ARYC', 'RNVA', 'DRWN', 'ROSGQ', 'PRLX', 'PCHM', 'AMBD', 'ACMSY', 'SLDX', 'NXGT', 'NDRAW', 'RVLWF', 'STRRP', 'BNGOW', 'PAOG', 'TLMDW', 'TALKW', 'CHEKZ', 'IDGGW', 'SQLLW', 'NMNSF', 'DHR-PA', 'OTRKP', 'LMDX', 'WFHG', 'BDYS', 'MEUSW', 'IMACW', 'PHCI', 'LMDXW']
tickerTwBio = ['4743.TWO', '6547.TWO', '6550.TWO', '6589.TWO', '4128.TWO', '6446.TWO', '6617.TWO', '4174.TWO', '4142.TW', '6541.TW', '4147.TWO', '6712.TWO', '6586.TWO', '4192.TWO', '6492.TWO', '4157.TWO', '6696.TWO', '4162.TWO', '3176.TWO', '4167.TWO', '1760.TW', '6575.TWO', '4726.TWO', '1762.TW', '6535.TWO', '1734.TW', '4728.TWO', '6634.TWO', '4171.TWO', '6838.TWO', '6657.TWO', '6709.TWO', '4168.TWO', '6580.TWO',
               '6564.TWO', '8279.TWO', '4130.TWO', '4194.TWO', '6733.TWO', '1733.TW', '4133.TW', '6461.TWO', '1777.TWO', '3164.TW', '6827.TWO', '4169.TWO', '4186.TWO', '6652.TWO', '6808.TWO', '4911.TWO', '6794.TWO', '6814.TWO', '6610.TWO', '4732.TWO', '3118.TWO', '4195.TWO', '7427.TWO', '3205.TWO', '6662.TWO', '6549.TWO', '6810.TWO', '6236.TWO', '6566.TWO', '8490.TWO', '6744.TWO', '4197.TWO', '4131.TWO', '6848.TWO']
tickerTwDev = ['4123.TWO', '1795.TW', '1707.TW', '1789.TW', '4105.TWO', '6472.TWO', '4132.TWO', '3705.TW', '6576.TWO', '6562.TWO', '4119.TW', '4114.TWO', '1720.TW', '1701.TW', '4746.TW', '6620.TWO', '4108.TW', '4120.TWO',
               '6539.TWO', '4166.TWO', '6785.TWO', '1731.TW', '3054.TW', '4191.TWO', '8432.TWO', '4117.TWO', '1796.TWO', '1780.TWO', '6817.TWO', '6496.TWO', '7561.TWO', '4172.TWO', '6677.TWO', '4747.TWO', '4102.TWO', '4127.TWO', '6621.TWO']
tickerTwDis = ['6469.TWO', '4164.TW', '8403.TWO',
               '4175.TWO', '4173.TWO', '6637.TWO']
tickerTwDrug = ['4123.TWO', '1795.TW', '1707.TW', '1789.TW', '4105.TWO', '6472.TWO', '4132.TWO', '3705.TW', '6576.TWO', '6562.TWO', '4119.TW', '4114.TWO', '1720.TW', '1701.TW', '4746.TW', '6620.TWO', '4108.TW', '4120.TWO',
                '6539.TWO', '4166.TWO', '6785.TWO', '1731.TW', '3054.TW', '4191.TWO', '8432.TWO', '4117.TWO', '1796.TWO', '1780.TWO', '6817.TWO', '6496.TWO', '7561.TWO', '4172.TWO', '6677.TWO', '4747.TWO', '4102.TWO', '4127.TWO', '6621.TWO']
tickerTwSer = ['6841.TWO', '6569.TWO', '6665.TWO', '8409.TWO']
tickerTwOth = ['1784.TWO', '4139.TWO', '4153.TWO', '6615.TWO',
               '6645.TWO', '7595.TWO', '6661.TWO', '4160.TWO']
period1 = int(time.mktime(datetime.datetime(1979, 12, 31, 23, 59).timetuple()))
period2 = int(time.mktime(datetime.datetime(2021, 12, 31, 23, 59).timetuple()))
interval = '1d'  # 1d, 1m

for i in country:
    for j in industry:
        if i == 'china':
            if j == 'bio':
                for k in tickerChBio:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dev':
                for k in tickerChDev:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dis':
                for k in tickerChDis:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'drug':
                for k in tickerChDrug:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'ser':
                for k in tickerChSer:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'oth':
                for k in tickerChOth:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
        elif i == 'hk':
            if j == 'bio':
                for k in tickerHkBio:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dev':
                for k in tickerHkDev:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dis':
                for k in tickerHkDis:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'drug':
                for k in tickerHkDrug:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'ser':
                for k in tickerHkSer:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'oth':
                for k in tickerHkOth:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
        elif i == 'japan':
            if j == 'bio':
                for k in tickerJpBio:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dev':
                for k in tickerJpDev:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dis':
                for k in tickerJpDis:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'drug':
                for k in tickerJpDrug:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'ser':
                for k in tickerJpSer:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'oth':
                for k in tickerJpOth:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
        elif i == 'korea':
            if j == 'bio':
                for k in tickerKoBio:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dev':
                for k in tickerKoDev:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dis':
                for k in tickerKoDis:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'drug':
                for k in tickerKoDrug:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'ser':
                for k in tickerKoSer:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'oth':
                for k in tickerKoOth:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
        elif i == 'usa':
            if j == 'bio':
                for k in tickerUsBio:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dev':
                for k in tickerUsDev:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dis':
                for k in tickerUsDis:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'drug':
                for k in tickerUsDrug:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'ser':
                for k in tickerUsSer:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'oth':
                for k in tickerUsOth:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
        elif i == 'tw':
            if j == 'bio':
                for k in tickerTwBio:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dev':
                for k in tickerTwDev:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'dis':
                for k in tickerTwDis:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'drug':
                for k in tickerTwDrug:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'ser':
                for k in tickerTwSer:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
            elif j == 'oth':
                for k in tickerTwOth:
                    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{k}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
                    df = pd.read_csv(query_string)
                    df.to_csv(f'{pwd}\{i}\{j}\{k}.csv')
                    print(f'{i}{j}{k}.csv saved')
                    time.sleep(1)
