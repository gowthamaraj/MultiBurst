#!/bin/bash

# This script splits a file into equal parts based on the number of servers

# Input arguments
file_location=$1  # The location of the file to be split
server_number=$2  # The number of the server
server_count=$3   # The total number of servers

# Calculate total number of lines in the file
total_lines=$(wc -l < "$file_location")  # Count the total number of lines in the file

# Calculate lines per server
lines_per_server=$((total_lines / server_count))  # Divide the total number of lines by the number of servers

# Calculate start and end lines for the portion of the file
start_line=$(((server_number - 1) * lines_per_server + 1))  # Calculate the starting line for the portion of the file
end_line=$((server_number * lines_per_server))  # Calculate the ending line for the portion of the file

# Extract the portion of the file
awk -v start="$start_line" -v end="$end_line" 'NR>=start && NR<=end' "$file_location"  # Extract the portion of the file based on the start and end lines
