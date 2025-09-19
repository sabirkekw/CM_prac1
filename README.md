# REPL Shell Implementation 
This Python script implements a simple Read-Eval-Print Loop (REPL) shell that mimics some basic shell functionality.  

## Features
**User and Host Identification:** Displays the current user and hostname in the prompt 

**Environment Variable Expansion:** Supports expanding environment variables prefixed with $  

**Basic Command Support:**

    exit: Terminates the shell session  

    ls: Lists directory contents (placeholder implementation)  

    cd: Changes directory (placeholder implementation)  

## Usage

Run the script with Python 3:

    python3 script_name.py

You'll see a prompt in the format:

    ~$username.hostname:

## Environment Variable Expansion

You can use environment variables in commands by prefixing them with $:

    ~$username.hostname: $HOME

This will expand $HOME to the value of the HOME environment variable.

## Supported Commands

    exit: Exit the REPL shell

    ls: List directory contents (currently just prints the command and arguments)

    cd: Change directory (currently just prints the command and arguments)

    Any command starting with $: Expands and prints the environment variable

## Example Session

    ~$Redmi.DESKTOP-VS2RB0P: ls -l
    ls 
     -l
    ~$Redmi.DESKTOP-VS2RB0P: $WINDIR
    C:\Windows
    ~$Redmi.DESKTOP-VS2RB0P: exit

## Implementation Details

The script uses:

    getpass.getuser() to get the current username

    socket.gethostname() to get the system hostname

    os.environ.get() to access environment variables

    Simple string parsing to handle commands and arguments

## Limitations

This is a basic implementation with placeholder functionality for most commands. In a real shell, you would want to:

    Actually execute the ls and cd commands using os.listdir() and os.chdir()

    Add more shell commands and features

    Handle errors gracefully

    Implement proper input parsing (quotes, escape sequences, etc.)

## File Structure

    .
    ├── shell.py          # Main REPL implementation
    └── README.md         # This documentation file
