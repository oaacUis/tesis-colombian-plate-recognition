# home-yolo.py

"""
Main script to run the License Plate Recognition (LPR) application. This application
uses deep learning models to detect and recognize license plates and characters.
It is built with PySide6 for the GUI and utilizes PyTorch for model inference.

Requirements:
- PySide6 for the GUI
- PyTorch for deep learning inference
- Pillow for image processing
- OpenCV for video and image manipulation
- NumPy for numerical operations
"""
from ultralytics import YOLO
import pandas as pd
import functools
import gc
import statistics
import time
import warnings
from pathlib import Path
import torch
from PIL import ImageOps
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QThread, Signal, QSize
from PySide6.QtGui import QImage, QIcon, QAction, QPainter
from PySide6.QtWidgets import QTableWidgetItem, QGraphicsScene
from qtpy.uic import loadUi

import ai.img_model as imgModel
from ai.img_model import *
from configParams import Parameters
from database.db_entries_utils import db_entries_time, dbGetAllEntries
from database.db_resident_utils import db_get_plate_status, db_get_plate_owner_name
from enteries_window import EnteriesWindow
from helper.gui_maker import configure_main_table_widget, create_image_label, on_label_double_click, center_widget, \
    get_status_text, get_status_color, \
    create_styled_button
from helper.text_decorators import convert_to_local_format, clean_license_plate_text, join_elements, \
    convert_to_standard_format, split_string_language_specific
from resident_view import residentView
from residents_edit import residentsAddNewWindow
from residents_main import residentsWindow

warnings.filterwarnings("ignore", category=UserWarning)
params = Parameters()
import sys

sys.path.append('model')


def get_device():
    """
    Determines the device to run the PyTorch models on.
    Returns a torch.device object representing the device (CUDA, MPS, or CPU).
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")

try:
    # modelPlate = torch.hub.load('model', 'custom', params.modelPlate_path, source='local', force_reload=True)
    modelPlate = YOLO(params.modelPlate_path)
    # modelPlate = modelPlate.to(device())

    # modelCharX = torch.hub.load('model', 'custom', params.modelCharX_path, source='local', force_reload=True)
    modelCharX = YOLO(params.modelCharX_path)
    print("Models loaded successfully")

except Exception as e:
    print("Error loading the model")
    print("Error description: ", e)


class MainWindow(QtWidgets.QMainWindow):
    """
    The main window class of the LPR application.
    It sets up the user interface and connects signals and slots.
    """

    def __init__(self):
        """
       Initializes the main window and its components.
       """
        super(MainWindow, self).__init__()
        loadUi('./gui/mainFinal.ui', self)
        self.setFixedSize(self.size())

        self.camImage = None
        self.plateImage = None
        self.residentsWindow = None
        self.enterieswindow = None
        self.startButton.clicked.connect(self.start_webcam)
        self.stopButton.clicked.connect(self.stop_webcam)
        self.usersListButton.clicked.connect(self.show_residents_list)
        self.enteriesListButton.clicked.connect(self.show_entries_list)

        exitAct = QAction("Exit", self)
        exitAct.setShortcut("Ctrl+Q")

        self.startButton.setIcon(QPixmap("./icons/icons8-play-80.png"))
        self.startButton.setIconSize(QSize(40, 40))

        self.stopButton.setIcon(QPixmap("./icons/icons8-stop-80.png"))
        self.stopButton.setIconSize(QSize(40, 40))

        self.usersListButton.setIcon(QPixmap("./icons/icons8-people-64.png"))
        self.usersListButton.setIconSize(QSize(40, 40))

        self.enteriesListButton.setIcon(QPixmap("./icons/icons8-car-80.png"))
        self.enteriesListButton.setIconSize(QSize(40, 40))

        self.settingsButton.setIcon(QPixmap("./icons/icons8-tools-80.png"))
        self.settingsButton.setIconSize(QSize(40, 40))

        self.plateTextView.setStyleSheet(
            f"""border-image: url("{Path().absolute()}/Templates/template-base.png") 0 0 0 0 stretch stretch;""")

        self.Worker1 = Worker1()
        self.Worker1.plateDataUpdate.connect(self.on_plate_data_update)
        self.Worker1.mainViewUpdate.connect(self.on_main_view_update)

        self.Worker2 = Worker2()
        self.Worker2.mainTableUpdate.connect(self.refresh_table)
        self.Worker2.start()

        configure_main_table_widget(self)
        self.scene = QGraphicsScene()
        self.gv.setScene(self.scene)

        torch.cuda.empty_cache()
        gc.collect()

    def refresh_table(self, plateNum=''):
        # print("\n=== INICIO DE REFRESH_TABLE ===")
        # print(f"Parámetro plateNum recibido: {plateNum}")

        # Get all entries from the database
        plateNum = dbGetAllEntries(limit=10, whereLike=plateNum)
        # print(f"Número de registros obtenidos de la base de datos: {len(plateNum)}")

        # Set the number of rows
        self.tableWidget.setRowCount(len(plateNum))
        # print(f"Tabla configurada con {len(plateNum)} filas")

        # Iterate through entries
        for index, entry in enumerate(plateNum):
            # print(f"\n--- Procesando entrada {index + 1} ---")
            
            # Get plate number in English
            original_plate = entry.getPlateNumber(display=True)
            # print(f"Número de placa original: {original_plate}")
            
            plateNum2 = join_elements(
                convert_to_standard_format(split_string_language_specific(original_plate)))
            # print(f"Número de placa convertido: {plateNum2}")
            
            # Get status
            statusNum = db_get_plate_status(plateNum2)
            # print(f"Estado de la placa: {statusNum}")

            # Set table items
            # print("\nActualizando campos de la tabla:")
            # print(f"Estado: {entry.getStatus(statusNum=statusNum)}")
            # print(f"Placa: {entry.getPlateNumber(display=True)}")
            # print(f"Hora: {entry.getTime()}")
            # print(f"Fecha: {entry.getDate()}")
            
            self.tableWidget.setItem(index, 0, QTableWidgetItem(entry.getStatus(statusNum=statusNum)))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(entry.getPlateNumber(display=True)))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(entry.getTime()))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(entry.getDate()))

            # Load plate picture
            # print("\nCargando imagen de la placa...")
            plate_pic_path = entry.getPlatePic()
            # print(f"Ruta de la imagen: {plate_pic_path}")
            
            Image = QImage()
            image_loaded = Image.load(entry.getPlatePic())
            # print(f"Estado de carga de imagen: {'Exitoso' if image_loaded else 'Fallido'}")
            
            QcroppedPlate = QPixmap.fromImage(Image)
            # print(f"Dimensiones de la imagen: {QcroppedPlate.width()}x{QcroppedPlate.height()}")

            # Create and set image label
            item = create_image_label(QcroppedPlate)
            item.mousePressEvent = functools.partial(on_label_double_click, source_object=item)
            self.tableWidget.setCellWidget(index, 4, item)
            self.tableWidget.setRowHeight(index, 44)

            # Create buttons
            # print("\nCreando botones...")
            infoBtnItem = create_styled_button('info')
            infoBtnItem.mousePressEvent = functools.partial(self.on_info_button_clicked, source_object=infoBtnItem)
            self.tableWidget.setCellWidget(index, 5, infoBtnItem)

            addBtnItem = create_styled_button('add')
            addBtnItem.mousePressEvent = functools.partial(self.on_add_button_clicked, source_object=addBtnItem)
            self.tableWidget.setCellWidget(index, 6, addBtnItem)
            addBtnItem.setEnabled(False)

            # Handle button states
            if statusNum == 2:
                # print("Estado 2 detectado: Habilitando botón de agregar y deshabilitando botón de info")
                addBtnItem.setEnabled(True)
                infoBtnItem.setEnabled(False)

        # print("\n=== FIN DE REFRESH_TABLE ===")



    def on_info_button_clicked(self, event, source_object=None):
        r = self.tableWidget.currentRow()
        field1 = self.tableWidget.item(r, 1)
        residentView(residnetPlate=field1.text()).exec()

    def on_add_button_clicked(self, event, source_object=None):
        r = self.tableWidget.currentRow()
        field1 = self.tableWidget.item(r, 1)
        #print(f"Placa seleccionada: {field1.text()}")
        residentAddWindow = residentsAddNewWindow(self, isNew=True,
                                                  residnetPlate=field1.text())
        residentAddWindow.exec()
        self.refresh_table()

    def closeEvent(self, event):
        """### IT OVERRIDES closeEvent from PySide6"""
        if self.residentsWindow is not None and self.enterieswindow is not None:
            self.residentsWindow.close()
            self.enterieswindow.close()  # TODO if not openned any window will crash
        event.accept()

    def show_residents_list(self):
        residentsMain = residentsWindow()
        center_widget(residentsMain)
        residentsMain.exec()
        self.Worker2.start()

    def show_entries_list(self):
        enterieswindow = EnteriesWindow()
        center_widget(enterieswindow)
        enterieswindow.exec()

    def on_main_view_update(self, mainViewImage):

        qp = QPixmap.fromImage(mainViewImage)

        self.scene.addPixmap(qp)
        self.scene.setSceneRect(0, 0, 960, 540)
        self.gv.fitInView(self.scene.sceneRect())
        self.gv.setRenderHints(QPainter.Antialiasing)

    def on_plate_data_update(self, cropped_plate: QImage, plate_text: str, char_conf_avg: float,
                             plate_conf_avg: float) -> None:

        # Check if the plate text is 8 characters long and the character confidence is above 70
        if len(plate_text) == 8 and char_conf_avg >= 70:
            # Set the plate view to display the cropped plate
            self.plate_view.setScaledContents(True)
            self.plate_view.setPixmap(QPixmap.fromImage(cropped_plate))

            # Convert the plate text to Persian and set the text for the plate number and plate text in Persian
            plt_text_num = convert_to_local_format(plate_text[:6], display=True)
            plt_text_ir = convert_to_local_format(plate_text[6:], display=True)
            self.plate_text_num.setText(plt_text_num)
            self.plate_text_ir.setText(plt_text_ir)

            # Clean the plate text and get the status from the database
            plate_text_clean = clean_license_plate_text(plate_text)
            status = db_get_plate_status(plate_text_clean)

            # Update the plate owner and permission
            self.update_plate_owner(db_get_plate_owner_name(plate_text_clean))
            self.update_plate_permission(status)

            # Create data for send into services
            external_service_data = {
                'plate_number': plt_text_num + '-' + plt_text_ir,
                'image': cropped_plate
            }
            # Add the plate text, character confidence, plate confidence, cropped plate, and status to the database
            db_entries_time(plate_text_clean, char_conf_avg, plate_conf_avg, cropped_plate, status,
                            external_service_data=external_service_data)
            self.Worker2.start()

    def update_plate_owner(self, name):
        if name:
            self.plate_owner_name_view.setText(name)
        else:
            self.plate_owner_name_view.setText('')

    def update_plate_permission(self, status):
        r, g, b = get_status_color(status)
        statusText = get_status_text(status)

        self.plate_permission_view.setText(statusText)
        self.plate_permission_view.setStyleSheet("background-color: rgb({}, {}, {});".format(r, g, b))

    def start_webcam(self):
        if not self.Worker1.isRunning():
            self.Worker1.start()
        else:
            self.Worker1.unPause()

    def stop_webcam(self):
        self.Worker1.stop()


class Worker1(QThread):
    """
    Worker thread that handles frame grabbing and processing in the background.
    It is responsible for detecting plates and recognizing characters.
    """
    mainViewUpdate = Signal(QImage)
    plateDataUpdate = Signal(QImage, list, int, int)
    TotalFramePass = 0

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.prepare_capture()
        while self.ThreadActive:
            success, frame = self.Capture.read()
            if success:
                self.process_frame(frame)
                self.manageFrameRate()

    def prepare_capture(self):
        self.prev_frame_time = 0
        self.ThreadActive = True
        
        """
        # you can change 0 in >>>cv2.VideoCapture(0)<<< (which is webcam) to params.video
        # and it will read the config.ini >>> video = anpr_video.mp4
        # you should add your file path instead of anpr_video.mp4
        # if you want to use stream just replace your address in config.ini 
        >>> rtps = rtsp://172.17.0.1:8554/webCamStream
        """
        self.Capture = cv2.VideoCapture(params.video) # (params.rtps)  # 0 -> use for local webcam
        self.adjust_video_position()

    def adjust_video_position(self):
        if params.source == 'video':
            total = int(self.Capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.TotalFramePass = 0 if self.TotalFramePass > total else self.TotalFramePass
            self.Capture.set(1, self.TotalFramePass)

    def process_frame(self, frame):
        self.TotalFramePass += 1
        resize = self.prepareImage(frame)
        resize = cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)
        platesResult = modelPlate(resize)[0]
        resize = cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)

        xyxy = platesResult.boxes.xyxy.cpu().numpy()  # Coords [xmin, ymin, xmax, ymax]
        confidence = platesResult.boxes.conf.cpu().numpy()  # Confidence score

        platesResult_df = pd.DataFrame(xyxy, columns=['xmin', 'ymin', 'xmax', 'ymax'])
        platesResult_df['confidence'] = confidence

        plate_th = 50
        for _, plate in platesResult_df.iterrows():
            plateConf = int(plate['confidence'] * 100)
            print("Confidence in prediction: ", plateConf, "%")
            if plateConf >= plate_th:
                self.highlightPlate(resize, plate)
                croppedPlate = self.cropPlate(resize, plate)
                plateText, char_detected, charConfAvg = self.detectPlateChars(croppedPlate)
                self.emitPlateData(croppedPlate, plateText, char_detected, charConfAvg, plateConf)

        self.emitFrame(resize)

    def prepareImage(self, frame):
        resize = cv2.resize(frame, (960, 540))
        effect = ImageOps.autocontrast(imgModel.to_img_pil(resize), cutoff=1)
        return cv2.cvtColor(imgModel.to_img_opencv(effect), cv2.COLOR_BGR2RGB)

    def highlightPlate(self, resize, plate):
        cv2.rectangle(resize, (int(plate['xmin']) - 3, int(plate['ymin']) - 3),
                      (int(plate['xmax']) + 3, int(plate['ymax']) + 3),
                      color=(0, 0, 255), thickness=3)

    def cropPlate(self, resize, plate):
        return resize[int(plate['ymin']): int(plate['ymax']), int(plate['xmin']): int(plate['xmax'])]

    def emitPlateData(self, croppedPlate, plateText, char_detected, charConfAvg, plateConf):
        croppedPlate = cv2.resize(croppedPlate, (600, 132))
        croppedPlateImage = QImage(croppedPlate.data, croppedPlate.shape[1], croppedPlate.shape[0],
                                   QImage.Format_RGB888)
        self.plateDataUpdate.emit(croppedPlateImage, plateText, charConfAvg, plateConf)

    def manageFrameRate(self):
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - self.prev_frame_time)
        self.prev_frame_time = new_frame_time
        self.currentFPS = fps  # Save the current FPS for later drawing on the frame

    def emitFrame(self, resize):
        if hasattr(self, 'currentFPS'):  # Check if currentFPS has been calculated
            imgModel.draw_fps(resize, self.currentFPS)  # Draw FPS on the frame
        mainFrame = QImage(resize.data, resize.shape[1], resize.shape[0], QImage.Format_RGB888)
        self.mainViewUpdate.emit(mainFrame)

    def detectPlateChars(self, croppedPlate):
        chars, confidences, char_detected = [], [], []
        results = modelCharX(croppedPlate, save=False)[0]
        char_id_dict1 = results.names

        boxes = results.boxes.xyxy.numpy()  # Convertir a NumPy
        predictions = results.boxes.cls.numpy()  # Clases predichas
        confidence = results.boxes.conf.numpy()  # Confianza de las predicciones

        detections = [(box, pred, conf) for box, pred, conf in zip(boxes, predictions, confidence)]
        detections_sorted = sorted(detections, key=lambda x: x[0][0])
        chars_th = 0.5

        for det in detections_sorted:
            conf = det[2]
            if conf > chars_th:
                cls = det[1]
                char = char_id_dict1.get(int(cls))
                chars.append(char)
                confidences.append(conf)
                char_detected.append(list(det)) # Char position
        print("Plate detected: ", ''.join(chars))
        charConfAvg = round(statistics.mean(confidences) * 100) if confidences else 0
        return ''.join(chars), char_detected, charConfAvg

    def unPause(self):
        self.ThreadActive = True

    def stop(self):
        self.ThreadActive = False


class Worker2(QThread):
    mainTableUpdate = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.mainTableUpdate.emit()
        time.sleep(.5)

    def unPause(self):
        self.ThreadActive = True

    def stop(self):
        self.ThreadActive = False


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]



if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle('Windows')

    window = MainWindow()
    window.setWindowIcon(QIcon("./icons/65th_xs.png"))
    window.setIconSize(QSize(16, 16))
    center_widget(window)
    window.show()
    sys.exit(app.exec())
