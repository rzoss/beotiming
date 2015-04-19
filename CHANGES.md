# Change Log #
All notable changes to this project will be documented in this file.
This project adheres to [BEO-Timing](http://www.beo-timing.ch/).

## [Unreleased] ##

## [1.1.0] - 2015-04-19 ##
### Changed ###
- changed version numbering format

### Fixed ###
- added a timeout in the check_card transition to avoid a error behaviour in the field. 
- changed the connection_check function to work on python3 and fixed some errors in error case.

## [01.00] - 2015-04-04 33 ##
First operational release

### Added ###
- config.ini for start station
- add error handling for getState()

## [00.99] - 2015-04-03 ##

### Added ###
- changelog
- add log entry to the launcher script
- getRouteType to show on display
- add support for left and centered alignment on the display

### Changed ###
- changed logging format
- use smaller polling time for the buttons
- regrouped py-modules 

### Fixed ###
- fill every line up to 16 char to remove the last text

## [00.90] - 2015-03-29 ##
first working version

### Missing functions ###
- configuration
- choose race
- logging
- end station functions

