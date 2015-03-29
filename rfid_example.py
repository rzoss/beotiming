# SL030 RFID tag reader example  18/08/2014  D.J.Whale
# http://blog.whaleygeek.co.uk/raspberry-pi-rfid-tag-reader
#
# For use with SKPang Electronics SL030 RFID module,
# with a SL030 Raspberry Pi cable, and a Raspberry Pi
# running Raspbian Wheezy.
# product numbers: RFID-SL030, RSP-SL030-CAB
# http://skpang.co.uk/blog/archives/946
#
# Run this program as follows:
#   sudo python rfid_example.py
# or
#   sudo python3 rfid_example.py


# Import this module to gain access to the RFID driver
import rfid
from rfid import TAG_STATUS_STRECKENVALID, TAG_STATUS_STARTVALID
import datetime

# fill in this map with the names of your card ID's
cards = {
  "2B53B49B"       : "whaleygeek", 
  "04982B29EE0280" : "elektor RFID card", 
  "EAC85517"       : "white card 1",
  "24B1E145"       : "white card 2",
  "C2091F58"       : "label 1",
  "22F51E58"       : "label 2"
}


# MAIN PROGRAM

tag_reader = rfid.SL030()

while True:

  # wait for a card to be detected as present
  print("Waiting for a card...")
  tag_reader.waitTag()
  print("Card present")

  # This demo only uses Mifare cards
  if not tag_reader.selectMifareUL():
    print("This is not a mifare card")
  else:
    # What type of Mifare card is it? (there are different types)
    print("Card type:" + tag_reader.getTypeName())

    # look up the unique ID to see if we recognise the user
    uid = tag_reader.getUniqueId()
    if not tag_reader.readDataPageUL(4):
      print("Can't read page")
    else:
      print("Page 4: %02X" %tag_reader.getData(0))

    if not tag_reader.readDataPageUL(5):
      print("Can't read page")
    else:
      print("Page 5:" + tag_reader.getDataString())
      
    if not tag_reader.readDataPageUL(6):
      print("Can't read page")
    else:
      print("Page 6:" + tag_reader.getDataString())
    
    if not tag_reader.readDataPageUL(7):
      print("Can't read page")
    else:
      print("Page 7:" + tag_reader.getDataString())  # wait for the card to be removed
  
    if not tag_reader.readDataPageUL(8):
      print("Can't read page")
    else:
      print("Page 8:" + tag_reader.getDataString())  # wait for the card to be removed
    
    if not tag_reader.readDataPageUL(9):
      print("Can't read page")
    else:
      print("Page 9:" + tag_reader.getDataString())  # wait for the card to be removed
     
    if not tag_reader.readDataPageUL(10):
      print("Can't read page")
    else:
      print("Page 10:" + tag_reader.getDataString())  # wait for the card to be removed
           
    if not tag_reader.getStateUL():
      print("Can't read state")
    else:
      print("State %02X:" %tag_reader.getData(0))  # wait for the card to be removed
      
    if not tag_reader.setStateUL(TAG_STATUS_STRECKENVALID | TAG_STATUS_STARTVALID):
      print("Can't write state")
    else:
      print("Wrote state successfully")  # wait for the card to be removed     
      
    if not tag_reader.setRaceKeyUL(65):
      print("Can't write race key")
    else:
      print("Wrote race key successfully")  # wait for the card to be removed 
   
    if not tag_reader.setStartTimeUL(datetime.datetime.now()):
      print("Can't write start time")
    else:
      print("Wrote start time successfully")  # wait for the card to be removed    
   
    if not tag_reader.setEndTimeUL(datetime.datetime.now()):
      print("Can't write end time")
    else:
      print("Wrote end time successfully")  # wait for the card to be removed       
   
    if not tag_reader.setRaceTimeUL(1,23,43):
      print("Can't write race time")
    else:
      print("Wrote race time successfully")  # wait for the card to be removed 
         
  print("Waiting for card to be removed...")
  tag_reader.waitNoTag()
  print("Card removed")

# END
