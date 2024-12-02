"""Robot Communication and Data Parsing for Robot App"""
import socket
import json

class rob:
    def __init__(self, ip="192.168.1.200", port=8055):
        self.ip = ip
        self.port = port
        self.sock = None
        self.data = [
            ['cafpos', 0, 0],
            ['coffeetype', 0, 1],
            ['printer', 0, 2],
            ['dropoff', 0, 3],
            ['startsignal', 0, 5],
        ]
        self.avData = {item[0]: idx for idx, item in enumerate(self.data)}

    def __str__(self):
        return '\n'.join(f'{item[0]} has value {item[1]}' for item in self.data)
        
    def set_value(self, key, value):
        if key in self.avData:
            self.data[self.avData[key]][1] = value
        else:
            print(f"Key {key} not found.")

    def get_value(self, key):
        return self.data[self.avData[key]][1] if key in self.avData else None
    
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.ip, self.port))
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            self.sock = None
            return False

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def send_cmd(self, cmd, params=None, id=1):
        if not self.sock:
            print("Not connected to the robot.")
            return False, None, None
        #params = json.dumps(params or [])
        if(not params):
            params=[]
        else:
            params=json.dumps(params)
        #print(params)
        send_str = '{"method":"' + cmd + '","params":' + str(params) + ',"jsonrpc":"2.0","id":' + str(id) + '}\n'
        #print("Feedback send_cmd: ", send_str)
        try:
            self.sock.sendall(bytes(send_str, "utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            if("result" in jdata.keys()):
                return (True,json.loads(jdata["result"]),jdata["id"])
            elif("error" in jdata.keys()):
                return (False,jdata["error"],jdata["id"])
            else:
                return (False,None,None)
        except Exception as e:
            print(f"Command failed: {e}")
            return False, None, None
    
    def write_start(self):
        jbi_filename="main"
        success, result, _ = self.send_cmd("checkJbiExist",{"filename":jbi_filename})
        print("write start feedback: ", success, result)
        if success and result:
            self.send_cmd("runJbi", {"filename":jbi_filename})
        return success

    def read_mod_data(self):
        if not self.sock:
            print("Not connected to the robot.")
            return
        for item in self.data:
            success, result, _ = self.send_cmd("getSysVarB", {"addr": item[2]})
            if success and isinstance(result, int):
                item[1] = result
                print(f"{item[0]}: {item[1]}")
            elif result.get('code') == -32601:
                print("Error: Method in readModData not found")
            else:
                print(f"Failed to read {item[0]}: {result}")
           # print("read_mod_data feedback for item: ", item ,success, result)

    def write_mod(self, key, value):
        if key in self.avData:
            success, result, _ = self.send_cmd("setSysVarB", {"addr": self.data[self.avData[key]][2], "value": value})
            if success:
                print(f"{key} updated to {value}")
            else:
                print(f"Failed to update {key}: {result}")
        else:
            print(f"Key {key} not found.")

    def test_connection(self):
        print("run test_connection")
        conSuc = self.connect()
        if conSuc:
            print("test_connection to Robot successfull at: ", format(self.sock))
            success, state, _ = self.send_cmd("getRobotState")
            print("test_connection Robot State: ", state)
            success, state, _ = self.send_cmd("getRobotMode")
            if success:
                print(f"Robot Mode: {state}")
            if state != 2:
                print("Attention Robot is not in Remote Mode! Can not recive data or get started remotly! Switch to Remot Mode first!")
            return True, state
        else:
            print("Failed to connect to robot.")
            return False, False
    
    def emergencystop(self):
        print("emergency stop")
        if self.connect():
            self.send_cmd("stop")
        self.disconnect()
    
    def gobacktoStart(self):
        print("goback to start")
        gotostartfile = "p_startpos"
        if self.connect():
            self.send_cmd("runJbi", {"filename":gotostartfile})
        self.disconnect()
        