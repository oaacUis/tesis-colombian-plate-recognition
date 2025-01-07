from datetime import datetime, timedelta
import random
import os
from PIL import Image


class MockEntry:
    def __init__(self, plate_number, entry_time, entry_date, plate_pic, status):
        self._plate_number = plate_number
        self._time = entry_time
        self._date = entry_date
        self._plate_pic = plate_pic
        self._status = status

    def getPlateNumber(self, display=False):
        return self._plate_number

    def getTime(self):
        return self._time

    def getDate(self):
        return self._date

    def getPlatePic(self):
        return self._plate_pic

    def getStatus(self, statusNum=None):
        if statusNum is not None:
            return {
                0: "Permitido",
                1: "No Registrado",
                2: "Pendiente",
                3: "Bloqueado"
            }.get(statusNum, "Desconocido")
        return self._status

def dbGetAllEntries(limit=10, orderBy='eDate', orderType='DESC', whereLike=''):
    # Lista de placas de ejemplo
    sample_plates = [
        "ABC123",
        "XYZ789",
        "DEF456",
        "GHI789",
        "JKL012",
        "MNO345",
        "PQR678",
        "STU901",
        "VWX234",
        "YZA567"
    ]

    # Directorio para imágenes de prueba
    #test_image_path = "D:/Brayam/Proyectos/tesis/tesis-colombian-plate-recognition/pruebas_funciones/test_images/Imagen de WhatsApp 2024-12-11 a las 10.00.33_97452c0f.jpg"
    test_image_path = r"./test_images/prueba1.jpg"
    
    
    
    # Crear directorio si no existe
    os.makedirs("test_images", exist_ok=True)
    
    # Crear una imagen de prueba si no existe
    if not os.path.exists(test_image_path):
        # Crear una imagen en blanco de 100x50 píxeles
        
        img = Image.new('RGB', (100, 50), color = 'gray')
        img.save(test_image_path)

    # Lista para almacenar las entradas
    entries = []
    
    
    # Fecha y hora base (actual)
    base_date = datetime.now()

    # Filtrar placas si hay whereLike
    filtered_plates = [p for p in sample_plates if whereLike.upper() in p.upper()] if whereLike else sample_plates

    # Generar entradas
    for i in range(min(limit, len(filtered_plates))):
        # Generar fecha y hora aleatorias dentro de las últimas 24 horas
        time_offset = timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        entry_datetime = base_date - time_offset
        
        entry = MockEntry(
            plate_number=filtered_plates[i],
            entry_time=entry_datetime.strftime("%H:%M:%S"),
            entry_date=entry_datetime.strftime("%Y-%m-%d"),
            plate_pic=test_image_path,
            status=random.randint(0, 3)
        )
        entries.append(entry)

    # Ordenar entradas según orderBy y orderType
    if orderBy == 'eDate':
        entries.sort(
            key=lambda x: (x.getDate(), x.getTime()),
            reverse=(orderType == 'DESC')
        )

    return entries

# Función auxiliar para probar el funcionamiento
def test_mock_entries():
    print("Probando dbGetAllEntries mock:")
    entries = dbGetAllEntries(limit=5, whereLike='')
    print(f"Entradas generadas: {len(entries)}")
    
    for entry in entries:
        print(f"""
        Placa: {entry.getPlateNumber(display=True)}
        Fecha: {entry.getDate()}
        Hora: {entry.getTime()}
        Estado: {entry.getStatus()}
        Imagen: {entry.getPlatePic()}
        """)

# Ejecutar prueba si se corre directamente
if __name__ == "__main__":
    test_mock_entries()