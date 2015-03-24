from statemachine import StateMachine
import dogm
import time
import urllib2

VERSION="01.00"

def internet_on():
    try:
        response=urllib2.urlopen('http://www.google.ch',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def start_transitions(txt):
    # initialisation
    Dogm.display_init()
    Dogm.display_backlight(True)
    Dogm.display_write(0,"Startup ...")
    Dogm.display_write(1,"Version " + VERSION)
    Dogm.display_write(2,"www.beo-Timing.ch")
    time.sleep(3)
    # test internet connection
    Dogm.display_write(2,"check connection")
    time.sleep(1)
    i = 0 
    while ! internet_on():
	  # retry every second
	  i++
      Dogm.display_write(1,"conn. failed")
      Dogm.display_write(2,"retry #" + i)
      time.sleep(1)
    Dogm.display_write(1,"conn. succesfull")
    Dogm.display_write(2,"startup finished")    
    time.sleep(1)
    # next state idle
    newState = "idle"
    return (newState, txt)

def python_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "is":
        newState = "is_state"
    else:
        newState = "error_state"
    return (newState, txt)

def is_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "not":
        newState = "not_state"
    elif word in positive_adjectives:
        newState = "pos_state"
    elif word in negative_adjectives:
        newState = "neg_state"
    else:
        newState = "error_state"
    return (newState, txt)

def not_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word in positive_adjectives:
        newState = "neg_state"
    elif word in negative_adjectives:
        newState = "pos_state"
    else:
        newState = "error_state"
    return (newState, txt)

def neg_state(txt):
    print("Hallo")
    return ("neg_state", "")

if __name__== "__main__":
    m = StateMachine()
    m.add_state("init", init_transition)
    m.add_state("idle", idle_transition)
    m.add_state("check_card", check_card_transition)
    m.add_state("read_card", read_card_transition)
    m.add_state("choose_route", choose_route_transition)
    m.add_state("write_route", write_route_transition)
    m.add_state("wait_remove", wait_remove_transition)
    m.add_state("write_start_time", write_start_time_transition)
    m.add_state("beep", beep_transition)
    m.add_state("shutdown", shutdown_transition, end_state=1)
    m.set_start("init")
    
    m.run("dummy")
