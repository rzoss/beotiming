from statemachine import StateMachine
import dogm, rfid, portexpander, summer
import time
import datetime
from urllib.request import urlopen

VERSION="01.00"

CFG_TAG_PRESENT_POLL_TIME = 0.25

old_timestring = ""

# create objects
disp = dogm.dogm()
exp = portexpander.PCF8574()
beeper = summer.summer()
tag_reader = rfid.SL030()

def internet_on():
    try:
        response=urlopen('http://www.google.ch',timeout=1)
        return True
    except URLError as err: pass
    return False

def init_transition(txt):
    # initialisation
    disp.display_backlight(True)
    disp.display_write(0,"Startup ...")
    disp.display_write(1,"Version " + VERSION)
    disp.display_write(2,"beo-timing.ch")
    time.sleep(3)
    # test internet connection
    disp.display_write(2,"check connection")
    time.sleep(1)
    i = 0 
    while not internet_on():
        # retry every second
        i += 1
        disp.display_write(1,"conn. failed")
        disp.display_write(2,"retry #" + i)
        time.sleep(1)
    disp.display_write(1,"conn. succesfull")
    disp.display_write(2,"startup finished")    
    time.sleep(1)
    disp.display_backlight(False)
    # next state idle
    newState = "idle"
    return (newState, txt)

def idle_transition(txt):
	global old_timestring
	time.sleep(CFG_TAG_PRESENT_POLL_TIME)
	disp.clear_display()
	t = datetime.datetime.now()
	timestring = t.strftime("%H:%M:%S")
	if not timestring == old_timestring:
		disp.display_write(1,"    " + t.strftime("%H:%M:%S") + "    ")
	old_timestring = timestring
	newState = "check_card"
	return (newState, txt)

def check_card_transition(txt):
	# check if a tag is present
	if tag_reader.selectMifareUL():
		newState = "read_card"
	else:
		newState = "idle"
	return (newState, txt)
	
def read_card_transition(txt):
	# check if there was already a race writen to the card
	tag_reader.getStateUL()
	if (tag_reader.getData() & TAG_STATUS_STRECKENVALID) and not(tag_reader.getData() & TAG_STATUS_STARTVALID) and not (tag_reader.getData() & TAG_STATUS_ENDVALID) and not (tag_reader.getData() & TAG_STATUS_MANUALCLEARED):
		newState = "write_start_time"
	else:
		newState = "choose_route"
	return (newState, txt)
		
def choose_route_transition(txt):
	# let the user select a route
	disp.clear_display()
	disp.display_write(0,"Kategorieauswahl")
	# TODO: get race name and route nr from somewhere
	disp.display_write(1,"Rennvelo")
	route_nr = 65
	while 1:
		# check for pressed button
		button = exp.readButton()
		if button & BUTTON_BACK:
			# TODO
			newState = "choose_route"
		elif button & BUTTON_NEXT:
			# TODO
			newState = "choose_route"
		elif button & BUTTON_OK:
			# set state on the card, but do not overwrite the registred flag
			if not tag_reader.setRaceKeyUL(route_nr):
				# cancel
				newState = "idle"
				break
			if not tag_reader.setStateUL(tag_reader.getData()&0xF0 | TAG_STATUS_STRECKENVALID):
				# cancel
				newState = "idle"
				break
			# wrote succesfully
			disp.display_write(0,"Gewaehlt:")
			newState = "wait_remove"
			break
		# check if the rfid tag is still available
		if not tag_reader.selectMifareUL():
			newState = "idle"
			break
		# wait some time before doing it again
		time.sleep(0.01)
	return (newState, txt)

def wait_remove_transition(txt):
	# wait for removing rfid tag
	tag_reader.waitNoTag()
	newState = "idle"
	return (newState, txt)
	
def write_start_time_transition(txt):
	# write start time to the rfid tag and update states
	if not tag_reader.setStartTimeUL(datetime.datetime.now()):
		newState = "idle"
		return (newState, txt)
	if not tag_reader.getStateUL():
		newState = "idle"
		return (newState, txt)
	if not tag_reader.setStateUL(tag_reader.getData()&0xF0 | TAG_STATUS_STRECKENVALID | TAG_STATUS_STARTVALID):
		newState = "idle"
		return (newState, txt)
	newState = "beep"
	return (newState, txt)
	
def beep_transition(txt):
	# beep 
	beeper.beep(0.5)
	newState = "idle"
	return(newState, txt)
		
def shutdown_transition(txt):
	return("shutdown", "")
		
if __name__== "__main__":
    m = StateMachine()
    m.add_state("init", init_transition)
    m.add_state("idle", idle_transition)
    m.add_state("check_card", check_card_transition)
    m.add_state("read_card", read_card_transition)
    m.add_state("choose_route", choose_route_transition)
    m.add_state("wait_remove", wait_remove_transition)
    m.add_state("write_start_time", write_start_time_transition)
    m.add_state("beep", beep_transition)
    m.add_state("shutdown", shutdown_transition, end_state=1)
    m.set_start("init")
    
    m.run("dummy")
