# KEYLOGGER - AN INDEPENDENT PROJECT (FOR ACADEMIC PURPOSES)
# BY ANDREW COTAJ
# SUMMER 2024

# OVERVIEW
    # In general terminology, a Keylogger is a program that is used to generally record the keystrokes made by a user. Often used in a malicious setting - a keylogger is many times incorporated into viruses/malware to steal account information or financial information. 
    # This Keylogger, which I have been working on for the past few months, is an advanced version of a Keylogger that would be more similar to the ones seen in legal and illegal use. It is important to note that although this project is for academic purposes, the use of a Keylogger in a malicious context (to steal information from an unsuspecting user) is illegal and ethically corrupt. 
    # This Keylogger includes the basics, which include recording keystrokes and mouse position/movements/operations - which are all grouped into a text file. The text file in question is automatically named according to the date of creation, and the start and end times of the program are also recorded in the same file. This Keylogger also has the ability to identify/record to the text file what applications or windows are opened/active and currently being used by the user. The program can be exited through a designated STOP_KEY, which in this use is the ESC button. This is a characteristic that is not used in official implementations and has mainly been included to prevent malicious use. Upon the program being exited, the Keylogger program has the ability to utilize an SMTP server with TLS encryption (in this case, that belonging to Google's Gmail), and send an email from a predefined email to a recipient email, with the text file from the recording included as an attachment. For the sake of display purposes, and to again diminish the chance of malicious use as well as to avoid violating Gmail's terms of service, the email operations will not be displayed in the demonstration video. Also, crucial details involving 2FA have been omitted from the code to discourage illicit use once again. 

# RESOURCES/INSTRUCTIONS/MANUALS:
    # PYNPUT LIBRARIES/RESOURCES:
        # @buildwithpython on YouTube - attreyabhatt on GitHub
        # Official Instruction Manual: https://pynput.readthedocs.io/en/latest/index.html#
        # Example Implementations: https://pypi.org/project/pynput/ 
    # EMAIL LIBRARIES/RESOURCES:
        # Official Instruction Manual: https://docs.python.org/3/library/email.html 
    # SMTP LIBRARIES/RESOURCES:
        # Official Instruction Manual: https://docs.python.org/3/library/smtplib.html#module-smtplib
    # DATETIME LIBRARIES/RESOURCES:
        # Unofficial Instruction Set w/ Examples: https://www.w3schools.com/python/python_datetime.asp 
    # CTYPES LIBRARIES/RESOURCES:
        # Official Instruction Manual: https://docs.python.org/3/library/ctypes.html
    # SUBPROCESS LIBRARIES/RESOURCES:
        # Official Instruction Manual: https://docs.python.org/3/library/subprocess.html 
        # Information Learned from CSE 20289 taught by Peter Bui at the University of Notre Dame
    # PLATFORM LIBRARIES/RESOURCES:
        # Official Instruction Manual: https://docs.python.org/3/library/platform.html
