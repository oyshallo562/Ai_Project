# 클래스 이름을 Yolo 클래스 ID로 매핑하는 딕셔너리
import os
import re
import threading


class_to_id_mapping_temp ={'c_4_01_01': '재사용 유리 (소주병+맥주병) + 다중포장재',
 'c_4_01_02': '재사용 유리 (소주병+맥주병)',
 'c_5_01_01': '페트 + 이물질 + 다중포장재',
 'c_4_02_01_01': '갈색 유리 + 다중포장재',
 'c_4_02_02_01': '녹색 유리 + 다중포장재',
 'c_4_02_03_01': '백색 유리 + 다중포장재',
 'c_4_03_01': '기타유리 + 이물질',
 'c_6_01': '플라스틱 + 이물질',
 'c_5_01': '페트 + 다중포장재',
 'c_8_01_01': '스티로폼 + 이물질',
 'c_2_02_01': '종이컵 + 이물질',
 'c_1_01': '종이 + 이물질',
 'c_5_02_01': '페트 + 이물질',
 'c_7_01': '비닐 + 이물질',
 'c_3_01': '캔 + 이물질',
 'c_8_01': '흰색 스티로폼',
 'c_8_02': '컬러 스티로폼',
 'c_4_02_01_02': '갈색 유리',
 'c_4_02_02_02': '녹색 유리',
 'c_4_02_03_02': '백색 유리',
 'c_4_03': '기타 유리',
 'c_6': '플라스틱',
 'c_2_01': '종이팩',
 'c_2_02': '종이컵',
 'c_9': '건전지',
 'c_1': '종이',
 'c_3': '캔류',
 'c_5_02': '페트',
 'c_7': '비닐'
}

class_to_id_mapping = {
    'c_4_01_01': 0,  # '재사용 유리 (소주병+맥주병) + 다중포장재'
    'c_4_01_02': 1,  # '재사용 유리 (소주병+맥주병)'
    'c_5_01_01': 2,  # '페트 + 이물질 + 다중포장재'
    'c_4_02_01_01': 3,  # '갈색 유리 + 다중포장재'
    'c_4_02_02_01': 4,  # '녹색 유리 + 다중포장재'
    'c_4_02_03_01': 5,  # '백색 유리 + 다중포장재'
    'c_4_03_01': 6,  # '기타유리 + 이물질'
    'c_6_01': 7,      # '플라스틱 + 이물질'
    'c_5_01': 8,      # '페트 + 다중포장재'
    'c_8_01_01': 9,   # '스티로폼 + 이물질'
    'c_2_02_01': 10,  # '종이컵 + 이물질'
    'c_1_01': 11,     # '종이 + 이물질'
    'c_5_02_01': 12,  # '페트 + 이물질'
    'c_7_01': 13,     # '비닐 + 이물질'
    'c_3_01': 14,     # '캔 + 이물질'
    'c_8_01': 15,     # '흰색 스티로폼'
    'c_8_02': 16,     # '컬러 스티로폼'
    'c_4_02_01_02': 17, # '갈색 유리'
    'c_4_02_02_02': 18, # '녹색 유리'
    'c_4_02_03_02': 19, # '백색 유리'
    'c_4_03': 20,     # '기타 유리'
    'c_6': 21,        # '플라스틱'
    'c_2_01': 22,     # '종이팩'
    'c_2_02': 23,     # '종이컵'
    'c_9': 24,        # '건전지'
    'c_1': 25,        # '종이'
    'c_3': 26,        # '캔류'
    'c_5_02': 27,     # '페트'
    'c_7': 28         # '비닐'
}

# 수정된 class_to_id_mapping 딕셔너리
modified_class_to_id_mapping = {
    'c_4_01_01': 0,  # '재사용 유리 (소주병+맥주병) + 다중포장재'
    'c_5_01_01': 2,  # '페트 + 이물질 + 다중포장재'
    'c_4_02_01_01': 3,  # '갈색 유리 + 다중포장재'
    'c_4_02_02_01': 4,  # '녹색 유리 + 다중포장재'
    'c_4_02_03_01': 5,  # '백색 유리 + 다중포장재'
    'c_4_03_01': 6,  # '기타유리 + 이물질'
    'c_6_01': 7,      # '플라스틱 + 이물질'
    'c_5_01': 8,      # '페트 + 다중포장재'
    'c_8_01_01': 9,   # '스티로폼 + 이물질'
    'c_2_02_01': 10,  # '종이컵 + 이물질'
    'c_1_01': 11,     # '종이 + 이물질'
    'c_5_02_01': 12,  # '페트 + 이물질'
    'c_7_01': 13,     # '비닐 + 이물질'
    'c_3_01': 14,     # '캔 + 이물질'
    'c_4_01_02': 1,  # '재사용 유리 (소주병+맥주병)'
    'c_8_01': 15,     # '흰색 스티로폼'
    'c_8_02': 16,     # '컬러 스티로폼'
    'c_4_02_01_02': 17, # '갈색 유리'
    'c_4_02_02_02': 18, # '녹색 유리'
    'c_4_02_03_02': 19, # '백색 유리'
    'c_4_03': 20,     # '기타 유리'
    'c_6': 21,        # '플라스틱'
    'c_2_01': 22,     # '종이팩'
    'c_2_02': 23,     # '종이컵'
    'c_9': 24,        # '건전지'
    'c_1': 25,        # '종이'
    'c_3': 26,        # '캔류'
    'c_5_02': 27,     # '페트'
    'c_7': 28         # '비닐'
}


# 주어진 클래스 매핑을 반대로 매핑하는 딕셔너리 생성
id_to_class_mapping = {v: k for k, v in class_to_id_mapping.items()}

# 특정 디렉토리 내의 모든 .txt 파일을 순회하며 매핑 변경
# 파일 처리를 수행하는 함수
def process_file(file_path, mapping):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 파일 내용에서 Yolo 클래스 ID를 원래 클래스 이름으로 변경
    for id, class_name in mapping.items():
        #content = content.replace(id, class_name)
        content = content.replace(str(id), str(class_name))

    # 변경된 내용을 같은 파일에 다시 씀
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# 멀티스레딩을 사용하여 매핑 변경
def revert_class_mapping_multithreaded(directory, mapping):
    threads = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            # 각 파일 처리를 위한 스레드 생성
            thread = threading.Thread(target=process_file, args=(file_path, mapping))
            threads.append(thread)
            thread.start()

    # 모든 스레드가 종료될 때까지 기다림
    for thread in threads:
        thread.join()
# 정렬된 매핑 딕셔너리 생성 (길이에 따라 내림차순)
sorted_mapping = dict(sorted(id_to_class_mapping.items(), key=lambda item: len(item[1]), reverse=True))

# 파일 처리를 수행하는 함수 (정렬된 매핑과 정규 표현식 사용)
def process_file_with_sorted_regex(file_path, mapping):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 파일 내용에서 Yolo 클래스 ID를 원래 클래스 이름으로 변경 (정렬된 매핑과 정규 표현식 사용)
    for id, class_name in mapping.items():
        pattern = r'\b' + re.escape(id) + r'\b'
        content = re.sub(pattern, class_name, content)

    # 변경된 내용을 같은 파일에 다시 씀
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# 멀티스레딩을 사용하여 매핑 변경 (정렬된 매핑과 정규 표현식 사용)
def revert_class_mapping_multithreaded_with_sorted_regex(directory, mapping):
    threads = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            # 각 파일 처리를 위한 스레드 생성
            thread = threading.Thread(target=process_file_with_sorted_regex, args=(file_path, mapping))
            threads.append(thread)
            thread.start()

    # 모든 스레드가 종료될 때까지 기다림
    for thread in threads:
        thread.join()

#revert_class_mapping('A:/dataset_yolo/images/test')
# 사용 예시: revert_class_mapping_multithreaded('/path/to/your/directory', id_to_class_mapping)
#revert_class_mapping_multithreaded_with_sorted_regex('A:/dataset_yolo/images/train/labels', id_to_class_mapping)
revert_class_mapping_multithreaded('A:/dataset_yolo/images/train/labels', modified_class_to_id_mapping)

# 주의: 이 코드는 로컬 환경에서 실행해야 합니다. 실행하기 전에 대상 디렉토리 경로를 올바르게 설정해야 합니다.


