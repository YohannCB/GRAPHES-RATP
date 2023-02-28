from utils import Utils
from displayer import display

s = Utils.import_stops()
print(s[1781])

adj_list = Utils.import_adjacency_list()
print(adj_list[1781])

display([1781, 1665])

for cle,valeur in s.items():
    if valeur[0]=="La Motte Picquet–Grenelle" and valeur[4]=="6":
        print(cle)

