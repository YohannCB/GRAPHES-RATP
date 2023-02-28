class Utils:

    def import_stops():
        """ Renvoie un dictionnaire décrivant les arrêts du métro parisien.
            Clés : id de l'arrêt (int)
            Valeurs : informations sur l'arrêt (list)
                      station, adresse, latitude, longitude, ligne """
        stops = dict()
        f = open("stops.tsv")
        for line in f.readlines():
            values = line[:-1].split("\t")
            key = int(values.pop(0))
            stops[key] = values
        f.close()
        return stops
        
    def import_adjacency_list():
        """ Renvoie la liste d'adjacence relative 
            aux arrêts du métro parisien.
            Clés : id de l'arrêt (int)
            Valeurs : ids des arrêts (list(int))
        """
        adj_list = dict()
        stops = Utils.import_stops()
        for key in stops.keys():
            adj_list[key] = []
        
        f = open("network.csv")
        for line in f.readlines():
            values = line[:-1].split(",")
            key = int(values[0])
            adj_list[key].append(int(values[1]))
        f.close()
        return adj_list

    def import_weighted_adjacency_list():
        """ Renvoie la liste d'adjacence relative 
            aux arrêts du métro parisien.
            Clés : id de l'arrêt (int)
            Valeurs : ids des arrêts (list(int))
        """
        adj_list = dict()
        stops = Utils.import_stops()
        for key in stops.keys():
            adj_list[key] = []
        
        f = open("network.csv")
        for line in f.readlines():
            values = line[:-1].split(",")
            key = int(values[0])
            neighbor = int(values[1])
            weight = int(values[2])
            adj_list[key].append((neighbor, weight))
        f.close()
        return adj_list

