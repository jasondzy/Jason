from greenlet import greenlet
from time import sleep
def funca():
    while True:
        print('-----A-------')
        gr2.switch()
        print('---switch to funca---')
        sleep(0.5)

def funcb():
    while True:
        print('----B---------')
        gr1.switch()
        print('---switch to funcb----')
        sleep(0.5)



gr1 = greenlet(funca)
gr2 = greenlet(funcb)

def main():
    gr1.switch()

if __name__ == '__main__':
    main()