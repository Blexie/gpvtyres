import xml.etree.ElementTree as ET
import ctypes
import tkinter
import sys
from tkinter import filedialog

tkroot = tkinter.Tk()
tkroot.overrideredirect(True)
tkroot.attributes("-alpha", 0)

def getqualifile():
    qualifile = filedialog.askopenfilename(filetypes=[("XML File", ".xml")], title="Select a QUALIFYING file")
    if not qualifile:
        sys.exit(2)
    else:
        qualitree = ET.parse(qualifile)
        qualiroot = qualitree.getroot()
        return qualiroot

def getracefile():
    racefile = filedialog.askopenfilename(filetypes=[("XML File", ".xml")], title="Select a RACE file")
    if not racefile:
        sys.exit(2)
    else:
        racetree = ET.parse(racefile)
        raceroot = racetree.getroot()
        return raceroot
top10 = {}

qualiroot = getqualifile()
raceroot = getracefile()

for driver in qualiroot.iter('Driver'):
    name = driver.find('Name')
    bestlap = driver.find('BestLapTime')
    qualiposition = int(driver.find('Position').text)
    if qualiposition <= 10:
        for lap in driver.findall('Lap'):
            if lap.text == bestlap.text:
                qualicompound = lap.get('fcompound')
                top10[name.text] = qualicompound
            else:
                continue

for driver in raceroot.iter('Driver'):
    name = driver.find('Name')
    if name.text in top10:
        for lap in driver.findall('Lap'):
            if lap.get('num') != "1":
                continue
            else:
                racecompound = lap.get('fcompound')
                if racecompound == top10[name.text]:
                    #print(name.text, "okay")
                    continue

                else:
                    ctypes.windll.user32.MessageBoxW(0, name.text + " NOT okay. Quali tyre: " + top10[name.text] +
                                                     " Race tyre: " + racecompound, "Tyre Violation")
                    #print(name.text, "NOT OKAY")
ctypes.windll.user32.MessageBoxW(0, "Check complete!", "GPV Tyre check")
