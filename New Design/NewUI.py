from tkinter import *
from tkinter import ttk

"""
? not sure if using tkinter is possible
TODO: Implement sliders, Map to buttons, figure out how to implement camera, replace pygame
! Will make sepparate branch when implementing to initialRelease.py, because I'm afraid to break shitt
"""

def btn_clicked():
    print("Button Clicked")

def main():
    window = Tk()

    window.geometry("1000x600")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(
        window,
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
    current_value = tk.DoubleVar()

    def get_current_value():
        return '{: .2f}'.format(current_value.get())


    def slider_changed(event):
        value_label.configure(text=get_current_value())

    # Slider
    sliderVertical = ttk.Scale(
        window,
        from_=0,
        to=100,
        orient='vertical',  # vertical
        command=slider_changed,
        variable=current_value
    )

    # Plotting the slider
    sliderVertical.place(
        x = 800, y = 300,
        width = 80,
        height = 400
    )

    img0 = PhotoImage(file = f"New Design\\img0.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
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
        command = btn_clicked,
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
        command = btn_clicked,
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
        command = btn_clicked,
        relief = "flat")

    b3.place(
        x = 78, y = 418,
        width = 78,
        height = 80)

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    main()