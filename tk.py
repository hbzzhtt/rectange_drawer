from tkinter import *

class ExampleApp(Frame):

    def __init__(self,master):
        Frame.__init__(self,master=None)

        # ------x------->
        # |
        # y
        # |
        # |
        # ~
        # tk axis is different from normal x-y axis 
        # so, position transform is need
        # for normal (x,y), x = x' , y = g_y_height - y', (x', y') is in tk axis
        
        self.g_height = self.g_width = 1000

        self.canvas = Canvas(self,  width=self.g_width, height=self.g_height)   
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<Button1-Motion>", self.on_move_press)
        self.canvas.bind("<Button1-ButtonRelease>", self.on_button_release)
        self.canvas.bind("<Button-3>", self.on_right_click)

        self.rect = None
        self.rect_txt = None
        self.start_x = None
        self.start_y = None

        self.canvas.grid()
        self.help = self.canvas.create_text(500, 30, text=f'use mouse left click for create rectange, move for expand rectange, use mouse right click for save rectange', font='Consolas 8', 
                                anchor='s')


 
    def on_right_click(self, event):
        self.rect = None
        self.rect_txt = None

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')
        if self.rect_txt:
            self.canvas.delete(self.rect_txt)
            self.rect_txt = None            

    def on_move_press(self, event):
        # positon transform from event axis to tk axis
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        # positon transform from event axis to tk axis
        event.x = self.canvas.canvasx(event.x)
        event.y = self.canvas.canvasy(event.y)

        left_bottom_x = min(self.start_x, event.x)
        left_bottom_y = min(self.start_y, event.y)
        right_top_x = max(self.start_x, event.x)
        right_top_y = max(self.start_y, event.y)

        txt_x = (left_bottom_x + right_top_x)/2
        txt_y = (left_bottom_y + right_top_y)/2

        # positon transform from tk axis to normal axis
        left_bottom_y = min(self.g_height - self.start_y, self.g_height - event.y)
        right_top_y = max(self.g_height - self.start_y, self.g_height - event.y)

        if not self.rect_txt:
            self.rect_txt = self.canvas.create_text( txt_x, 
                                txt_y,
                                text=f'start:({int(left_bottom_x)}, {int(left_bottom_y)})  ext:({int(right_top_x-left_bottom_x)},{int(right_top_y-left_bottom_y)})',
                                font='Consolas 8', 
                                anchor='s'
                                )

if __name__ == "__main__":
    root=Tk()

    app = ExampleApp(root)
    app.pack()

    root.mainloop() 
