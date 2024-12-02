from rob import rob
import vis
import tkinter as tk

root = tk.Tk() 
robot = rob()
text = str(robot)
App = vis.FinishScreen(root, text)
root.mainloop() 


"""
robot = rob()
print(robot.get_value('cafpos'))
robot.set_value('cafpos',1)
print(robot.get_value('cafpos'))
print(robot)
print("Connected:", robot.connect())
robot.read_mod_data()
robot.disconnect()"""

"""
robot = rob()
print(robot.get_value('cafpos'))
robot.set_value('cafpos',1)
print(robot.get_value('cafpos'))
print(robot)
print("Connected:", robot.connect())
#robot.read_mod_data()
robot.read_mod_data()
robot.write_mod("coffeetype", 1)
robot.write_mod("cafpos", 5)
robot.write_mod("printer", 1)
robot.write_mod("dropoff", 1)
robot.read_mod_data()
jbi_filename="main"
print(robot.send_cmd("checkJbiExist",{"filename":jbi_filename}))
robot.send_cmd("runJbi", {"filename":jbi_filename})"""
