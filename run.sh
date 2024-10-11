#!/bin/bash

echo "Will execute commands in pop up terminals with a delay of 10 sec."
# Function to execute a command in a new terminal with a delay
run_in_terminal() {
  command=$1
  sleep 10  # Wait for 10 seconds
  gnome-terminal -- bash -c "$command; read -n 1 -s -r -p 'Press any key to exit...'" &
}

# Execute the commands in separate terminals
run_in_terminal "source ./commands/run_webservice.sh"
run_in_terminal "source ./commands/run_index.sh"
run_in_terminal "source ./commands/upload.sh"

echo "Commands launched in separate terminals."
