import os
import fnmatch
import json
import threading

def find_files(directory, file_extension):
    matches = []
    for filename in os.listdir(directory):
        if filename.endswith(f'.{file_extension}'):
            matches.append(os.path.join(directory, filename))
    return matches

def process_json_file(json_file, output_dir, class_to_id_mapping, image_directory):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    image_filename_without_extension = os.path.splitext(os.path.basename(json_file))[0]

    found_image_file = False
    temp = ''
    for ext in ['jpg', 'jpeg', 'png']:

        temp = 'TS_3.어플리케이션_C_1'

        image_path = os.path.join(image_directory, f"{image_filename_without_extension}.{ext}")


        if os.path.exists(image_path):
            #print(image_path)
            found_image_file = True
            break

    if not found_image_file:
        print(image_path)
        print(f"Image file for {json_file} not found.")
        return

    yolo_filename = os.path.join(output_dir, f"{image_filename_without_extension}.txt")

    with open(yolo_filename, 'w', encoding='utf-8') as yolo_file:
        for item in data['objects']:
            class_id = class_to_id_mapping.get(item['class_name'], -1)
            bbox = item['annotation']['coord']
            x, y, width, height = bbox['x'], bbox['y'], bbox['width'], bbox['height']
            x_center, y_center = x + width / 2, y + height / 2
            yolo_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

def convert_json_to_yolo_multithreaded(json_files, output_dir, class_to_id_mapping, image_directory, num_threads=10):
    threads = []

    for json_file in json_files:
        thread = threading.Thread(target=process_json_file, args=(json_file, output_dir, class_to_id_mapping, image_directory))
        threads.append(thread)
        thread.start()

        while threading.active_count() > num_threads:
            pass

    for thread in threads:
        thread.join()

# JSON 파일과 이미지 파일 디렉토리 지정
json_directory = r'A:\307.생활폐기물 데이터 활용ㆍ환류\01.데이터\Validation\02.라벨링데이터'
image_directory = r'A:\dataset_yolo\images\val'
# 파일 찾기
json_files = find_files(json_directory, 'json')

# 클래스 이름을 Yolo 클래스 ID로 매핑
class_to_id_mapping = {
    'c_1': '종이',
    'c_2_01': '종이팩',
    'c_2_02': '종이컵',
    'c_3': '캔류',
    'c_4_01_02': '재사용 유리 (소주병+맥주병)',
    'c_4_02_01_02': '갈색 유리',
    'c_4_02_02_02': '녹색 유리',
    'c_4_02_03_02': '백색 유리',
    'c_4_03': '기타 유리',
    'c_5_02': '페트',
    'c_6': '플라스틱',
    'c_7': '비닐',
    'c_1_01': '종이 + 이물질',
    'c_2_02_01': '종이컵 + 이물질',
    'c_3_01': '캔 + 이물질',
    'c_4_03_01': '기타유리 + 이물질',
    'c_5_01_01': '페트 + 이물질 + 다중포장재',
    'c_5_02_01': '페트 + 이물질',
    'c_6_01': '플라스틱 + 이물질',
    'c_7_01': '비닐 + 이물질',
    'c_4_01_01': '재사용 유리 (소주병+맥주병) + 다중포장재',
    'c_4_02_01_01': '갈색 유리 + 다중포장재',
    'c_4_02_02_01': '녹색 유리 + 다중포장재',
    'c_4_02_03_01': '백색 유리 + 다중포장재',
    'c_5_01': '페트 + 다중포장재',
    'c_8_01': '흰색 스티로폼',
    'c_8_02': '컬러 스티로폼',
    'c_8_01_01': '스티로폼 + 이물질',
    'c_9': '건전지'
}

# Yolo 형식으로 변환 (멀티스레딩 사용)
output_dir = r'A:\1\yolo2' # 출력 디렉토리 지정
convert_json_to_yolo_multithreaded(json_files, output_dir, class_to_id_mapping, image_directory, num_threads=12)

print(f'Processed {len(json_files)} JSON files.')
