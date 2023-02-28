from tkcontext import TkContext
from utils import Utils

class Displayer :

    line_colors = {"1" : "#FFCD00",
                   "2" : "#003CA6",
                   "3" : "#837902",
                   "4" : "#be418d",
                   "5" : "#ff7f32",
                   "6" : "#6eca97",
                   "7" : "#f59bbb",
                   "8" : "#e19bdf",
                   "9" : "#b6bd00",
                   "10" : "#c9910d",
                   "11" : "#704b1c",
                   "12" : "#007852",  
                   "13" : "#6ec4e8",
                   "14" : "#62259d",
                   "3b" : "#6EC4E8",
                   "7b" : "#6eca97"
                  }
    
    def __init__(self, path, w, h):
        self.wh = w, h
        self.dx, self.dy = 0, 0
        self.unit = min(w, h)*5
        self.display_path = True
        self.display_stations = 0
        self.stops = Utils.import_stops()
        self.adj_list = Utils.import_adjacency_list()

        self.path, self.broken_path = self.check_path(path)
                
        self.stations_coords = self.get_stations()
        self.edges = self.get_edges()
        
        

        self.tk = TkContext(self, w, h)
        self.tk.add_menu_command(0, "Zoom in", self.zoom_in, "Ctrl+I", "<Control-i>")
        self.tk.add_menu_command(0, "Zoom out", self.zoom_out, "Ctrl+O", "<Control-o>")
        self.tk.add_menu_command(0, "Afficher/Cacher les stations", self.toggle_display_stations, "Ctrl+S", "<Control-s>")
        self.tk.add_menu_command(0, "Afficher/Cacher le chemin", self.toggle_display_path, "Ctrl+A", "<Control-a>")
        self.tk.add_menu_command(0, "Quitter", self.quit, "Ctrl+Q", "<Control-q>")


        self.draw()
        self.tk.mainloop()

    def get_info(self):
        if not self.path:
            return "Aucun chemin"

        if self.broken_path:
            s1, s2 = self.broken_path
            st1 = self.stops[s1][0]
            st2 = self.stops[s2][0]
            info = "Chemin incorrect !\n"
            info += "Impossible de joindre \n  %s (%s) \n  à\n  %s (%s)\n"%(s1, st1, s2, st2)
        else:
            info = "Chemin correct !\n"


        current = self.stops[self.path[0]]
        info += "\nDépart de %s - %s\n"%(self.path[0], current[0])
        for stop_id in self.path[1:]:
            next = self.stops[stop_id]
            info += "%s - %s\n"%(stop_id, next[0])
            current = next
        return info
    
    def toggle_display_path(self):
        self.display_path = not self.display_path
        self.draw()

    def toggle_display_stations(self):
        self.display_stations = (self.display_stations+1)%3
        self.draw()
        
    def zoom_in(self):
        self.zoom(1.5)
        
    def zoom_out(self):
        self.zoom(1/1.5)
        
    def zoom(self, factor):
        self.unit *= factor
        self.stations_coords = self.get_stations()
        self.edges = self.get_edges()
        self.draw()


    def check_path(self, path):
        if not path:
            return [], None
        current = path[0]
        valid_path = [current]
        for stop_id in path[1:]:
            next = stop_id
            if next not in self.adj_list[current]:
                return valid_path, (current, next)
            current = next
            valid_path.append(next)
        return valid_path, None

    def quit(self):
        self.tk.window.destroy()
        
    def move(self, dx, dy):
        self.dx += dx
        self.dy += dy
        self.draw()
        
    def shift(self, p):
        x, y = p
        return int(x+self.dx), int(y+self.dy)
        
    def draw(self):
        canvas = self.tk.canvas
        canvas.delete("all")

        if self.path and self.display_path:
            current = self.stations_coords[self.stops[self.path[0]][0]]
            for stop_id in self.path[1:]:
                next = self.stations_coords[self.stops[stop_id][0]]
                sx, sy = self.shift(current)
                ex, ey = self.shift(next)
                canvas.create_line(sx, sy, ex, ey, width=4, fill="white")
                current = next            
        
        for start, end, color in self.edges.values():
            sx, sy = self.shift(start)
            ex, ey = self.shift(end)
            canvas.create_line(sx, sy, ex, ey, width=2, fill=color)

        r = 3
        for p in self.stations_coords.values():
            x, y = self.shift(p)
            obj = canvas.create_oval(x-r, y-r, x+r, y+r, fill='white')
            
        stations_info = {}            
        if self.display_stations==1:
            for stop, info in self.stops.items():
                station = info[0]
                p = self.shift(self.stations_coords[station])
                stations_info[p] = station

        if self.display_stations==2:
            for stop, info in self.stops.items():
                station = info[0]
                p = self.shift(self.stations_coords[station])
                stops = stations_info.get(p)
                if stops:
                    stations_info[p] = "%s, %s"%(stops, stop)
                else:
                    stations_info[p] = "%s"%(stop)
        for p, info in stations_info.items():
            x, y = p
            canvas.create_text(x, y, text=info)

    def get_edges(self):
        edges = {}
        for start_id, neighbors_id in self.adj_list.items():
            for end_id in neighbors_id:
                edge_id = start_id, end_id
                if edge_id not in edges:
                    start = self.stops[start_id]
                    end = self.stops[end_id]
                    if start[0]!=end[0] and start[4]==end[4]:
                        start_coords = self.stations_coords[start[0]]
                        end_coords = self.stations_coords[end[0]]
                        color = Displayer.line_colors[start[4]]
                        edges[edge_id] = (start_coords, end_coords, color)
        return edges
      
    def get_stations(self):
        w, h = self.wh
        s = self.unit

        stations_coords = {}
        for stop, info in self.stops.items():
            station = info[0]
            if station not in stations_coords:
                lat = float(info[2])
                lon = float(info[3])
                coords = w//2+s*(lon-2.35), h//2-s*(lat-48.86)
                stations_coords[station] = coords
        return stations_coords
        
def display(path=None, w=800, h=600):
    Displayer(path, w, h)
