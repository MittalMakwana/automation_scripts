'Email id 
grep -Eo '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b' <filename>

'IPv4
grep -Eo "((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" <file name>

'Date stamp: Jan  1 12:51:59 Usefull for log parsing
grep -Eo "\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}" log

'Date YYYY-MM-DD
grep -Eo "\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])" log
