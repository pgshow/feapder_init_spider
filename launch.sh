#!/bin/sh
#ps -ef | grep python3 | cut -c 9-15| xargs kill -s 9

GetSpiders(){
  echo "\033[31m-Launch Spider: $1 \033[0m"

  # launch spider with tmux one by one
  tmux new-session -d -s "$1"
  tmux send-key -t "$1" "cd spiders" Enter
  tmux send-key -t "$1" "export PYTHONPATH=.." Enter
  tmux send-key -t "$1" "python3 $1.py" Enter
}

cmd=$(which tmux) # tmux path

# Check environment
if [ -z "$cmd" ]; then
      echo "You need to install tmux."
      exit 1
fi

# Find in spiders folder and launch
files=$(ls spiders)
for filename in $files
    do
        # Only py file
        if [ "${filename##*.}"x != "py"x ]; then
          continue
        fi

        # Drop __init__.py file
        if [ "$filename" = "__init__.py" ];then
          continue
        fi

        # Get only the name
        spider_name="${filename%.py*}"

        GetSpiders "$spider_name"
    done



# Launch Schedule controller
echo "\033[33m-Launch Schedule Controller \033[0m"
tmux new-session -d -s schedule
tmux send-key -t "$1" "python3 main_schedule.py" Enter

# Instructions
echo "\033[33m-Use 'tmux ls' to list sessions \033[0m"
echo "\033[33m-Use 'tmux a -t xxx' to join a session \033[0m"
echo "\033[33m-'<Ctrl-b> then <d>' to quit a session \033[0m"
echo "\033[33m-'Others Usage: https://tmuxcheatsheet.com/"