# Gaming
Utility to display stats from a gaming session.

# Prereqs
A user needs to have a gaming client (steam, epic, etc) set up on their computer, and games available on those platforms.
A user needs to have an email address they can use for setting up free accounts for any tools that may require it (grafana, datadog)


# Architecture

The user needs to clone this repo to their gaming rig.
Run the configurator and select: 

    - monitoring solutions you want to use.

provide any necessary info and wait for monitoring solutions to be provisioned.  This should provide links when complete.

wait for monitoring clients to install on your computer.  
start gaming and view results!


# Datadog
In the initial state, contains agent configuration files with the assumption the agent is running on a windows machine  
A docker image option is coming at a later date

# Grafana
Contains setup for creating all the dashboards in datadog in grafana.

# Terraform 
Contains terraform templates to create datadog/grafana monitors and dashboards that will be used to display the session stats

# Known Issues
Currently only works with games running through steam, and sometimes inconsistently (ie, bladur's gate runs using ../bin/bg3.exe and thus is not cautght by steamapps)  
Some games don't really have any indication what they are (ie, slay the spire shows as javaw)  
Dashboard needs to be referenced in a more robust way  
Getting stats from Nvidia GPUs is surprisingly unintuitive. May need to do something custom
Need to determine how to set the timespan of the monitor to start when the alert fliped from "alert" to "ok", signifying the start of a gaming session.  
