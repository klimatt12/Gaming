# Gaming
Utility to display stats from a gaming session


# Datadog
In the inital state, contains agent configuration files with the assumption the agent is already installed and running on a windows machine  
A docker image with config already completed will be added at a later date

# Terraform 
Contains terraform templates to create datadog monitors and dashboards that will be used to display the session stats

# Known Issues
Currently only works with games running through steam, and sometimes inconsistently (ie, bladur's gate runs using ../bin/bg3.exe and thus is not cautght by steamapps)  
Dashboard needs to be referenced in a more robust way  
Getting stats from Nvidia GPUs is surprisingly unintuitive. May need to do something custom
Need to determine how to set the timespan of the monitor to start when the alert fliped from "alert" to "ok", signifying the start of a gaming session.  