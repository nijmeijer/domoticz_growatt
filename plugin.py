# Growatt Python Plugin for Domoticz
#
# Author: Alex Nijmeijer
#
# Required Python Packages
#    pip install modbus pymod pymodbus
#
"""
<plugin key="Growatt" name="Growatt Solar Inverter" author="Alex Nijmeijer" version="1.0.0">
    <params>
        <param field="SerialPort" label="Serial Port" width="150px" required="true"/>
    </params>
</plugin>
"""

import subprocess
from time import strftime
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


#import logging
#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.ERROR)


try:
    import Domoticz
except ImportError:
    import fakeDomoticz as Domoticz


class BasePlugin:
    enabled = False
    def __init__(self):
        return

    def onStart(self):
       Domoticz.Log("onStart called")
       if (len(Devices) == 0 ):
         Domoticz.Log("Adding devices.")
         Domoticz.Device("Test", Unit=1, Type=243, Subtype=29).Create()
       DumpConfigToLog()
       Domoticz.Log("Plugin is started @ Serial " + Parameters["SerialPort"])
       Domoticz.Heartbeat(20) #20

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")

        ## Read Growatt Inverter ##
        try:
          # myport = Parameters["SerialPort"]
          # Domoticz.Log(myport)
          client = ModbusClient(method='rtu', port=Parameters["SerialPort"], baudrate=9600, stopbits=1, parity='N', bytesize=8, timeout=1)
        except:
          Domoticz.Log("Error opening USB Modbus connection to Growatt inverter on "+Parameters["SerialPort"])
        else:
          try:
            client.connect()
            growatt_pv_watt   = int(client.read_input_registers(2,1).registers[0]/10)
            growatt_wh_total  = int(client.read_input_registers(29,1).registers[0]*100)
            Domoticz.Log("Growatt New:" + str(growatt_wh_total) + "; " + str(growatt_pv_watt) )
            Devices[1].Update(nValue=growatt_pv_watt, sValue=(str(growatt_pv_watt) + "; " +str(growatt_wh_total)) )
            client.close()
            Domoticz.Log("Updated")
          except:
            Domoticz.Log("Error")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data, Status, Extra):
    global _plugin
    _plugin.onMessage(Connection, Data, Status, Extra)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

