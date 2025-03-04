#configParams.py is a file that contains the parameters used in the system, such as the database paths, the model paths, the source of the video, the services, the rectification dictionaries, the field names, the field status, the field record type, and the alphabet representation of numbers and letters.

from configparser import ConfigParser


class Parameters:

    def __init__(self):
        self.imgsz = 640
        self.conf_thres = 0.25
        self.max_det = 1000
        self.hide_conf = True

        self.region_threshold = 0.05

        self.color_blue = (255, 255, 0)
        self.color_red = (25, 20, 240)
        self.color = self.color_blue
        self.text_x_align = 10
        self.inference_time_y = 30
        self.fps_y = 90
        self.analysis_time_y = 60
        self.font_scale = 0.7
        self.thickness = 2
        self.rect_thickness = 3

        self.rect_size = 15000

        self.pred_shape = (480, 640, 3)
        self.vis_shape = (800, 600)

        config_object = ConfigParser()
        config_object.read("./config.ini")

        dbconfig = config_object["DATABASE"]
        self.dbEntries = dbconfig["dbentries"]
        self.dbResidents = dbconfig["dbresidents"]
        modelconfig = config_object["MODELCONFIG"]
        self.modelPlate_path = modelconfig["platemodel"]
        self.modelCharX_path = modelconfig["charmodel"]
        sourceConfig = config_object["SOURCEDETECT"]
        self.video = sourceConfig["video"]
        self.rtps = sourceConfig["rtps"]
        self.webcam = sourceConfig["webcam"]
        self.source = sourceConfig["source"]

        # services
        external_service_config = config_object["EXTERNAL-SERVICE"]
        self.external_service_url = external_service_config["url"]

        self.video_path = r"./prueba.mp4"

        # choose device; "cpu" or "cuda"(if cuda is available)
        self.cpu_or_cuda = "cuda"

        # Homography setup
        self.set_homography = False
        self.set_homography_manual = False
        self.src_points_manual = [[0, 0], [640, 0], [640, 480], [0, 480]]

        self.rectification_text_dict = {
            "0": "O",
            "1": "I",
            "6": "G",
            "8": "B",
        }  # [0, 1, 6, 8]
        self.rectification_nums_dict = {
            "O": "0",
            "I": "1",
            "G": "6",
            "B": "8",
        }  # [O, I, G, B]

        # English representation of numbers and letters
        self.alphabetP = {
            "ZERO": "0",
            "ONE": "1",
            "TWO": "2",
            "THREE": "3",
            "FOUR": "4",
            "FIVE": "5",
            "SIX": "6",
            "SEVEN": "7",
            "EIGHT": "8",
            "NINE": "9",
            "A": "A",
            "B": "B",
            "D": "D",
            "Gh": "Gh",
            "H": "H",
            "J": "J",
            "L": "L",
            "M": "M",
            "N": "N",
            "P": "P",
            "PuV": "PuV",
            "PwD": "PwD",
            "Sad": "Sad",
            "Sin": "Sin",
            "T": "T",
            "Taxi": "Taxi",
            "V": "V",
            "Y": "Y",
        }

        self.fieldNames = {
            "fName": "First Name",
            "lName": "Last Name",
            "building": "Building",
            "block": "Block",
            "num": "Number",
            "carModel": "Car Model",
            "plateNum": "License Plate",
            "status": "Permission",
            "time": "Time",
            "date": "Date",
            "platePic": "Plate Picture",
            "charPercent": "Character Percentage",
            "platePercent": "Plate Percentage",
            "editBtn": "Edit",
            "deleteBtn": "Delete",
            "searchBtn": "Search",
            "findEntriesBtn": "Entries",
            "moreInfo": "Show Information",
            "addNew": "Register Plate",
        }

        self.fieldStatus = {"0": "Unauthorized",
                            "1": "Authorized",
                            "2": "Unregistered"}

        self.fieldRecordType = {"0": "System", "1": "Manual", "2": "Edited"}


def getFieldNames(fieldsList):
    params = Parameters()
    fieldNamesOutput = []
    for value in fieldsList:
        fieldNamesOutput.append(params.fieldNames[value])
    return fieldNamesOutput
