from statemachine import StateMachine
import dogm, portexpander, summer
import time
import urllib2

VERSION="01.00"

CFG_TAG_PRESENT_POLL_TIME = 0.25

def internet_on():
    try:
        response=urllib2.urlopen('http://www.google.ch',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def init_transitions(txt):
    # initialisation
    Dogm.display_init()
    portexpander.PCF8574_init()
    summer.init()
    Dogm.display_backlight(True)
    Dogm.display_write(0,"Startup ...")
    Dogm.display_write(1,"Version " + VERSION)
    Dogm.display_write(2,"www.beo-Timing.ch")
    time.sleep(3)
    # test internet connection
    Dogm.display_write(2,"check connection")
    time.sleep(1)
    i = 0 
    while not internet_on():
        # retry every second
        i += 1
        Dogm.display_write(1,"conn. failed")
        Dogm.display_write(2,"retry #" + i)
        time.sleep(1)
    Dogm.display_write(1,"conn. succesfull")
    Dogm.display_write(2,"startup finished")    
    time.sleep(1)
    # next state idle
    newState = "idle"
    return (newState, txt)

def idle_transitions(txt):
    time.sleep(CFG_TAG_PRESENT_POLL_TIME)
    Dogm.clear_display()
    t = datetime.datetime.now()
    Dogm.display_write(2,"    " + i.strftime("%H:%M:%S") + "    ")
    newState = "check_card"
    return (newState, txt)

def check_card_transition(txt):
	# check if a tag is present
	if rfid.selectMifareUL():
		newState = "read_card"
	else:
		newState = "idle"
	return (newState, txt)
	
def read_card_transition(txt):
	# check if there was already a race writen to the card
	rfid.getStateUL()
	if (rdif.getData() & TAG_STATUS_STRECKENVALID) and not(rdif.getData() & TAG_STATUS_STARTVALID) and not (rdif.getData() & TAG_STATUS_ENDVALID) and not (rdif.getData() & TAG_STATUS_MANUALCLEARED):
		newState = "write_start_time"
	else:
		newState = "choose_route"
	return (newState, txt)
		
def choose_route_transition(txt):
	# let the user select a route
	dogm.clear_display()
	dogm.display_write(0,"Kategorieauswahl")
	# TODO: get race name and route nr from somewhere
	dogm.display_write(1,"Rennvelo")
	route_nr = 65
	while 1:
		# check for pressed button
		button = portexpander.readButton()
		if button & BUTTON_BACK:
			# TODO
			newState = "choose_route"
		elif button & BUTTON_NEXT:
			# TODO
			newState = "choose_route"
		elif button & BUTTON_OK:
			# set state on the card, but do not overwrite the registred flag
			if not rfid.setRaceKeyUL(route_nr):
				# cancel
				newState = "idle"
				break
			if not rfid.setStateUL(rfid.getData()&0xF0 | TAG_STATUS_STRECKENVALID):
				# cancel
				newState = "idle"
				break
			# wrote succesfully
			dogm.display_write(0,"Gewaehlt:")
			newState = "wait_remove"
			break
		# check if the rfid tag is still available
		if not rfid.selectMifareUL():
			newState = "idle"
			break
		# wait some time before doing it again
		time.sleep(0.01)
	return (newState, txt)

def wait_remove_transition(txt):
	# wait for removing rfid tag
	rfid.waitNoTag()
	newState = "idle"
	return (newState, txt)
	
def write_start_time_transition(txt):
	# write start time to the rfid tag and update states
	if not rfid.setStartTimeUL(datetime.datetime.now()):
		newState = "idle"
		return (newState, txt)
	if not rfid.getStateUL():
		newState = "idle"
		return (newState, txt)
	if not rfid.setStateUL(rfid.getData()&0xF0 | TAG_STATUS_STRECKENVALID | TAG_STATUS_STARTVALID):
		newState = "idle"
		return (newState, txt)
	newState = "beep"
	return (newState, txt)
	
def beep_transition(txt):
	# beep 
	summer.beep(0.5)
	newState = "idle"
	return(newState, txt)
		
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
