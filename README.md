## General
____________

### Author
* Josh McIntyre

### Website
* jmcintyre.net

### Overview
* HobbyStats processes generic hobby log formats and computes interesting statistics

## Development
________________

### Git Workflow
* master for releases (merge development)
* development for bugfixes and new features

### Building
* make build
Build the application
* make clean
Clean the build directory

### Features
* Trip-level stats like totals, per hobby, per year counts
* Mileage stats like sum, avg, min, max per hobby

### Requirements
* Requires Python 3

### Platforms
* Windows
* Linux
* MacOSX

## Usage
____________

### Log formatting
* Logs can have the following formats:
* Trip Count - A column for "Years" and a column for "Trips". All other data is ignored
* Date and Data - A column for "Date" at least, and other data you log. All other data is ignored.
* Date and Mileage - A column for "Date" and "Distance (mi)" at least. All other data is ignored.

### General usage
* Put CSV format logs in the log directory and run make
* Run `python hobbystats.py` from the build dir
* Formatted data will be printed to the console

### Unit tests
* Run `python -m pytest <test files>`

