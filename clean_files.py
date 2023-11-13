import os
import glob
import threading

def delete_file_if_no_counterpart(file, extension_to_check, replacement_extension):
    # 대응하는 파일의 경로 생성
    counterpart_file = file.replace(replacement_extension, extension_to_check)

    # 대응하는 파일이 존재하지 않는 경우 원래 파일 삭제
    if not os.path.exists(counterpart_file):
        os.remove(file)
        print(f"Deleted: {file}")  # 삭제된 파일 이름 출력

# 디렉토리 경로 설정
directory_path = 'A:/dataset_yolo/images/train'  # 여기에 원하는 디렉토리 경로를 입력하세요.

# 디렉토리 내의 모든 JPG와 TXT 파일 검색
jpg_files = glob.glob(os.path.join(directory_path, '*.jpg'))
txt_files = glob.glob(os.path.join(directory_path, '*.txt'))

# 각 파일에 대해 별도의 스레드에서 함수 실행
threads = []
for jpg_file in jpg_files:
    thread = threading.Thread(target=delete_file_if_no_counterpart, args=(jpg_file, '.txt', '.jpg'))
    thread.start()
    threads.append(thread)

for txt_file in txt_files:
    thread = threading.Thread(target=delete_file_if_no_counterpart, args=(txt_file, '.jpg', '.txt'))
    thread.start()
    threads.append(thread)

# 모든 스레드의 완료를 기다림
for thread in threads:
    thread.join()

