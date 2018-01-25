from TaMainFrame import TaMainFrame
from IndexMainFrame import IndexMainFrame
from TickMainFrame import TickMainFrame


alist = [5, 10, 30, 60, 90]
TaFrame = TaMainFrame('600519', 730, 30, 90, 0.1)
D1 = TaFrame.Pattern_Recognition_Functions()

IndexFrame = IndexMainFrame('000001', 730, 30, 90, 0.1)
D2 = IndexFrame.data_assemble(alist)
#
TickFrame = TickMainFrame('600519', 730, 30, 90, 0.1)
D3 = TickFrame.data_assemble(alist)

d4 = pd.concat([D1,D2,D3],axis=1)