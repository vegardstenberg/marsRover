from tkinter import *
from tkinter import ttk
import roboclaw as RC
import marsRover as rover
"""
? not sure if using tkinter is possible
TODO: Map to buttons, figure out how to implement camera, replace pygame
! Will make sepparate branch when implementing to initialRelease.py, because I'm afraid to break shitt
"""


def Wbtn_clicked():
    print("W Button Clicked")
    RC.drive(kwargs["speed"])

def Abtn_clicked():
    print("A Button Clicked")
    RC.turn_left(kwargs["speed"])

def Sbtn_clicked():
    print("S Button Clicked")
    RC.reverse(kwargs["turning"])

def Dbtn_clicked():
    print("D Button Clicked")
    RC.turn_right(kwargs["turning"])

def main():
    root = Tk()

    root.geometry("1000x600")
    root.configure(bg = "#FFFFFF")
    canvas = Canvas(
        root,
        bg = "#FFFFFF",
        height = 600,
        width = 1000,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"New Design\\background.png")
    background = canvas.create_image(
        499.0, 299.0,
        image=background_img)

    # slider current value
    current_value = DoubleVar()
    current_value2 = DoubleVar()

    def get_current_value():
        return '{: .2f}'.format(current_value.get())

    value_label = ttk.Label(
        root,
        text=get_current_value()
    )

    def get_current_value2():
        return '{: .2f}'.format(current_value2.get())

    value_label2 = ttk.Label(
        root,
        text=get_current_value2()
    )

    def sliderVertical_changed(event):
        value_label.configure(text = get_current_value())
        print(f"Curent Vertical Slider Value: {str(get_current_value())}")

    def sliderHorizontal_changed(event):
        value_label.configure(text = get_current_value())
        print(f"Curent Horizontal Slider Value: {str(get_current_value2())}")


    style = ttk.Style()
    style.configure("TScale", background = "#808080")

    # style = ttk.Style root)

    # Import the tcl file with the tk.call method
    #   root.tk.call(")  # Put here the path of your theme file

    # Set the theme with the theme_use method
    # style.theme_use("breeze-dark")  # Theme files create a ttk theme, here you can put its name

    # Slider
    sliderVertical = ttk.Scale(
        root,
        from_ = 100,
        to = 0,
        orient = 'vertical',  # vertical
        command = sliderVertical_changed,
        variable = current_value,
        style = "TScale",
    )

    # Plotting the slider
    sliderVertical.place(
        x = 900, y = 10,
        width = 86,
        height = 578,
    )

    # Slider2
    sliderHorizontal = ttk.Scale(
        root,
        from_ = 0,
        to = 100,
        orient = 'horizontal',  # vertical
        command = sliderHorizontal_changed,
        variable = current_value2,
        style = "TScale",
    )

    # Plotting the slider2
    sliderHorizontal.place(
        x = 10, y = 502,
        width = 877,
        height = 86,
    )

    img0 = PhotoImage(file = f"New Design\\img0.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = Wbtn_clicked,
        relief = "flat")

    b0.place(
        x = 78, y = 341,
        width = 78,
        height = 80)

    img1 = PhotoImage(file = f"New Design\\img1.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = Dbtn_clicked,
        relief = "flat")

    b1.place(
        x = 153, y = 418,
        width = 75,
        height = 80)

    img2 = PhotoImage(file = f"New Design\\img2.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = Abtn_clicked,
        relief = "flat")

    b2.place(
        x = 1, y = 418,
        width = 80,
        height = 80)

    img3 = PhotoImage(file = f"New Design\\img3.png")
    b3 = Button(
        image = img3,
        borderwidth = 0,
        highlightthickness = 0,
        command = Sbtn_clicked,
        relief = "flat")

    b3.place(
        x = 78, y = 418,
        width = 78,
        height = 80)

    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()
