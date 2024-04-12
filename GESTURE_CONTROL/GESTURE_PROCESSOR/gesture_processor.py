import os
import time
import subprocess

#$$$$$$$$$$#

PROCESS_GESTURES = True

SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920

SCREENSHOT_TIME = 0
SCREENSHOT_THREASHOLD = 2

LAST_VOLUME_DETECTED = [0, 0]
LAST_BRIGHTNESS_DETECTED = [0, 0]

prev_cap = [0,0]
prev_cap_x = [0,0,0,0,0,0,0,0,0,0]*2
prev_cap_y = [0,0,0,0,0,0,0,0,0,0]*2

MOUSE_POINTER_CAPTURES = {"X": [0]*10,
                          "Y": [0]*10}

SPACEBAR_TIME = 0
SPACEBAR_THREASHOLD = 1.5

VOLUME_TIME = 0
VOLUME_COORDINATE = (0, 0)
VOLUME_COORDINATE_THREASHOLD = 0.05
VOLUME_THREASHOLD = 1.5

BRIGHTNESS_TIME = 0
BRIGHTNESS_COORDINATE = (0, 0)
BRIGHTNESS_COORDINATE_THREASHOLD = 0.05
BRIGHTNESS_THREASHOLD = 1.5

WORKSPACE_TIME = 0
WORKSPACE_COORDINATE = (0, 0)
WORKSPACE_THREASHOLD_X = 1.5
WORKSPACE_THREASHOLD_Y = 1.5

DRAG_PREVIOUS = False

LEFT_CLICK_TIME = 0
LEFT_CLICK_THREASHOLD = 0.5

RIGHT_CLICK_TIME = 0
RIGHT_CLICK_THREASHOLD = 1.5

SUPER_KEY_TIME = 0
SUPER_KEY_THREASHOLD = 1.5

fuck_you_detected = 0

#$$$$$$$$$$#

class GESTURE_PROCESSOR :
    def __init__(self) -> None :
        print("$$")
        pass

    def process_gesture(self,
                        data: dict[str:object]) -> None :
        global PROCESS_GESTURES

        data_iterable = {"hands": {},
                         "face": {},
                         "hollistic": []}

        if data["hands"].multi_hand_landmarks is None : return
        for _ in range(len(data["hands"].multi_hand_landmarks)) :
            data_iterable["hands"][_] = []
            for __ in range(21) :
                data_iterable["hands"][_].append([round(data["hands"].multi_hand_landmarks[_].landmark[__].x, 2),
                                                  round(data["hands"].multi_hand_landmarks[_].landmark[__].y, 2),
                                                  round(data["hands"].multi_hand_landmarks[_].landmark[__].z, 2)])

        gestures_found = {}

        self.check_gestures(data_iterable,
                            gestures_found)
        self.process_gestures(gestures_found,
                              data_iterable)

    def check_gestures(self,
                       data_iterable: dict[str:list[list[float]]],
                       gestures_found: dict[str:list]) -> None :
        self.check_fuck_you(data_iterable,
                            gestures_found)
        self.check_mouse_pointer(data_iterable,
                                 gestures_found)
        self.check_screenshot(data_iterable,
                              gestures_found)
        self.check_volume(data_iterable,
                          gestures_found)
        self.check_brightness(data_iterable,
                              gestures_found)
        self.check_workspace(data_iterable,
                             gestures_found)
        self.check_drag(data_iterable,
                        gestures_found)
        self.check_right_click(data_iterable,
                               gestures_found)
        self.check_space_bar(data_iterable,
                             gestures_found)
        self.check_super_key(data_iterable,
                             gestures_found)
        self.check_stop_processing(data_iterable,
                                   gestures_found)
        self.check_start_processing(data_iterable,
                                    gestures_found)

    def process_gestures(self,
                         gestures_found: dict[str:list],
                         data_iterable: dict[str:list[list[float]]]) -> None :
        self.process_stop_processing(gestures_found,
                                     data_iterable)
        self.process_start_processing(gestures_found,
                                      data_iterable)
        if PROCESS_GESTURES == True :
            print(gestures_found)
            self.process_fuck_you(gestures_found)
            self.process_screenshot(gestures_found)
            self.process_drag(gestures_found,
                              data_iterable)
            self.process_mouse_pointer(gestures_found,
                                       data_iterable)
            self.process_left_click(gestures_found,
                                    data_iterable)
            self.process_right_click(gestures_found,
                                     data_iterable)
            self.process_volume(gestures_found,
                                data_iterable)
            self.process_space_bar(gestures_found,
                                   data_iterable)
            self.process_brightness(gestures_found,
                                    data_iterable)
            self.process_workspace_switch(gestures_found,
                                          data_iterable)
            self.process_super_key(gestures_found,
                                   data_iterable)

    def check_fuck_you(self,
                       data_iterable: dict[str:list[list[float]]],
                       gestures_found: dict[str:list]) -> None :
        gestures_found["FUCK_YOU"] = []
        for _ in range(len(data_iterable["hands"])) :
            if ((data_iterable["hands"][_][12][1] <
                 data_iterable["hands"][_][11][1] <
                 data_iterable["hands"][_][10][1]) and (data_iterable["hands"][_][8][1] >
                                                        data_iterable["hands"][_][6][1]) and (data_iterable["hands"][_][16][1] >
                                                                                              data_iterable["hands"][_][15][1]) and (data_iterable["hands"][_][20][1] >
                                                                                                                                     data_iterable["hands"][_][18][1])) :
                gestures_found["FUCK_YOU"].append(_)

    def check_mouse_pointer(self,
                            data_iterable: dict[str:list[list[float]]],
                            gestures_found: dict[str:list]) -> None :
        gestures_found["MOUSE_POINTER"] = []
        for _ in range(len(data_iterable["hands"])) :
            if ((data_iterable["hands"][_][8][1] <
                 data_iterable["hands"][_][7][1] <
                 data_iterable["hands"][_][6][1] <
                 data_iterable["hands"][_][5][1]) and (data_iterable["hands"][_][12][1] >
                                                       data_iterable["hands"][_][10][1]) and (data_iterable["hands"][_][16][1] >
                                                                                              data_iterable["hands"][_][14][1]) and (data_iterable["hands"][_][20][1] >
                                                                                                                                     data_iterable["hands"][_][18][1])) :
                gestures_found["MOUSE_POINTER"].append(_)

    def check_right_click(self,
                          data_iterable: dict[str:list[list[float]]],
                          gestures_found: dict[str:list]) -> None :
        gestures_found["RIGHT_CLICK"] = []
        for _ in range(len(data_iterable["hands"])) :
            if ((data_iterable["hands"][_][20][1] <
                 data_iterable["hands"][_][19][1] <
                 data_iterable["hands"][_][18][1]) and (data_iterable["hands"][_][16][1] >
                                                        data_iterable["hands"][_][14][1]) and (data_iterable["hands"][_][12][1] >
                                                                                               data_iterable["hands"][_][10][1]) and (data_iterable["hands"][_][8][1] >
                                                                                                                                      data_iterable["hands"][_][6][1])) :
                if ((data_iterable["hands"][_][5][1] < data_iterable["hands"][_][17][1]) and
                    (data_iterable["hands"][_][4][0] > data_iterable["hands"][_][3][0])) :
                    gestures_found["RIGHT_CLICK"].append(_)
                if ((data_iterable["hands"][_][5][1] > data_iterable["hands"][_][17][1]) and
                    (data_iterable["hands"][_][4][1] < data_iterable["hands"][_][3][1])) :
                    gestures_found["RIGHT_CLICK"].append(_)

    def check_screenshot(self,
                         data_iterable: dict[str:list[list[float]]],
                         gestures_found: dict[str:list]) -> None :
        gestures_found["SCREENSHOT"] = []
        for _ in range(len(data_iterable["hands"])) :
            if ((data_iterable["hands"][_][8][1] <
                 data_iterable["hands"][_][7][1] <
                 data_iterable["hands"][_][6][1] <
                 data_iterable["hands"][_][5][1]) and (data_iterable["hands"][_][12][1] >
                                                       data_iterable["hands"][_][10][1]) and (data_iterable["hands"][_][16][1] >
                                                                                              data_iterable["hands"][_][14][1]) and (data_iterable["hands"][_][20][1] <
                                                                                                                                     data_iterable["hands"][_][19][1] <
                                                                                                                                     data_iterable["hands"][_][18][1] <
                                                                                                                                     data_iterable["hands"][_][17][1]) and ((data_iterable["hands"][_][4][0] <
                                                                                                                                                                             data_iterable["hands"][_][3][0] <
                                                                                                                                                                             data_iterable["hands"][_][2][0] <
                                                                                                                                                                             data_iterable["hands"][_][1][0]) or (data_iterable["hands"][_][4][0] >
                                                                                                                                                                                                                  data_iterable["hands"][_][3][0] >
                                                                                                                                                                                                                  data_iterable["hands"][_][2][0] >
                                                                                                                                                                                                                  data_iterable["hands"][_][1][0]))) :
                gestures_found["SCREENSHOT"].append(_)

    def check_volume(self,
                     data_iterable: dict[str:list[list[float]]],
                     gestures_found: dict[str:list]) -> None :
        gestures_found["VOLUME"] = []
        for _ in range(len(data_iterable["hands"])) :
            if ((data_iterable["hands"][_][8][1] <
                 data_iterable["hands"][_][7][1] <
                 data_iterable["hands"][_][6][1] <
                 data_iterable["hands"][_][5][1]) and (data_iterable["hands"][_][12][1] >
                                                       data_iterable["hands"][_][10][1]) and (data_iterable["hands"][_][16][1] >
                                                                                              data_iterable["hands"][_][14][1]) and (data_iterable["hands"][_][20][1] <
                                                                                                                                     data_iterable["hands"][_][19][1] <
                                                                                                                                     data_iterable["hands"][_][18][1] <
                                                                                                                                     data_iterable["hands"][_][17][1]) and ((data_iterable["hands"][_][5][0] <
                                                                                                                                                                             data_iterable["hands"][_][4][0] <
                                                                                                                                                                             data_iterable["hands"][_][17][0]) or (data_iterable["hands"][_][5][0] >
                                                                                                                                                                                                                   data_iterable["hands"][_][4][0] >
                                                                                                                                                                                                                   data_iterable["hands"][_][17][0]))) :
                gestures_found["VOLUME"].append(_)

    def check_brightness(self,
                         data_iterable: dict[str:list[list[float]]],
                         gestures_found: dict[str:list]) -> None :
        gestures_found["BRIGHTNESS"] = []
        for _ in range(len(data_iterable["hands"])) :
            if not ((data_iterable["hands"][_][8][1] <
                     data_iterable["hands"][_][7][1] <
                     data_iterable["hands"][_][6][1] <
                     data_iterable["hands"][_][5][1]) and (data_iterable["hands"][_][12][1] <
                                                           data_iterable["hands"][_][11][1] <
                                                           data_iterable["hands"][_][10][1] <
                                                           data_iterable["hands"][_][9][1]) and (data_iterable["hands"][_][16][1] <
                                                                                                 data_iterable["hands"][_][15][1] <
                                                                                                 data_iterable["hands"][_][14][1] <
                                                                                                 data_iterable["hands"][_][13][1]) and (data_iterable["hands"][_][20][1] <
                                                                                                                                        data_iterable["hands"][_][19][1] <
                                                                                                                                        data_iterable["hands"][_][18][1] <
                                                                                                                                        data_iterable["hands"][_][17][1]) and ((data_iterable["hands"][_][5][0] <
                                                                                                                                                                                data_iterable["hands"][_][4][0] <
                                                                                                                                                                                data_iterable["hands"][_][17][0]) or (data_iterable["hands"][_][5][0] >
                                                                                                                                                                                                                      data_iterable["hands"][_][4][0] >
                                                                                                                                                                                                                      data_iterable["hands"][_][17][0]))) :
                continue
            if not ((abs(data_iterable["hands"][_][8][0] - data_iterable["hands"][_][12][0]) >
                     abs(data_iterable["hands"][_][5][0] - data_iterable["hands"][_][9][0])) and (abs(data_iterable["hands"][_][12][0] - data_iterable["hands"][_][16][0]) >
                                                                                                  abs(data_iterable["hands"][_][9][0] - data_iterable["hands"][_][13][0])) and (abs(data_iterable["hands"][_][16][0]-data_iterable["hands"][_][20][0]) >
                                                                                                                                                                                abs(data_iterable["hands"][_][13][0]-data_iterable["hands"][_][17][0]))) :
                continue
            gestures_found["BRIGHTNESS"].append(_)

    def check_workspace(self,
                        data_iterable: dict[str:list[list[float]]],
                        gestures_found: dict[str:list]) -> None :
        gestures_found["WORKSPACE"] = []
        for _ in range(len(data_iterable["hands"])) :
            if not ((data_iterable["hands"][_][8][1] <
                     data_iterable["hands"][_][7][1] <
                     data_iterable["hands"][_][6][1] <
                     data_iterable["hands"][_][5][1]) and (data_iterable["hands"][_][12][1] <
                                                           data_iterable["hands"][_][11][1] <
                                                           data_iterable["hands"][_][10][1] <
                                                           data_iterable["hands"][_][9][1]) and (data_iterable["hands"][_][16][1] <
                                                                                                 data_iterable["hands"][_][15][1] <
                                                                                                 data_iterable["hands"][_][14][1] <
                                                                                                 data_iterable["hands"][_][13][1]) and (data_iterable["hands"][_][20][1] >
                                                                                                                                        data_iterable["hands"][_][19][1]) and ((data_iterable["hands"][_][5][0] <
                                                                                                                                                                                data_iterable["hands"][_][4][0] <
                                                                                                                                                                                data_iterable["hands"][_][17][0]) or (data_iterable["hands"][_][5][0] >
                                                                                                                                                                                                                      data_iterable["hands"][_][4][0] >
                                                                                                                                                                                                                      data_iterable["hands"][_][17][0]))) :
                return
            if not ((abs(data_iterable["hands"][_][8][0] - data_iterable["hands"][_][12][0]) <
                     abs(data_iterable["hands"][_][5][0] - data_iterable["hands"][_][9][0])*1.5) and (abs(data_iterable["hands"][_][12][0] - data_iterable["hands"][_][16][0]) <
                                                                                                      abs(data_iterable["hands"][_][9][0] - data_iterable["hands"][_][13][0])*1.5)) :
                return
            gestures_found["WORKSPACE"].append(_)

    def check_drag(self,
                   data_iterable: dict[str:list[list[float]]],
                   gestures_found: dict[str:list]) -> None :
        gestures_found["DRAG"] = []
        for _ in range(len(data_iterable["hands"])) :
            if not ((data_iterable["hands"][_][8][1] <
                     data_iterable["hands"][_][7][1] <
                     data_iterable["hands"][_][6][1] <
                     data_iterable["hands"][_][5][1]) and (data_iterable["hands"][_][12][1] <
                                                           data_iterable["hands"][_][11][1] <
                                                           data_iterable["hands"][_][10][1] <
                                                           data_iterable["hands"][_][9][1]) and (data_iterable["hands"][_][16][1] >
                                                                                                 data_iterable["hands"][_][15][1] >
                                                                                                 data_iterable["hands"][_][14][1]) and (data_iterable["hands"][_][20][1] >
                                                                                                                                        data_iterable["hands"][_][19][1] >
                                                                                                                                        data_iterable["hands"][_][18][1])) :
                continue
            if not (abs(data_iterable["hands"][_][12][0]-
                        data_iterable["hands"][_][8][0]) < abs(data_iterable["hands"][_][9][0]-
                                                               data_iterable["hands"][_][5][0])*1.5) :
                continue
            gestures_found["DRAG"].append(_)

    def check_space_bar(self,
                        data_iterable: dict[str:list[list[float]]],
                        gestures_found: dict[str:list]) -> None :
        gestures_found["SPACE_BAR"] = []
        for _ in range(len(data_iterable["hands"])) :
            if not ((data_iterable["hands"][_][8][1] >
                     data_iterable["hands"][_][7][1] >
                     data_iterable["hands"][_][6][1]) and (data_iterable["hands"][_][12][1] >
                                                           data_iterable["hands"][_][11][1] >
                                                           data_iterable["hands"][_][10][1]) and (data_iterable["hands"][_][16][1] >
                                                                                                  data_iterable["hands"][_][15][1] >
                                                                                                  data_iterable["hands"][_][14][1])) :
                continue
            if not (((data_iterable["hands"][_][4][0] <
                      data_iterable["hands"][_][3][0] <
                      data_iterable["hands"][_][2][0] <
                      data_iterable["hands"][_][1][0]) and (data_iterable["hands"][_][20][0] >
                                                            data_iterable["hands"][_][19][0] >
                                                            data_iterable["hands"][_][18][0] >
                                                            data_iterable["hands"][_][17][0])) or ((data_iterable["hands"][_][4][0] >
                                                                                                    data_iterable["hands"][_][3][0] >
                                                                                                    data_iterable["hands"][_][2][0] >
                                                                                                    data_iterable["hands"][_][1][0]) and (data_iterable["hands"][_][20][0] <
                                                                                                                                          data_iterable["hands"][_][19][0] <
                                                                                                                                          data_iterable["hands"][_][18][0] <
                                                                                                                                          data_iterable["hands"][_][17][0]))) :
                continue
            gestures_found["SPACE_BAR"].append(_)

    def check_stop_processing(self,
                              data_iterable: dict[str:list[list[float]]],
                              gestures_found: dict[str:list]) -> None :
        gestures_found["STOP_PROCESSING"] = []
        if len(gestures_found["MOUSE_POINTER"]) == 2 :
            if data_iterable["hands"][0][0][0] < data_iterable["hands"][1][0][0] :
                hand_one = 0
                hand_two = 1
            else :
                hand_one = 1
                hand_two = 0

            if (((data_iterable["hands"][hand_one][8][0] > data_iterable["hands"][hand_two][8][0]) and
                 (data_iterable["hands"][hand_one][5][0] < data_iterable["hands"][hand_two][5][0]) and
                 (abs(data_iterable["hands"][hand_one][6][1]-data_iterable["hands"][hand_two][6][1]) <
                  abs(data_iterable["hands"][hand_one][8][1]-data_iterable["hands"][hand_one][7][1])) )) :
                gestures_found["STOP_PROCESSING"].append(0)
                gestures_found["STOP_PROCESSING"].append(1)

    def check_start_processing(self,
                               data_iterable: dict[str:list[list[float]]],
                               gestures_found: dict[str:list]) -> None :
        gestures_found["START_PROCESSING"] = []
        if len(gestures_found["MOUSE_POINTER"]) == 2 :
            if data_iterable["hands"][0][0][0] < data_iterable["hands"][1][0][0] :
                hand_one = 0
                hand_two = 1
            else :
                hand_one = 1
                hand_two = 0

            if ((abs(data_iterable["hands"][hand_one][8][0] - data_iterable["hands"][hand_two][8][0]) <
                 abs(data_iterable["hands"][hand_one][8][0] - data_iterable["hands"][hand_one][7][0])) and
                (abs(data_iterable["hands"][hand_one][4][0] - data_iterable["hands"][hand_two][4][0]) <
                 abs(data_iterable["hands"][hand_one][4][0] - data_iterable["hands"][hand_one][3][0]))) :
                gestures_found["START_PROCESSING"].append(0)
                gestures_found["START_PROCESSING"].append(1)

    def check_super_key(self,
                        data_iterable: dict[str:list[list[float]]],
                        gestures_found: dict[str:list]) -> None :
        gestures_found["SUPER_KEY"] = []
        for _ in range(len(data_iterable["hands"])) :
            if ((data_iterable["hands"][_][8][1] > data_iterable["hands"][_][6][1]) and
                (data_iterable["hands"][_][12][1] < data_iterable["hands"][_][10][1]) and
                (data_iterable["hands"][_][16][1] < data_iterable["hands"][_][14][1]) and
                (data_iterable["hands"][_][20][1] < data_iterable["hands"][_][18][1])) :
                gestures_found["SUPER_KEY"].append(_)



    def process_fuck_you(self,
                         gestures_found: dict[str:list]) -> None :
        if len(gestures_found["FUCK_YOU"]) < 2 : return
        os.system("shutdown -h now")

    def process_screenshot(self,
                           gestures_found: dict[str:list]) -> None :
        global SCREENSHOT_TIME, SCREENSHOT_THREASHOLD
        if gestures_found["SCREENSHOT"] == [] : return
        if (SCREENSHOT_TIME + SCREENSHOT_THREASHOLD) > time.time() : return
        print("#", os.environ.get("USERNAME"))
        if os.environ.get("USERNAME") != None :
            os.system("gnome-screenshot -f ~/Pictures/Screenshots/{0}.png".format("GESTURE_CONTROL"+
                                                                                  str(int(time.time()*(10**7)))))
        else :
            users = os.listdir("/home")
            print("$", users)
            time_= time.time()
            os.system("gnome-screenshot -f /home/{0}/Pictures/Screenshots/{1}.png".format(users[0], "GESTURE_CONTROL"+
                                                                                                    str(int(time_*(10**7)))))
            for _ in range(1, len(users)) :
                os.system("sudo cp /home/{0}/Pictures/Screenshots/{1}.png /home/{2}/Pictures/Screenshots/{1}.png".format(users[0],
                                                                                                                         "GESTURE_CONTROL"+str(int(time_*(10**7))), users[_]))
        SCREENSHOT_TIME = time.time()

    def process_mouse_pointer(self,
                              gestures_found: dict[str:list],
                              data_iterable: dict[str:list[list[float]]]) -> None :
        global SCREEN_WIDTH, SCREEN_HEIGHT, MOUSE_CAPTURES
        if gestures_found["MOUSE_POINTER"] == [] and gestures_found["DRAG"] == [] : return

        max_x = 0
        min_x = SCREEN_WIDTH*2
        max_y = 0
        min_y = SCREEN_HEIGHT*2

        for _ in data_iterable["hands"][0] :
            if _[0] < min_x : min_x = max(_[0], 0)
            if _[0] > max_x : max_x = min(_[0], 1)
            if _[1] < min_y : min_y = max(_[1], 0)
            if _[1] > max_y : max_y = min(_[1], 1)

        correction_x = (max_x - min_x)/(1 - (max_x - min_x))
        correction_y = (max_y - min_y)/(1 - (max_y - min_y))

        coordinates = [min(max(int((data_iterable["hands"][0][8][0])*SCREEN_WIDTH), 0), SCREEN_WIDTH),
                       min(max(int((data_iterable["hands"][0][8][1]*(1 + correction_y))*SCREEN_HEIGHT), 0), SCREEN_HEIGHT)]
       
        MOUSE_POINTER_CAPTURES["X"].append(coordinates[0])
        MOUSE_POINTER_CAPTURES["X"].pop(0)
        MOUSE_POINTER_CAPTURES["Y"].append(coordinates[1])
        MOUSE_POINTER_CAPTURES["Y"].pop(0)

        os.system("xdotool mousemove {0} {1}".format(sum(MOUSE_POINTER_CAPTURES["X"])//len(MOUSE_POINTER_CAPTURES["Y"]),
                                                     sum(MOUSE_POINTER_CAPTURES["Y"])//len(MOUSE_POINTER_CAPTURES["Y"])))

    def process_volume(self,
                       gestures_found: dict[str:list],
                       data_iterable: dict[str:list[list[float]]]) -> None :
        global VOLUME_TIME, VOLUME_THREASHOLD, VOLUME_TIME, VOLUME_COORDINATE_THREASHOLD, VOLUME_COORDINATE
        if gestures_found["VOLUME"] == [] : return
        if (time.time() - VOLUME_TIME) > VOLUME_THREASHOLD :
            VOLUME_COORDINATE = data_iterable["hands"][gestures_found["VOLUME"][0]][0]
        
        VOLUME_TIME = time.time()

        if abs(VOLUME_COORDINATE[1] - data_iterable["hands"][gestures_found["VOLUME"][0]][0][1]) > VOLUME_COORDINATE_THREASHOLD :
            if VOLUME_COORDINATE[1] > data_iterable["hands"][gestures_found["VOLUME"][0]][0][1] :
                os.system("amixer -D pulse sset Master 10%+")
            elif VOLUME_COORDINATE[1] < data_iterable["hands"][gestures_found["VOLUME"][0]][0][1] :
                os.system("amixer -D pulse sset Master 10%-")
            VOLUME_COORDINATE = data_iterable["hands"][gestures_found["VOLUME"][0]][0]

    def process_brightness(self,
                           gestures_found: dict[str:list],
                           data_iterable: dict[str:list[list[float]]]) -> None :
        global BRIGHTNESS_TIME, BRIGHTNESS_THREASHOLD, BRIGHTNESS_TIME, BRIGHTNESS_COORDINATE_THREASHOLD, BRIGHTNESS_COORDINATE
        if gestures_found["BRIGHTNESS"] == [] : return
        if (time.time() - BRIGHTNESS_TIME) > BRIGHTNESS_THREASHOLD :
            BRIGHTNESS_COORDINATE = data_iterable["hands"][gestures_found["BRIGHTNESS"][0]][0]

        BRIGHTNESS_TIME = time.time()

        if abs(BRIGHTNESS_COORDINATE[1] - data_iterable["hands"][gestures_found["BRIGHTNESS"][0]][0][1]) > BRIGHTNESS_COORDINATE_THREASHOLD :
            if BRIGHTNESS_COORDINATE[1] > data_iterable["hands"][gestures_found["BRIGHTNESS"][0]][0][1] :
                os.system("sudo brightnessctl set 10%+")
            elif BRIGHTNESS_COORDINATE[1] < data_iterable["hands"][gestures_found["BRIGHTNESS"][0]][0][1] :
                os.system("sudo brightnessctl set 10%-")
            BRIGHTNESS_COORDINATE = data_iterable["hands"][gestures_found["BRIGHTNESS"][0]][0]

    def process_space_bar(self,
                          gestures_found: dict[str:list],
                          data_iterable: dict[str:list[list[float]]]) -> None :
        global SPACEBAR_TIME, SPACEBAR_THREASHOLD
        if gestures_found["SPACE_BAR"] == [] : return
        if (time.time() - SPACEBAR_TIME) > SPACEBAR_THREASHOLD :
            os.system("xdotool key space")
            SPACEBAR_TIME = time.time()

    def process_stop_processing(self,
                                gestures_found: dict[str:list],
                                data_iterable: dict[str:list[list[float]]]) -> None :
        global PROCESS_GESTURES
        if gestures_found["STOP_PROCESSING"] != [] :
            PROCESS_GESTURES = False

    def process_start_processing(self,
                                 gestures_found: dict[str:list],
                                 data_iterable: dict[str:list[list[float]]]) -> None :
        global PROCESS_GESTURES
        if gestures_found["START_PROCESSING"] != [] :
            PROCESS_GESTURES = True

    def process_enter_button(self,
                             gesture_found: dict[str:list],
                             data_iterable: dict[str:list[list[float]]]) -> None :
        pass

    def process_super_key(self,
                           gestures_found: dict[str:list],
                           data_iterable: dict[str:list[list[float]]]) -> None :
        global SUPER_KEY_TIME, SUPER_KEY_THREASHOLD

        if gestures_found["SUPER_KEY"] == [] : return
        if (time.time() - SUPER_KEY_TIME) < SUPER_KEY_THREASHOLD : return
        os.system("xdotool key Super")
        SUPER_KEY_TIME = time.time()

    def process_workspace_switch(self,
                                 gestures_found: dict[str:list],
                                 data_iterable: dict[str:list[list[float]]]) -> None :
        global WORKSPACE_TIME, WORKSPACE_COORDINATE, WORKSPACE_THREASHOLD_X, WORKSPACE_THREASHOLD_Y
        if gestures_found["WORKSPACE"] == [] : return
        if (time.time() - WORKSPACE_TIME) > WORKSPACE_THREASHOLD_X :
            WORKSPACE_COORDINATE = data_iterable["hands"][gestures_found["WORKSPACE"][0]][0]
        else : return

        if data_iterable["hands"][gestures_found["WORKSPACE"][0]][0][0] < 0.3 :
            os.system("xdotool keydown alt+ctrl key Left keyup alt+ctrl")
            WORKSPACE_COORDINATE = data_iterable["hands"][gestures_found["WORKSPACE"][0]][0]
            WORKSPACE_TIME = time.time()
        if data_iterable["hands"][gestures_found["WORKSPACE"][0]][0][0] > 0.7 :
            os.system("xdotool keydown alt+ctrl key Right keyup alt+ctrl")
            WORKSPACE_COORDINATE = data_iterable["hands"][gestures_found["WORKSPACE"][0]][0]
            WORKSPACE_TIME = time.time()

    def process_drag(self,
                     gestures_found: dict[str:list],
                     data_iterable: dict[str:list[list[float]]]) -> None :
        global DRAG_PREVIOUS

        if DRAG_PREVIOUS == True :
            if len(gestures_found["DRAG"]) != 0 :
                pass
            else :
                os.system("xdotool mouseup 1")
                DRAG_PREVIOUS = False
        if DRAG_PREVIOUS == False :
            if len(gestures_found["DRAG"]) != 0 :
                os.system("xdotool mousedown 1")
                DRAG_PREVIOUS = True
            else :
                pass

    def process_left_click(self,
                           gestures_found: dict[str:list],
                           data_iterable: dict[str:list[list[float]]]) -> None :
        global LEFT_CLICK_THREASHOLD, LEFT_CLICK_TIME

        if (time.time()  - LEFT_CLICK_TIME) < LEFT_CLICK_THREASHOLD : return
        if gestures_found["MOUSE_POINTER"] == [] : return
        if data_iterable["hands"][gestures_found["MOUSE_POINTER"][0]][5][0] < data_iterable["hands"][gestures_found["MOUSE_POINTER"][0]][17][0] :
            if data_iterable["hands"][gestures_found["MOUSE_POINTER"][0]][4][0] > data_iterable["hands"][gestures_found["MOUSE_POINTER"][0]][5][0] :
                os.system("xdotool click 1")
                LEFT_CLICK_TIME = time.time()
        if data_iterable["hands"][gestures_found["MOUSE_POINTER"][0]][5][0] > data_iterable["hands"][gestures_found["MOUSE_POINTER"][0]][17][0] :
            if data_iterable["hands"][gestures_found["MOUSE_POINTER"][0]][4][0] < data_iterable["hands"][gestures_found["MOUSE_POINTER"][0]][5][0] :
                os.system("xdotool click 1")
                LEFT_CLICK_TIME = time.time()

    def process_right_click(self,
                            gestures_found: dict[str:list],
                            data_iterable: dict[str:list[list[float]]]) -> None :
        global RIGHT_CLICK_THREASHOLD, RIGHT_CLICK_TIME

        if (time.time()  - RIGHT_CLICK_TIME) < RIGHT_CLICK_THREASHOLD : return
        if gestures_found["RIGHT_CLICK"] == [] : return
        
        os.system("xdotool click 3")
        RIGHT_CLICK_TIME = time.time()
