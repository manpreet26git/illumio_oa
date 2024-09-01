**Given**:
1) The file containing logs and tags are both plain text files. The tag file is a csv file.
2) The matches should be case insensitive 

**Assumptions**:
1) The program only supports default log format, not custom and the only version that is supported is 2. 
2) According to the details mentioned here https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
   2.1) Each log record is a string with fields separated by spaces
   2.2) Destination port is the sixth entry and protocol number is seventh entry in the record when zero indexed
3) A destination port and protocol combination given in the logs may not be present in the tags file. 
   For this case the untagged count goes up by one.

**Note**:
Tags are converted to lower case since it is given that matchings are case insensitive 
and the file containing tags may have "sv_P1" corresponding to 23, "tcp" and "sv_p1" to 31, "udp"

**How to run the program**:
1) Clone the repo
2) From a shell run: pip install -r requirements.txt
3) From a shell run: python script.py --logs_file_path path_to_logs_file --tags_file_path path_to_tags_file

**Output**:
The required outputs of i) Count of each tag in tags file and a count of untagged logs ii) Count of each destination port and protocol in the tags file

**Errors accounted for**:
1) Missing Command-line Arguments
The script checks if the log file path and tag file path are provided. 
If not, it exits with a message.
2) Invalid Protocol Names
If socket.getprotobyname() raises an exception due to an invalid protocol name in the tag file, 
the script catches the exception and prints an "invalid protocol name" message.
3) File Handling Errors
The script handles exceptions during file opening and reading, printing the exception message 
and exiting gracefully if something goes wrong.

**Time complexity**:
Tag File Parsing: O(n), where n is the number of lines in the tag file. Each line is processed once.
Log File Parsing: O(m), where m is the number of lines in the log file. Each line is processed once.
The overall time complexity is O(n + m).

**Space complexity**:
Space complexity is O(n + k), 
where n is the number of entries in the tag file and k is the number of unique destination port/protocol combinations in the log file.

**Sample input and output**:
1) Input files are given in the repo: tags.txt and logs.txt
2) Run from a shell (when logs.txt and tags.txt are in the same folder as the script):
   python script.py --logs_file_path logs.txt --tags_file_path tags.txt
3) Please check output.png in the repo
