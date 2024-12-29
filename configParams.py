

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

        self.video_path = r"./anpr_video.mp4"
        self.cpu_or_cuda = "cpu"  # choose device; "cpu" or "cuda"(if cuda is available)

        self.label_map = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'D', 'Gh', 'H', 'J', 'L', 'M',
                         'N', 'P', 'PuV', 'PwD', 'Sad', 'Sin', 'T', 'Taxi', 'V', 'Y']

        self.char_dict = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8',
                         '9': '9', 'A': '10', 'B': '11', 'P': '12', 'Taxi': '13', 'A': '14', 'J': '15', 'Ch': '16',
                         'H': '17', 'Kh': '18', 'D': '19', 'Th': '20', 'R': '21', 'Z': '22', 'Zh': '23', 'Sin': '24',
                         'Sh': '25', 'Sad': '26', 'Dh': '27', 'T': '28', 'Tz': '29', 'PuV': '30', 'Gh': '31',
                         'F': '32', 'Gh': '33', 'K': '34', 'G': '35', 'L': '36', 'M': '37', 'N': '38', 'H': '39',
                         'V': '40', 'Y': '41', 'PwD': '42'}

        self.char_id_dict = {v: k for k, v in self.char_dict.items()}

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

        self.alphabetP2 = self.alphabetP.copy()

        self.alphabetE = {
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
            'ALEF': 'A',
            'BEH': 'B',
            'DAL': 'D',
            'QAF': 'Gh',
            'HEH': 'H',
            'JEEM': 'J',
            'LAM': 'L',
            'MEEM': 'M',
            'NOON': 'N',
            'PEH': 'P',
            'AIN': 'PuV',
            'JEH': 'PwD',
            'SAD': 'Sad',
            'SEEN': 'Sin',
            'TAH': 'T',
            'TEH': 'Taxi',
            'WAW': 'V',
            'YEH': 'Y',
        }

        self.plateAlphabet = {
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
            'fName': 'First Name',
            'lName': 'Last Name',
            'building': 'Building',
            'block': 'Block',
            'num': 'Number',
            'carModel': 'Car Model',
            'plateNum': 'License Plate',
            'status': 'Permission',
            'time': 'Time',
            'date': 'Date',
            'platePic': 'Plate Picture',
            'charPercent': 'Character Percentage',
            'platePercent': 'Plate Percentage',
            'editBtn': 'Edit',
            'deleteBtn': 'Delete',
            'searchBtn': 'Search',
            'findEntriesBtn': 'Entries',
            'moreInfo': 'Show Information',
            'addNew': 'Register Plate',
        }

        self.fieldStatus = {
            '0': 'Unauthorized',
            '1': 'Authorized',
            '2': 'Unregistered'
        }

        self.fieldRecordType = {
            '0': 'System',
            '1': 'Manual',
            '2': 'Edited'
        }


def getFieldNames(fieldsList):
    params = Parameters()
    fieldNamesOutput = []
    for value in fieldsList:
        fieldNamesOutput.append(params.fieldNames[value])
    return fieldNamesOutput