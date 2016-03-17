from asyncio import get_event_loop
from Server import Server

def main():
    loop = get_event_loop()
    Server(loop, 5000)
    loop.run_forever()

if __name__ == '__main__':
    main()