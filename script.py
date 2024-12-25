import os
import numpy as np
from PIL import Image
from minio import Minio
from minio.error import S3Error
import time
import shutil
time.sleep(1)

# Настройки MinIO
MINIO_URL = 'minio:9000'  # Минимально необходимый адрес MinIO
MINIO_ACCESS_KEY = 'minioadmin'  # Ваш ключ доступа
MINIO_SECRET_KEY = 'minioadmin'  # Ваш секретный ключ
BUCKET_NAME = 'testbucket'  # Название bucket для загрузки изображений

# Инициализация клиента MinIO
client = Minio(MINIO_URL, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False)

# Проверка существования bucket
try:
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)
except S3Error as e:
    print("Error occurred: ", e)


# Генерация случайного изображения и загрузка в MinIO
def upload_random_image(bucket_name, image_name):
    # Генерация случайного изображения 100x100 пикселей
    random_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    image = Image.fromarray(random_image)

    # Сохранение изображения во временный файл
    temp_image_path = f"/tmp/{image_name}"
    image.save(temp_image_path)

    # Загрузка изображения в MinIO
    client.fput_object(bucket_name, image_name, temp_image_path)
    print(f"Uploaded {image_name} to bucket {bucket_name}")

    # Удаление временного файла
    os.remove(temp_image_path)

# Проверка размера bucket
def get_bucket_size(bucket_name):
    total_size = 0
    for obj in client.list_objects(bucket_name):
        total_size += obj.size
    return total_size

# Основная функция для загрузки изображений до заполнения памяти
def main():
    while True:
        image_name = f"random_image_{np.random.randint(1, 100000)}.png"
        try:
            upload_random_image(BUCKET_NAME, image_name)
        except S3Error as e:
            print("Error occurred: ", e)
            break

            

if __name__ == '__main__':
    main()