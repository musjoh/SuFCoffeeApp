"""Visualisation for Coffee App"""
import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
from rob import rob
import time

class StartScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Welcome to the Coffee Order App!")
        self.master.geometry("900x1400")
        self.master.configure(bg="#f9f9f9")
        self.master.attributes("-fullscreen", True)
        #self.master.state('zoomed')

        # Load an image using PIL for cup Pos
        current_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        self.gifpath = os.path.join(current_dir, "picture", "wantacofe.gif")

        # Load the GIF and get frames
        self.frames = self.load_gif(self.gifpath)
        self.current_frame = 0

        # Create a label for the GIF
        self.welcomegif = tk.Label(self.master)
        self.welcomegif.pack(side="top", pady=20, padx=10)

        # Start the animation
        self.animate()

        # Create an OK button
        ok_button = tk.Button(self.master, text="Yes", command=self.open_coffee_app, width=15, font=("Helvetica", 20),bg="lightgray", borderwidth=5)
        ok_button.pack(pady=10)

    def load_gif(self, gif_path):
        """Load all frames of the GIF into a list."""
        img = Image.open(gif_path)
        frames = []
        
        try:
            while True:
                frame = ImageTk.PhotoImage(img.copy())
                frames.append(frame)
                img.seek(len(frames))  # Move to the next frame
        except EOFError:
            pass  # End of frames
        
        return frames

    def animate(self):
        """Update the label with the next frame."""
        if self.frames:
            frame = self.frames[self.current_frame]
            self.welcomegif.configure(image=frame)
            self.current_frame = (self.current_frame + 1) % len(self.frames)  # Loop back to first frame
            
            # Call this method again after a delay (in milliseconds)
            self.master.after(50, self.animate)  # Adjust delay as needed

    def open_coffee_app(self):
        self.master.destroy()  # Close the start screen
        app = CoffeeOrderApp()  # Open the coffee app

class CoffeeOrderApp:
    def __init__(self):
        self.robot = rob()

        self.root = tk.Tk()
        self.root.title("Coffee Order App")
        #self.root.attributes("-fullscreen", True)
        self.root.state('zoomed')
        self.backgroundcolour = "#f9f9f9"
        self.buttoncolour_up = "lightgray"
        self.buttoncolour_down = "lightblue"

        self.root.configure(bg=self.backgroundcolour)

        # Load an image using PIL for cup Pos
        current_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(current_dir, "picture", "CupHolder2.png")

        self.coffee_buttons = []
        self.cup_position_buttons = []
        self.drop_off_buttons = []

        self.create_frames()
        self.create_coffee_selection()
        self.create_cup_position_selection()
        self.create_drop_off_selection()
        self.create_action_buttons()
        self.create_output_box()

        # Initialize button colors
        self.update_button_colors(self.coffee_buttons, "Coffee")
        self.update_button_colors(self.cup_position_buttons, "Front Right")
        self.update_button_colors(self.drop_off_buttons, "No")

        self.root.after(60000, self.show_start_screen)
        self.root.mainloop() 

    def create_frames(self):
        self.coffee_frame = tk.Frame(self.root, bg=self.backgroundcolour)
        self.coffee_frame.pack(side='top', fill='both', padx=5, pady=5)

        self.cuppos_frame = tk.Frame(self.root, bg=self.backgroundcolour)
        self.cuppos_frame.pack(side='top', fill='both', padx=5, pady=5)

        self.dropoff_frame = tk.Frame(self.root, bg=self.backgroundcolour)
        self.dropoff_frame.pack(side='top', fill='both', padx=5, pady=5)

    def create_coffee_selection(self):
        coffee_label = tk.Label(self.coffee_frame, text="Select Coffee Type:", font=("Helvetica", 24), anchor='w', bg=self.backgroundcolour)
        coffee_label.pack(side='top', anchor='w')

        coffee_buttons_frame = tk.Frame(self.coffee_frame, bg=self.backgroundcolour)
        coffee_buttons_frame.pack(side='top', anchor='w')

        coffee_options = [("Coffee", 0), ("Cappuccino", 1)]
        
        for text, value in coffee_options:
            button = tk.Button(coffee_buttons_frame, text=text, font=("Helvetica", 20),
                               command=lambda t=text, v=value: self.select_coffee(t, v),
                               bg=self.buttoncolour_up, borderwidth=5, relief=tk.RAISED, width=15)
            button.grid(row=0, column=len(self.coffee_buttons), padx=5, pady=5)
            self.coffee_buttons.append(button)

    def create_cup_position_selection(self):
        cuppos_label = tk.Label(self.cuppos_frame, text="Select Cup Position:", font=("Helvetica", 24), anchor='w', bg=self.backgroundcolour)
        cuppos_label.pack(side='top', anchor='w')

        cuppos_hint = tk.Label(self.cuppos_frame, text="Please check that cup holders are stocked.", font=("Helvetica", 16), anchor='w', bg=self.backgroundcolour)
        cuppos_hint.pack(side='top', anchor='w')

        image = Image.open(self.image_path)
        resized_image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(resized_image)

        cuppos_image = tk.Label(self.cuppos_frame, image=photo, bg=self.backgroundcolour)
        cuppos_image.image = photo  # Keep a reference to avoid garbage collection
        cuppos_image.pack(side='top', anchor='w')

        cup_position_options = [("Back Left", 5), ("Back Right", 4), ("Middle Left", 3), ("Middle Right", 2),
                                ("Front Left", 1), ("Front Right", 0)]

        cuppos_button_frame = tk.Frame(self.cuppos_frame, bg=self.backgroundcolour)
        cuppos_button_frame.pack(side='top', anchor='w')

        for text, value in cup_position_options:
            button = tk.Button(cuppos_button_frame, text=text, font=("Helvetica", 20),
                               command=lambda t=text, v=value: self.select_cup_position(t, v),
                               bg=self.buttoncolour_up, borderwidth=5, relief=tk.RAISED, width=15)
            button.grid(row=len(self.cup_position_buttons) // 2 + 1,
                        column=len(self.cup_position_buttons) % 2,
                        padx=5, pady=5)
            self.cup_position_buttons.append(button)

    def create_drop_off_selection(self):
        dropoff_label = tk.Label(self.dropoff_frame, text="Print Logo:", font=("Helvetica", 24), anchor='w', bg=self.backgroundcolour)
        dropoff_label.pack(side='top', anchor='w')

        dropoff_button_frame = tk.Frame(self.dropoff_frame, bg=self.backgroundcolour)
        dropoff_button_frame.pack(side='top', anchor='w')

        drop_off_options = [("No", 0), ("Yes", 1)]

        for text, value in drop_off_options:
            button = tk.Button(dropoff_button_frame, text=text, font=("Helvetica", 20),
                               command=lambda t=text, v=value: self.select_drop_off(t, v),
                               bg=self.buttoncolour_up, borderwidth=5, relief=tk.RAISED, width=15)
            button.grid(row=1,column=len(self.drop_off_buttons), padx=(5))
            self.drop_off_buttons.append(button)

    def create_action_buttons(self):
        button_frame = tk.Frame(self.root, bg=self.backgroundcolour)
        button_frame.pack(pady=(20), padx=(5), anchor='w')

        start_button = tk.Button(button_frame,width=(15), height=(2), text=("Start"),
                                 command=self.start_action,
                                 font=("Helvetica", 20), bg=("lightgreen"),
                                 borderwidth=(5), relief=tk.RAISED)
        
        start_button.grid(row=(0), column=(1), padx=(5), sticky='w')

        test_button = tk.Button(button_frame,width=(15), height=(2), text=("Test Connection"),
                                command=self.run_test,
                                font=("Helvetica", 20), bg=("grey"),
                                borderwidth=(5), relief=tk.RAISED)
        
        test_button.grid(row=(0), column=(0), padx=(5), sticky='w')

    def create_output_box(self):
        self.output_text = tk.Text(self.root,height=(10), width=(50),
                                    font=("Helvetica", 16))
        
        self.output_text.pack(pady=20,padx=5,anchor='w')

    def select_coffee(self, option_text, value):
        self.robot.set_value("coffeetype", value)
        self.update_button_colors(self.coffee_buttons, option_text)
        print(f"Selected Coffee: {option_text}")
        
    def select_cup_position(self, option_text,value):
        self.robot.set_value("cafpos", value)
        self.update_button_colors(self.cup_position_buttons, option_text)
        print(f"Selected Cup Position: {option_text}")

    def select_drop_off(self, option_text,value):
        self.robot.set_value("dropoff", 0)
        self.robot.set_value("printer", value)
        self.update_button_colors(self.drop_off_buttons, option_text)
        print(f"Selected Drop Off: {option_text}")

    def update_button_colors(self, buttons_list, selected):
       for button in buttons_list:
           if button['text'] == selected:
               button.config(bg=self.buttoncolour_down, relief=tk.SUNKEN)
           else:
               button.config(bg=self.buttoncolour_up, relief=tk.RAISED)

    def start_action(self):
        #self.show_finish_screen()
        self.output_text.delete(1.0, tk.END)
        success, mode = self.robot.test_connection()
        self.output_text.insert(tk.END, "Connected to robot.\n")
        #self.output_text.insert(tk.END, "Robot is in state: " + str(mode)+ ". State 2 is Rmote and ready to go\n")
        if mode != 2:
            self.output_text.insert(tk.END, "Attention Robot is not in Remote Mode! Can not recive data or get started remotly! Switch to Remot Mode first!")
        elif self.robot.connect():
            self.output_text.insert(tk.END, "Send data to Robot.\n")
            self.robot.write_mod("coffeetype", self.robot.get_value("coffeetype"))
            self.robot.write_mod("cafpos", self.robot.get_value("cafpos"))
            self.robot.write_mod("printer", self.robot.get_value("printer"))
            self.robot.write_mod("dropoff", self.robot.get_value("dropoff"))
            self.robot.read_mod_data()
            success = self.robot.write_start()
            if success:
                self.output_text.insert(tk.END, "Production Started.\n")
                print("Production Started.\n")
                time.sleep(3)
                self.show_finish_screen()
            else:
                self.output_text.insert(tk.END, "Could not start production.\n")
                print("Could not start production.\n")
        else:
            self.output_text.insert(tk.END, "Connection failed.\n")
            print("Connection failed.\n")

    def run_test(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Connect to robot.\n")
        success, mode = self.robot.test_connection()
        if success:
            self.output_text.insert(tk.END, "Connected to robot.\n")
            self.output_text.insert(tk.END, "Robot is in state: " + str(mode)+ "\n")
            if mode != 2:
                self.output_text.insert(tk.END, "Attention Robot is not in Remote Mode! Can not recive data or get started remotly! Switch to Remot Mode first!")
        else:
            self.output_text.insert(tk.END, "Failed to connect to robot.\n")
        print("Test connection finished")

    def show_finish_screen(self):
        self.root.destroy()
        finish_screen = FinishScreen(tk.Tk(),str(self.robot))
        
    def show_start_screen(self):
        self.root.destroy()
        finish_screen = StartScreen(tk.Tk())

class FinishScreen():
    def __init__(self, master, outputtext= ""):
        self.master = master
        self.master.title("Finish Screen")
        self.master.configure(bg="#f9f9f9")
        self.outputtext = outputtext
        
        # Set window size
        self.master.geometry("500x900")
        self.master.attributes("-fullscreen", True)
        #self.master.state('zoomed')

        # Load an image for the finish screen (replace with your image path)
        current_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "picture", "finish_image.png")  # Replace with your actual image path
        
        finish_image = Image.open(image_path)
        #finish_image = finish_image.resize((400, 300))  # Resize as needed
        self.finish_image_tk = ImageTk.PhotoImage(finish_image)

        # Create a "New Coffee" button
        new_coffee_button = tk.Button(self.master, text="New Coffee", command=self.new_coffee_order, width=15, font=("Helvetica", 20), bg="lightgray", borderwidth=5)
        new_coffee_button.pack(pady=5)

        # Create a label for the image
        image_label = tk.Label(self.master, image=self.finish_image_tk)
        image_label.pack(pady=5)
        
        # Create an emergency button (red)
        emergency_button = tk.Button(self.master, text="Emergency STOP", bg="red", fg="white", command=self.emergency_stop, width=15, font=("Helvetica", 20), borderwidth=5)
        emergency_button.pack(pady=5)

        # Create a "back to start pose" button
        new_coffee_button = tk.Button(self.master, text="Back to Start Pose", command=self.startpose, width=15, font=("Helvetica", 20), bg="lightgray", borderwidth=5)
        new_coffee_button.pack(pady=5)


        # Output Box for Order feedback
        """self.output_text = tk.Text(self.master,height=(10), width=(50),
                                    font=("Helvetica", 16))
        
        self.output_text.pack(pady=20,padx=5,anchor='w')
        self.output_text.insert(tk.END, self.outputtext)"""

        # Set a timer to close this screen and return to start screen after 2 minutes (120000 milliseconds)
        self.master.after(120000, self.close_application)  # Automatically close after 20 sec

    def emergency_stop(self):
        robot=rob()
        robot.emergencystop()

    def startpose(self):
        robot=rob()
        robot.gobacktoStart()


    def close_application(self):
        """Close the application."""
        self.master.destroy()  # Close this window
        app = StartScreen(tk.Tk()) #Open startscreen

    def new_coffee_order(self):
        """Open a new CoffeeOrderApp instance."""
        self.master.destroy()  # Close this window
        app = CoffeeOrderApp()  # Open a new coffee order app
