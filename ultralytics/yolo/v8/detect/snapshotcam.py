import cv2

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=10)


def capture_snapshot():
    """
    Toma un snapshot del stream RTSP y lo guarda como una imagen.

    :param rtsp_url: URL del stream RTSP.
    :param output_file: Nombre del archivo de salida donde se guardará la imagen.
    """

    rtsp_url = "rtsp://admin:96552333A@192.168.2.64:554/Streaming/channels/101"
    output_file = "snapshot.jpg"

    # Abrimos el stream RTSP
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print(f"Error: No se pudo abrir el stream RTSP: {rtsp_url}")
        return

    # Leer un frame del stream
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el frame del stream RTSP.")
        cap.release()
        return

    # Guardar el frame como imagen estática
    cv2.imwrite(output_file, frame)
    print(f"Snapshot guardado como {output_file}")

    # Liberar el stream
    cap.release()


#if __name__ == "__main__":
#    # URL del stream RTSP
#    rtsp_url = "rtsp://admin:96552333A@192.168.2.64:554/Streaming/channels/101"
#
#    # Llamar a la función para capturar el snapshot
#    capture_snapshot(rtsp_url)

def schedule_snapshot_thread():
    """
    Encola la tarea de inserción en un hilo separado.
    """
    executor.submit(capture_snapshot)
    print("Snapshot programado.")