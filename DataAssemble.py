from TaMainFrame import TaMainFrame
from IndexMainFrame import IndexMainFrame
from TickMainFrame import TickMainFrame
import pandas as pd
import time

#IndexFrame = IndexMainFrame('000001', 730, 30, 90, 0.1)
#D2 = IndexFrame.data_assemble(alist)

alist = [5, 10, 30, 60, 90]
ticklist = ['600000', '600008', '600009', '600010', '600011', '600015', '600016', '600018', '600019', '600021', '600023', '600028', '600029', '600030', '600031', '600036', '600038', '600048', '600050', '600061', '600066', '600068', '600074', '600085', '600089', '600100', '600104', '600109', '600111', '600115', '002558', '002572', '002594', '002601', '002602', '002608', '002624', '002673', '002714', '002736', '002739', '002797', '002831', '002839', '002841', '300003', '300015', '300017', '300024', '300027', '300033', '300059', '300070', '300072', '300122', '300124', '300136', '300144', '300251', '300315']
#ticklist = ['600000', '600008']
i = int(0)
for value in ticklist:
    TaFrame = TaMainFrame(value, 730, 30, 90, 0.2)
    TickFrame = TickMainFrame(value, 730, 30, 90, 0.2)
    D1 = TaFrame.Pattern_Recognition_Functions()
    D3 = TickFrame.data_assemble(alist)
    print(value)
    if i==0:
        df = pd.concat([D1,D3],axis=1)
        out = df
    else:
        df = pd.concat([D1, D3], axis=1)
        out = pd.concat([out,df])
    i = i+1

out.to_csv(time.strftime('%Y-%m-%d',time.localtime(time.time()))+'Assemble.csv')
