# Padel-Wizard
Discover you Padel level and what to improve via simple Telegram Bot (RU)

Level calculated mostly based on this system https://docs.google.com/spreadsheets/d/1jdE1Vapsp82gfPGZ1dLT-uWM2JZJzav4J5mrZjnMBRw/edit?gid=989509914#gid=989509914

About author/feedback:
telegram: t.me/dikarevp
linkdin: linkedin.com/in/pavel-dikarev/

Stack:
Telegram bot API, Alogram 3.13.1, Phyton 3.8+, SQLite, bash, timeweb server 
~95% of code written by Codex+ChatGPT


Comands that are useful on the server:

supervisorctl start padel = starts the bot
supervisorctl stop padel = stops the bot
supervisorctl restart padel = restarts the bot
supervisorctl status padel = shows whether the bot is running
cd ~/stuff/padel_wizard && git pull && supervisorctl restart padel = updates code and restarts the bot
cd ~/stuff/padel_wizard && ./deploy.sh = runs the deploy script
tail -n 100 /var/log/padel_out.log = shows recent bot logs
tail -n 100 /var/log/padel_err.log = shows recent error logs
tail -f /var/log/padel_out.log = streams logs live
sqlite3 ~/stuff/padel_wizard/storage/padel_wizard.sqlite3 = opens the SQLite database
.tables = lists database tables
.schema users = shows the schema of the users table
