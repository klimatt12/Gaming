# Gaming
Utility to display stats from a gaming session.

# Prereqs
- A user needs to have a gaming client (steam, epic, etc) set up on their computer, and games available on those platforms.  
- A user needs to have an email address they can use for setting up free accounts for any tools that may require it (grafana, datadog)

# Overview
- Code Tab: contains all the code for all the utilities available.
- Wiki Tab: contains various how-tos and overviews.
- Projects: A simple work tracking board, used for the author to keep track of WIP and completed items.
- Issues: create work items here  
  **do not use apostrophes, they are interpretted as single quotes and will cause failures! as of 9/13**
- Actions: view details about github actions executions.  Code for these can be found in the .guthub folder


# Architecture

The user needs to clone this repo to their gaming rig.
Run the configurator and select: 

    - monitoring solutions you want to use.

provide any necessary info and wait for monitoring solutions to be provisioned.  This should provide links when complete.

wait for monitoring clients to install on your computer.  
start gaming and view results!


# Datadog
In the initial state, contains agent configuration files with the assumption the agent is running on a windows machine.   
A docker image option is coming at a later date  
Instructions for creating a free trial can be found in the [wiki](https://github.com/klimatt12/Gaming/wiki/Create-Free-Trial-of-Datadog) section of this repo

# Grafana
Contains setup for creating all the dashboards in datadog in grafana.

# Terraform 
Contains terraform templates to create datadog/grafana monitors and dashboards that will be used to display the session stats

# Known Issues
Steam games are mostly reliable, but if it runs without referencing steamapps it won't be caught (ie, bladur's gate runs using ../bin/bg3.exe)  
I only currently have 2 games installed on epic - both are caught by -epicapp=, but this may not always be the case  
Some games don't really have any indication what they are (ie, slay the spire shows as javaw)   
Dashboard needs to be referenced in a more robust way  
Getting stats from Nvidia GPUs is surprisingly unintuitive. May need to do something custom
Need to determine how to set the timespan of the monitor to start when the alert fliped from "alert" to "ok", signifying the start of a gaming session.  
