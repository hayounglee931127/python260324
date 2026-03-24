import os
import shutil
from pathlib import Path

# 원본 다운로드 폴더
downloads_dir = Path(r"C:\Users\student\Downloads")

# 목적지 폴더
target_dirs = {
    "images": [".jpg", ".jpeg"],
    "data": [".csv", ".xlsx"],
    "docs": [".txt", ".doc", ".pdf"],
    "archive": [".zip"],
}

# 폴더 없으면 생성
for folder in target_dirs.keys():
    target_path = downloads_dir / folder
    target_path.mkdir(parents=True, exist_ok=True)

# 파일 확장자에 맞게 이동
for item in downloads_dir.iterdir():
    if item.is_file():
        ext = item.suffix.lower()
        moved = False
        for folder, ext_list in target_dirs.items():
            if ext in ext_list:
                dest = downloads_dir / folder / item.name
                # 이름 충돌 시 덮어쓰기(혹은 원하시면 건너뛰기/리네임 처리 추가)
                shutil.move(str(item), str(dest))
                moved = True
                print(f"Moved: {item.name} -> {folder}\\")
                break
        if not moved:
            # 처리 대상이 아닌 경우 (필요 시 확장자 추가하거나 무시)
            pass