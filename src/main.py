from right_sandal_handler import *

def main():
    right_sandal_handler = RightSandalHandler()
    right_sandal_handler.start()
    right_sandal_handler.mqtt_client.loop_start()





if __name__ == "__main__":
    main()
