from motorcontrol02 import init, forward, reverse, pivotleft, pivotright
from range02 import distance


def key_input(event):
    init()
    print("key: ", event)
    key_press = event
    tf = 1

    if key_press.lower() == 'w':
        forward(tf)
    elif key_press.lower() == 's':
        reverse(tf)
    elif key_press.lower() == 'a':
        pivotleft(tf)
    elif key_press.lower() == 'd':
        pivotright(tf)
    else:
        print("invalid key pressed!")


def mian():
    while True:
        time.sleep(1)
        print('distance ', distance(), ' cm')
        key_press = input('select driving mode: ')
        if key_press == 'p':
            break
        key_input(key_press)

if __name__ == '__main__':
    main()

