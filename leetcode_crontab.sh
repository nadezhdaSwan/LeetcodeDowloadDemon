#!/bin/bash
cd ~/code/LeetcodeDowloadDemon
export PATH=$PATH:$HOME/.python3.12/bin
export PATH=$PATH:$HOME/.local/bin
export PATH=$PATH:$HOME/bin
echo $(date) --- launched LeetcodeDowloadDemon >> /home/nadezhda/crontab.log
poetry run python -m main

# crontab
# 0 9-18 * * * /home/nadezhda/code/LeetcodeDowloadDemon/leetcode_crontab.sh