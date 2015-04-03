from helper import statemachine, beoconfig
from hardware import display, rfid, portexpander, summer
import time
import datetime
from urllib.request import urlopen
import logging


# VERSION="01.00"
VERSION = "00.99"

CFG_TAG_PRESENT_POLL_TIME = 0.10
CFG_BUTTON_POLL_TIME = 0.01

old_timestring = ""

# create objects
disp = display.dogm()
exp = portexpander.PCF8574()
beeper = summer.summer()
tag_reader = rfid.SL030()
cfg = beoconfig.BeoConfig()
logging.basicConfig(filename='/var/log/beotiming.log', level=logging.INFO, format='%(asctime)s | %(levelname)s: %(message)s')


def internet_on():
    try:
        response = urlopen('http://www.google.ch', timeout=1)
        return True
    except URLError as err:
        pass
    return False


def init_transition(txt):
    # initialisation

    disp.display_backlight(True)
    logging.info('Startup | Version ' + VERSION)
    disp.display_write(0, "Startup ...")
    disp.display_write(1, "Version " + VERSION)
    disp.display_write(2, "beo-timing.ch")
    time.sleep(3)
    # test internet connection
    disp.display_write(2, "check connection")
    time.sleep(1)
    i = 0
    while not internet_on():
        # retry every second
        disp.display_write(1, "conn. failed")
        i += 1
        disp.display_write(2, "retry #" + i)
        logging.info('Connection failed. Retry #' + i)
        time.sleep(1)
    disp.display_write(1, "successfull")
    logging.info('Connection test successfull. Startup finished.')
    time.sleep(1)
    disp.display_write(0, "Startup finished")
    disp.display_write(1, "The type is")
    if cfg.isStart():
        logging.info('This is a Start-Station.')
        disp.display_write(2, "Start-Station")
    else:
        logging.info('This is a Finish-Station.')
        disp.display_write(2, "Finish-Station")
    time.sleep(2)
    logging.info('The route is: ' + cfg.getRouteName())
    disp.display_write(1, "The route is")
    disp.display_write(2, cfg.getRouteName())
    time.sleep(2)
    disp.display_backlight(False)
    # next state idle
    newState = "idle"
    return (newState, txt)


def idle_transition(txt):
    global old_timestring
    time.sleep(CFG_TAG_PRESENT_POLL_TIME)
    disp.display_backlight(False)
    exp.setBothLED(False, False)
    t = datetime.datetime.now()
    timestring = t.strftime("%H:%M:%S")
    if not timestring == old_timestring:
        disp.display_write(0, t.strftime("%d.%m.%Y"), True)
        disp.display_write(1, t.strftime("%H:%M:%S"), True)
        disp.display_write(2, "beo-timing.ch", True)
    old_timestring = timestring
    newState = "check_card"
    return (newState, txt)


def check_card_transition(txt):
    # check if a tag is present
    if tag_reader.selectMifareUL():
        disp.display_backlight(True)
        exp.setRedLED(True)
        logging.debug('newState: check_card')
        newState = "read_card"
    else:
        newState = "idle"
    return (newState, txt)


def read_card_transition(txt):
    # check if there was already a race writen to the card
    tag_reader.getStateUL()
    if (tag_reader.getData(0) & rfid.TAG_STATUS_STRECKENVALID) and not (
                tag_reader.getData(0) & rfid.TAG_STATUS_STARTVALID) and not (
                tag_reader.getData(0) & rfid.TAG_STATUS_ENDVALID) and not (
                tag_reader.getData(0) & rfid.TAG_STATUS_MANUALCLEARED):
        exp.setRedLED(True)
        disp.display_write(1, "Karte nicht")
        disp.display_write(2, "entfernen")
        logging.debug('newState: write_start_time')
        newState = "write_start_time"
    else:
        exp.setRedLED(True)
        logging.debug('newState: choose_route')
        newState = "choose_route"
    return (newState, txt)


def choose_route_transition(txt):
    # let the user select a route
    disp.clear_display()
    disp.display_write(0, "Kategorieauswahl")
    # TODO: get race name and route nr from somewhere
    route, routecount = cfg.getRoute()
    logging.debug('Nr: ' + route[0][0] + ' / Typ: ' + route[0][1])
    index = 0
    disp.display_write(1, route[index][1])
    disp.display_write(2, cfg.getRouteName())
    route_nr = int(route[index][0])
    while 1:
        # check for pressed button
        button = exp.readButton()
        if button & portexpander.BUTTON_BACK:
            index = (index - 1)%routecount
            logging.debug("BACK pressed | index: " + str(index) + ' | Nr: ' + route[0][0] + ' | Typ: ' + route[0][1])
            disp.display_write(1, route[index][1])
            route_nr = int(route[index][0])
            newState = "choose_route"
        elif button & portexpander.BUTTON_NEXT:
            index = (index + 1)%routecount
            logging.debug("NEXT pressed | index: " + str(index) + ' | Nr: ' + route[0][0] + ' | Typ: ' + route[0][1])
            disp.display_write(1, route[index][1])
            route_nr = int(route[index][0])
            newState = "choose_route"
        elif button & portexpander.BUTTON_OK:
            # set state on the card, but do not overwrite the registred flag
            logging.debug("OK pressed")
            if not tag_reader.setRaceKeyUL(route_nr):
                # cancel
                logging.warning('error in setRaceKeyUL -> newState: idle')
                newState = "idle"
                break
            if not tag_reader.setStateUL(tag_reader.getData(0) & 0xF0 | rfid.TAG_STATUS_STRECKENVALID):
                # cancel
                logging.warning('error in setStateUL -> newState: idle')
                newState = "idle"
                break
            # wrote succesfully
            logging.info("wrote route successfull: " + tag_reader.getUniqueId() + " | route nr: " + str(route_nr) + " | route type: " + cfg.getRouteType(route_nr))
            disp.display_write(0, "Gewaehlt:")
            disp.display_write(1, route[index][1])
            disp.display_write(2, "Karte entfernen")
            exp.setGreenLED(True)
            exp.setRedLED(False)
            logging.debug('newState: wait_remove')
            newState = "wait_remove"
            break
        # check if the rfid tag is still available
        if not tag_reader.selectMifareUL():
            logging.debug('newState: idle')
            newState = "idle"
            break
        # wait some time before doing it again
        time.sleep(CFG_BUTTON_POLL_TIME)
    return (newState, txt)


def wait_remove_transition(txt):
    # wait for removing rfid tag
    logging.debug('wait for tag remove -> newState: idle')
    tag_reader.waitNoTag()
    exp.setGreenLED(False)
    newState = "idle"
    return (newState, txt)


def write_start_time_transition(txt):
    # write start time to the rfid tag and update states
    if not tag_reader.setStartTimeUL(datetime.datetime.now()):
        logging.warning('error in setStartTimeUL -> newState: idle')
        newState = "idle"
        return (newState, txt)
    if not tag_reader.getStateUL():
        logging.warning('error in getStateUL -> newState: idle')
        newState = "idle"
        return (newState, txt)
    if not tag_reader.setStateUL(tag_reader.getData(0) & 0xF0 | rfid.TAG_STATUS_STRECKENVALID | rfid.TAG_STATUS_STARTVALID):
        logging.warning('error in setStateUL -> newState: idle')
        newState = "idle"
        return (newState, txt)
    if not tag_reader.getRaceKeyUL():
        logging.warning('error in getRaceKeyUL -> newState: idle')
        newState = "idle"
        return (newState, txt)
    route_nr = tag_reader.getData(0)
    logging.info("wrote start time successfull: " + tag_reader.getUniqueId() + " | route nr: " + str(route_nr) + " | route type: " + cfg.getRouteType(route_nr) + " | start time: " + datetime.datetime.now().isoformat())
    # inform user
    disp.display_write(0, "Zeit gespeichert")
    disp.display_write(1, "STARTEN", True)
    disp.display_write(2, cfg.getRouteType(route_nr), True)
    exp.setGreenLED(True)
    exp.setRedLED(False)
    logging.debug('newState: beep')
    newState = "beep"
    return (newState, txt)


def beep_transition(txt):
    # beep
    beeper.beep(0.5)
    logging.debug('newState: wait_remove')
    newState = "wait_remove"
    return (newState, txt)


def shutdown_transition(txt):
    return ("shutdown", "")


if __name__ == "__main__":
    m = statemachine.StateMachine()
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
