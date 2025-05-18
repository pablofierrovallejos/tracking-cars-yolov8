import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import queue

#rtsp_url = "rtsp://admin:96552333A@192.168.2.64:554/Streaming/channels/101"

from shared_queue import frame_queue

print(f"[Servidor de video] ID de la cola al importar videoserver: {id(frame_queue)}")



class MJPEGHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/video_feed':
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()

        try:
            while True:
                print("Esperando frame en la cola...")
                print(f"[Servidor de video] ID de la cola: {id(frame_queue)}")

                # Obtener el siguiente frame desde la cola
                frame = frame_queue.get(timeout=10)
                 # Espera hasta que haya un frame disponible
                if frame is None:  # Si recibimos None, terminamos el streaming
                    print("Frame vacío recibido. Cerrando conexión.")

                    break
                print("Frame recibido, procesando...")

                # Codificar el frame como JPEG
                _, jpeg = cv2.imencode('.jpg', frame)
                cv2.imwrite("debug_frame.jpg", frame)  # Guarda un frame

                # Enviar frame a cliente
                self.wfile.write(b'--frame\r\n')
                self.wfile.write(b'Content-Type: image/jpeg\r\n\r\n')
                self.wfile.write(jpeg.tobytes())
                self.wfile.write(b'\r\n')
        except Exception as e:
            print("Stream terminado:", e)


def run_server():
    # Configura el servidor aquí
    print(f"[Servidor de video] ID de la cola: {id(frame_queue)}")

    server = HTTPServer(('0.0.0.0', 8080), MJPEGHandler)
    print("Servidor MJPEG en http://localhost:8080/video_feed")
    server.serve_forever()


if __name__ == "__main__":
    run_server()

