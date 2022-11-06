#this is the base to some interface class 
from hello import baseCall

def main():
    base = baseCall()
    print("This is base")
    #maybe a switch goes here
    print("calling hello.py now")
    base.callsocket()


if __name__ == '__main__':
    main()
