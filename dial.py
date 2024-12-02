# Define Variables
# Define register space for Variables on Robot Machine in B, 3rd Value
# Built send and read function
import time
import socket
import json
import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

# Define the slave IP and port
slave_ip = '192.168.1.200'
slave_port = 502

# Data Name, Data Value, Data position in B Variable in robot local storage
data = [
    ['cafpos', 0, 0],
    ['coffeetype', 0, 1],
    ['printer', 0, 2],
    ['dropoff', 0, 3],
    ['startsignal',0, 5],
]

avData = {}
for index, i in enumerate(data):
    avData[i[0]] = index

def setCoffeetype(value: int):
    data[1][1]=value
def getCoffeetype():
    return data[1][1]
def setPrinter(value: int):
    data[2][1]=value
def getPrinter():
    return data[2][1]
def setDropoff(value: int):
    data[3][1]=value
def getDropoff():
    return data[3][1]
def setCafpos(value: int):
    data[4][1]=value
def getCafpos():
    return data[4][1]
 
def connectETController(ip,port=8055):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((ip,port))
		return (True,sock)
	except Exception as e:
		sock.close()
		return (False,False)
		
def disconnectETController(sock):
	if(sock): 
		sock.close()
		sock=None
	else:
		sock=None
		
def sendCMD(sock,cmd,params=None,id=1):
	if(not params):
		params=[]
	else:
		params=json.dumps(params)
	sendStr = '{"method":"' + cmd + '","params":' + str(params) + ',"jsonrpc":"2.0","id":' + str(id) + '}\n'
	try:
		sock.sendall(bytes(sendStr,"utf-8"))
		ret=sock.recv(1024)
		jdata=json.loads(str(ret,"utf-8"))
		if("result" in jdata.keys()):
			return (True,json.loads(jdata["result"]),jdata["id"])
		elif("error" in jdata.keys()):
			return (False,jdata["error"],jdata["id"])
		else:
			return (False,None,None)
	except Exception as e:
		return (False,None,None)
      
def testconnect():
    # Create a Modbus TCP client
    robot_ip="192.168.1.200"
    command_text = "Test Connection"
    print (command_text)
    conSuc,sock=connectETController(robot_ip)
    
    # Check if the connection was successful
    if conSuc:
        # Get robot status
        command_text="Connected to Robot at {}".format(sock)
        print (command_text)
        suc, result, id = sendCMD(sock, "getRobotState")
        # Print results
        command_text="RobotState %s" %result
        print (command_text)
        suc, result, id = sendCMD(sock, "getRobotMode")
        command_text="RobotMode %s" %result
        print (command_text)
        if result != 2:
            command_text="Attention Robot is not in Remote Mode! Can not recive data or get started remotly! Switch to Remot Mode first!"
            print (command_text)
        return True, command_text
    else:
        command_text="No connection to Robot"
        return False, command_text

def readModData(client):
    for i in data:
        suc, result, id = sendCMD(client, "getSysVarB",{"addr":i[2]})
        if isinstance(result, int):
            i[1] = result
            print(f"Current {i[0]} is: {i[1]}")
        elif result.get('code') == -32601:
            print("Error: Method in readModData not found")

def writeMod(client, what, value):
    if what in avData:
        sendCMD(client, "setSysVarB",{"addr":data[avData[what]][2] ,"value":value})
        print(data[avData[what]][2])
        print(f'{what} value changed to: {value}')
    else:
        print(f'{what} is not definded data')

def writeStart(client):
    jbi_filename="main"
    suc, result, id = sendCMD(client,"checkJbiExist",{"filename":jbi_filename})
    print(suc, result)
    if suc and result == 1:
        suc, result, id = sendCMD(client, "runJbi", {"filename":jbi_filename})
        print(suc, result)

def writeCoffeetype(client, value=int):
    writeMod(client, "coffeetype", value)
def writePrinter(client, value: int):
    writeMod(client, "printer", value)
def writeDropoffpos(client, value: int):
    writeMod(client, "dropoff", value)
def writeCuppos(client, value: int):
    writeMod(client, "cafpos", value)

def run_test():
    output_text.delete(1.0, tk.END)
    command_output = (
    'Test Connection to Robot. Status:', testconnect()
    )
    output_text.insert(tk.END, command_output)
    output_text.insert(tk.END, "\n")

def start_action():
    output_text.delete("1.0", tk.END)
    command_output=[
        'input: ','coffeetype', getCoffeetype(),'dropoff', getDropoff(),'cuppos', getCafpos(), 'printer', getPrinter()
    ]
    output_text.insert(tk.END, command_output)
    output_text.insert(tk.END, "\n")

    command_output= ['connect to robot']
    output_text.insert(tk.END, command_output)
    output_text.insert(tk.END, "\n")
    # Robot IP address
    robot_ip="192.168.1.200"
    conSuc,sock=connectETController(robot_ip)
    if conSuc:
        writeCoffeetype(sock, getCoffeetype())
        writeDropoffpos(sock, getDropoff())
        writeCuppos(sock, getCafpos())
        writePrinter(sock, getPrinter())

        readModData(sock)
        command_output = (
            data
        )
        output_text.insert(tk.END, command_output)
        output_text.insert(tk.END, "\n")

        command_output = ['start production']
        output_text.insert(tk.END, command_output)
        output_text.insert(tk.END, "\n")
        writeStart(sock)
        
    else:
        command_output = (
            'no connection to robot'
        )
        output_text.insert(tk.END, command_output)
        output_text.insert(tk.END, "\n")

# Button Functions
def select_coffee(option, value):       
    setCoffeetype(value)
    update_button_colors(coffee_buttons, option)

def select_cup_position(option,value):
    setCafpos(value)
    update_button_colors(cup_position_buttons, option)

def select_drop_off(option,value):
    setPrinter(value)
    update_button_colors(drop_off_buttons, option)

def update_button_colors(buttons, selected):
    for button in buttons:
        if button['text'] == selected:
            button.config(bg="lightblue", relief=tk.SUNKEN)
        else:
            button.config(bg="lightgray", relief=tk.RAISED)

# Create the main window
root = tk.Tk()
root.title("Coffee Order App")

# Coffee Selection Frame
coffee_frame = tk.Frame(root)
coffee_frame.pack(side='top',  fill='both', padx=5, pady=5)

# Create Cup Position frame
cuppos_frame = tk.Frame(root)
cuppos_frame.pack(side='top',  fill='both', padx=5, pady=5)

# Create Drop Off Position frame
dropoff_frame = tk.Frame(root)
dropoff_frame.pack(side='top',  fill='both', padx=5, pady=5)

# Create Coffee selection buttons
# Header
coffee_label = tk.Label(coffee_frame, text="Select Coffee Type:", font=("Helvetica", 24), anchor='w')
coffee_label.pack(side='top', anchor = 'w')

#Button Frame
coffee_buttons_frame = tk.Frame(coffee_frame)
coffee_buttons_frame.pack(side='top', anchor = 'w')

coffee_buttons = [
    tk.Button(coffee_buttons_frame, text="Coffee", font=("Helvetica", 20), command=lambda: select_coffee("Coffee", 0), bg="lightblue", borderwidth=5, relief=tk.RAISED, width=15),
    tk.Button(coffee_buttons_frame, text="Cappuccino", font=("Helvetica", 20), command=lambda: select_coffee("Cappuccino", 1), bg="lightgray", borderwidth=5, relief=tk.RAISED, width=15),
]
for idx, button in enumerate(coffee_buttons):
    button.grid(row=0, column=idx, padx=5, pady=5, sticky='w')

# Create Cup selection buttons
# Load an image using PIL
# Determine if running as a bundled executable
if getattr(sys, 'frozen', False):
    # If frozen, use _MEIPASS to get the path of bundled files
    current_dir = sys._MEIPASS
else:
    # If not frozen, use the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "CupHolder.png")
image = Image.open(image_path)
desired_size = (300, 300)  # Set your desired size (width, height)
resized_image = image.resize(desired_size)
photo = ImageTk.PhotoImage(resized_image)

# Header
cuppos_label = tk.Label(cuppos_frame, text="Select Cup Position:", font=("Helvetica", 24), anchor='w')
cuppos_label.pack(side='top',  anchor = 'w')

# Add hint below the cup position label
cuppos_hint = tk.Label(cuppos_frame, text="Please check, that cup holders are stocked.", font=("Helvetica", 16), anchor='w')
cuppos_hint.pack(side='top',  anchor = 'w')

# Create a label to display the image next to the buttons
cuppos_image = tk.Label(cuppos_frame, image=photo)
cuppos_image.image = photo  # Keep a reference to avoid garbage collection
cuppos_image.pack(side='top', anchor = 'w')

# Buttons
cuppos_button_frame = tk.Frame(cuppos_frame)
cuppos_button_frame.pack(side='top', anchor = 'w')

cup_position_buttons = [
    tk.Button(cuppos_button_frame, text="Back Right", font=("Helvetica", 20), command=lambda: select_cup_position("Back Right",4), bg="lightgray", borderwidth=5, relief=tk.RAISED, width=15),
    tk.Button(cuppos_button_frame, text="Middle Left", font=("Helvetica", 20), command=lambda: select_cup_position("Middle Left",3), bg="lightgray", borderwidth=5, relief=tk.RAISED, width=15),
    tk.Button(cuppos_button_frame, text="Middle Right", font=("Helvetica", 20), command=lambda: select_cup_position("Middle Right",2), bg="lightgray", borderwidth=5, relief=tk.RAISED, width=15),
    tk.Button(cuppos_button_frame, text="Front Left", font=("Helvetica", 20), command=lambda: select_cup_position("Front Left",1), bg="lightblue", borderwidth=5, relief=tk.RAISED, width=15),
    tk.Button(cuppos_button_frame, text="Front Right", font=("Helvetica", 20), command=lambda: select_cup_position("Front Right",0), bg="lightgray", borderwidth=5, relief=tk.RAISED, width=15),
]

for idx, button in enumerate(cup_position_buttons):
    button.grid(row=((idx+1)  // 2) + 1, column=((idx +1)% 2), padx=5, pady=5) 

# Create Dorp Off selection buttons
# Header
dropoff_label = tk.Label(dropoff_frame, text="Print Logo:", font=("Helvetica", 24), anchor='w')  # Left align
dropoff_label.pack(side='top', anchor = 'w')

# Buttons
dropoff_button_frame = tk.Label(dropoff_frame)
dropoff_button_frame.pack(side='top', anchor = 'w')

name_dropoffbutton_up = "Yes"
name_dropoffbutton_down = "No"

drop_off_buttons = [
    tk.Button(dropoff_button_frame,text=name_dropoffbutton_down ,font=("Helvetica" ,20) ,command=lambda: select_drop_off(name_dropoffbutton_down ,0) ,bg="lightgray" ,borderwidth=5 ,relief=tk.RAISED ,width=15),
    tk.Button(dropoff_button_frame,text=name_dropoffbutton_up ,font=("Helvetica" ,20) ,command=lambda: select_drop_off(name_dropoffbutton_up ,1) ,bg="lightblue" ,borderwidth=5 ,relief=tk.RAISED ,width=15),
]
for idx ,button in enumerate(drop_off_buttons):
    button.grid(row=1,column=idx,padx=(5))

# Create Start and Test buttons
# Header
button_frame = tk.Frame(root)
button_frame.pack(pady=(20), padx=(5),anchor = 'w')
# Buttons
start_button = tk.Button(button_frame,width=(15) ,height=(2), text=("Start"), command=start_action, font=("Helvetica" ,20), bg=("lightgreen"), borderwidth=(5), relief=tk.RAISED)
start_button.grid(row=(0), column=(1), padx=(5), sticky = 'w')

test_button = tk.Button(button_frame, width=(15), height=(2), text=("Test Connection"), command=(run_test), font=("Helvetica" ,20), bg=("grey"), borderwidth=(5), relief=tk.RAISED)
test_button.grid(row=(0), column=(0), padx=(5), sticky= 'w')

# Create Text Box for output
output_text = tk.Text(root,height=(10) ,width=(70) ,font=("Helvetica" ,16))
output_text.pack(pady=20,padx=5,anchor = 'w')

# Initialize button colors
update_button_colors(coffee_buttons,"Coffee")
update_button_colors(cup_position_buttons,"Front Right")
update_button_colors(drop_off_buttons,name_dropoffbutton_down)

# Run the application
root.mainloop()