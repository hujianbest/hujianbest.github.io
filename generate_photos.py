import os
import json
from datetime import datetime

# 配置
PHOTOS_DIR = 'photography/photos'
OUTPUT_JSON = 'photography/photos.json'
EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.gif')

def generate_photos_json():
    if not os.path.exists(PHOTOS_DIR):
        print(f"错误: 目录 {PHOTOS_DIR} 不存在")
        return

    photos = []
    
    # 遍历目录
    for filename in os.listdir(PHOTOS_DIR):
        if filename.lower().endswith(EXTENSIONS):
            filepath = os.path.join(PHOTOS_DIR, filename)
            
            # 获取文件修改时间作为默认日期
            mtime = os.path.getmtime(filepath)
            date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
            
            # 基础信息
            photo_info = {
                "filename": filename,
                "title": os.path.splitext(filename)[0],
                "date": date_str
            }
            photos.append(photo_info)

    # 按日期降序排列
    photos.sort(key=lambda x: x['date'], reverse=True)

    # 写入 JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(photos, f, ensure_ascii=False, indent=4)
    
    print(f"成功: 已生成 {len(photos)} 张图片的索引文件 {OUTPUT_JSON}")

if __name__ == "__main__":
    generate_photos_json()
