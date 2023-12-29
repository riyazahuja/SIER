import sys
import os




def parse_input(data):
    data = data.split(" ")

    match data[0]:
        case "h":
            pass
        case "help":
            print("HELP")
        case "clr":
            pass
        case "clear":
            print("CLEAR")
        case 'q':
            pass
        case 'quit':
            return -1
        case "u":
            pass
        case "user":
            handle_user(data)
        
    




def main(argv):
    while(True):
        print('sier >', end = " ")
        inp = input()
        sig = parse_input(inp)
        if(sig == -1):
            break
    

if __name__ == '__main__':
    main(sys.argv)



