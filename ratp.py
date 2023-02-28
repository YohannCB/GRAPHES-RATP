from utils import Utils
from displayer import display

s = Utils.import_stops()
print(s[1781])

adj_list = Utils.import_adjacency_list()
print(adj_list[1781])

display([1781, 1665])
    


def recherche_chemin(adj_list,id_depart,id_dest):
    stations=[]
    p= Pile()
    p.empile(id_depart)
    while p.est_vide()==False:
        id = p.depile()
        for i in adj_list[id]:
            if i not in stations:
                stations.append(i)
                p.empile(i)
            if i==id_dest:
                return stations

print()