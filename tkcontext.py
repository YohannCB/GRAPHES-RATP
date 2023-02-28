from tkinter import Tk, Toplevel, Canvas, Button, Text, END, Entry, StringVar, font, ttk, Label, Menu, Frame, END, RIGHT, Y, Scrollbar

class TkContext :

    FONT = None
    GREEN = "#30B030"
    Y_GRAY = "#908040"
    
    def __init__(self, displayer, w, h):
        self.window = Tk()
        self.displayer = displayer
        
        TkContext.FONT = font.Font(family='DejaVu Sans', size=16)    
        
        self.window.geometry("%sx%s+20+20"%(w+200, h))
        self.canvas = Canvas(self.window, width=w, height=h, bg="lightgray")
        self.canvas.place(x=200, y=0)


        y_scroll = Scrollbar(self.window)
        y_scroll.place(x=200, y=0, height=h)
        self.text = Text(self.window, wrap="none", yscrollcommand=y_scroll.set)
        
        y_scroll.config(command=self.text.yview)

        self.text.place(x=0, y=0, width=200, height=h)
        self.text.insert(END, displayer.get_info())
        self.text.configure(state="disabled")
        
        
        self.bind()
        
        self.menu_bar = Menu(self.window)
        self.window["menu"] = self.menu_bar
        
        file_menu = Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Outils", menu=file_menu, underline=0)
        
        self.menus = [file_menu]
        
    def mainloop(self):        
        self.window.mainloop()

    def add_menu_command(self, idx, label, command, acc="", shortcut=None):
        menu = self.menus[idx]
        menu.add_command(label=label, command=command, accelerator=acc, underline=0)
        if shortcut:
            self.window.bind_all(shortcut, lambda _ : command())

    def bind(self):
        self.mouse = None
        self.canvas.bind("<Button-1>", lambda ev : self.button_down(ev))
        self.canvas.bind("<Button-3>", lambda ev : self.button_down(ev))

        self.canvas.bind("<ButtonRelease-1>", lambda ev : self.button_up(ev))
        self.canvas.bind("<ButtonRelease-3>", lambda ev : self.button_up(ev))

        self.canvas.bind("<Motion>", lambda ev : self._motion(ev))

        
    def button_down(self, event):
        self.mouse = event.x, event.y, event.num

    def button_up(self, event):
        self.mouse = None
        
    def _motion(self,  event):
        if self.mouse is None :
            return
        mx, my, button = self.mouse
        ex, ey = event.x, event.y
        self.motion(ex, ey, ex - mx, ey - my, button)
        self.mouse = ex, ey, button
        
    def motion(self, ex, ey, dx, dy, button):
        self.displayer.move(dx, dy)
