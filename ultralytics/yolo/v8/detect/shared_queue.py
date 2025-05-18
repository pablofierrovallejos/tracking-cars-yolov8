from multiprocessing import Queue

# Crear una cola compartida directamente
frame_queue = Queue(maxsize=150)  # Tamaño máximo de 150 elementos
print(f"[shared_queue] ID de la cola: {id(frame_queue)}")  # Solo para depuración
