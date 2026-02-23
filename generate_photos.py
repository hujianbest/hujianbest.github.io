"""
摄影作品索引脚本：从 EXIF 提取拍摄时间与地点，将照片重命名为「地点_时间」，并生成 photos.json。
依赖：pip install Pillow geopy
"""
import os
import re
import json
from datetime import datetime
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS

# 配置
PHOTOS_DIR = 'photography/photos'
THUMBNAILS_DIR = 'photography/thumbnails'
OUTPUT_JSON = 'photography/photos.json'
EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
# 缩略图最大宽度
THUMB_WIDTH = 800
# 文件名非法字符（Windows/通用）
INVALID_CHARS = r'[\\/:*?"<>|\s]+'
# 无地点时使用的名称（未提取到地理位置信息时的默认值）
UNKNOWN_PLACE = "中国"
# Nominatim 限速：约 1 次/秒
GEOCODE_DELAY = 1.1


def get_exif(path):
    """读取图片 EXIF，失败返回 None。"""
    try:
        with Image.open(path) as img:
            exif = img.getexif()
            return exif if exif else None
    except Exception:
        return None


def get_datetime_from_exif(exif):
    """从 EXIF 取拍摄时间，返回 datetime 或 None。"""
    if not exif:
        return None
    # 36867 = DateTimeOriginal, 36868 = DateTimeDigitized, 306 = DateTime
    for tag in (36867, 36868, 306):
        raw = exif.get(tag)
        if not raw:
            continue
        try:
            # 格式通常为 "2026:02:23 18:16:42"
            return datetime.strptime(str(raw).strip(), "%Y:%m:%d %H:%M:%S")
        except ValueError:
            continue
    return None


def dms_to_decimal(dms, ref):
    """将 EXIF 的度分秒元组转为十进制度数。"""
    if not dms or len(dms) != 3:
        return None
    try:
        d = float(dms[0][0]) / float(dms[0][1])
        m = float(dms[1][0]) / float(dms[1][1])
        s = float(dms[2][0]) / float(dms[2][1])
        dec = d + m / 60.0 + s / 3600.0
        if ref in ('S', 'W', 's', 'w') and dec > 0:
            dec = -dec
        return dec
    except (TypeError, ZeroDivisionError, IndexError):
        return None


def get_gps_from_exif(exif):
    """从 EXIF 取 GPS 经纬度，返回 (lat, lon) 或 None。"""
    if not exif:
        return None
    gps_tag = None
    for tag_id, name in TAGS.items():
        if name == "GPSInfo":
            gps_tag = tag_id
            break
    if gps_tag is None:
        return None
    gps_ifd = exif.get_ifd(gps_tag)
    if not gps_ifd:
        return None
    # 1=GPSLatitudeRef, 2=GPSLatitude, 3=GPSLongitudeRef, 4=GPSLongitude
    lat_ref = gps_ifd.get(1, 'N')
    lat_dms = gps_ifd.get(2)
    lon_ref = gps_ifd.get(3, 'E')
    lon_dms = gps_ifd.get(4)
    lat = dms_to_decimal(lat_dms, lat_ref)
    lon = dms_to_decimal(lon_dms, lon_ref)
    if lat is not None and lon is not None:
        return (round(lat, 6), round(lon, 6))
    return None


def reverse_geocode(lat, lon, cache):
    """逆地理编码：经纬度 -> 地点名称，使用缓存与限速。"""
    key = (lat, lon)
    if key in cache:
        return cache[key]
    try:
        from geopy.geocoders import Nominatim
        from geopy.extra.rate_limiter import RateLimiter
        geolocator = Nominatim(user_agent="hujianbest-photo-script")
        rlimiter = RateLimiter(geolocator.reverse, min_delay_seconds=GEOCODE_DELAY)
        location = rlimiter(f"{lat}, {lon}")
        if location and location.raw.get('address'):
            addr = location.raw['address']
            # 优先：城市/区/县/镇，其次国家
            name = (
                addr.get('city') or addr.get('town') or addr.get('village') or
                addr.get('county') or addr.get('state') or addr.get('country') or ""
            )
            if isinstance(name, dict):
                name = name.get('name', str(name))
            name = (name or UNKNOWN_PLACE).strip()
        else:
            name = UNKNOWN_PLACE
        cache[key] = name
        return name
    except Exception:
        cache[key] = UNKNOWN_PLACE
        return UNKNOWN_PLACE


def sanitize_filename(s):
    """去掉文件名非法字符，多个连续空白/下划线合并为一个下划线。"""
    s = re.sub(INVALID_CHARS, '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return s or "photo"


def build_new_basename(path, exif, use_geocode, geocode_cache):
    """根据 EXIF 生成新文件名基础部分（无扩展名）：地点_YYMMDD_HHMMSS。"""
    dt = get_datetime_from_exif(exif)
    if dt is None:
        dt = datetime.fromtimestamp(os.path.getmtime(path))
    time_str = dt.strftime("%y%m%d_%H%M%S")
    place = UNKNOWN_PLACE
    gps = get_gps_from_exif(exif)
    if gps and use_geocode:
        place = reverse_geocode(gps[0], gps[1], geocode_cache)
    elif gps:
        place = f"{gps[0]:.4f}N_{gps[1]:.4f}E"
    place = sanitize_filename(place)
    return f"{place}_{time_str}", dt


def create_thumbnail(src_path, thumb_path):
    """生成缩略图。"""
    try:
        with Image.open(src_path) as img:
            # 自动处理 EXIF 旋转方向
            img = ImageOps.exif_transpose(img)
            # 保持比例缩小
            w, h = img.size
            if w > THUMB_WIDTH:
                ratio = THUMB_WIDTH / float(w)
                new_h = int(float(h) * ratio)
                img = img.resize((THUMB_WIDTH, new_h), Image.Resampling.LANCZOS)
            # 转换为 RGB 以支持保存为 JPEG (处理带有 Alpha 通道的图片)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(thumb_path, "JPEG", quality=85)
            return True
    except Exception as e:
        print(f"生成缩略图失败 {src_path}: {e}")
        return False


def main():
    if not os.path.exists(PHOTOS_DIR):
        print(f"错误: 目录 {PHOTOS_DIR} 不存在")
        return

    if not os.path.exists(THUMBNAILS_DIR):
        os.makedirs(THUMBNAILS_DIR)

    use_geocode = True
    try:
        from geopy.geocoders import Nominatim
    except ImportError:
        print("提示: 未安装 geopy，地点将使用坐标或「中国」。安装: pip install geopy")
        use_geocode = False

    geocode_cache = {}
    # 第一轮：收集 (原路径, 新文件名, 拍摄时间)
    renames = []
    seen_basenames = set()

    for filename in os.listdir(PHOTOS_DIR):
        if not filename.lower().endswith(EXTENSIONS):
            continue
        path = os.path.join(PHOTOS_DIR, filename)
        if not os.path.isfile(path):
            continue
        exif = get_exif(path)
        base_new, dt = build_new_basename(path, exif, use_geocode, geocode_cache)
        ext = os.path.splitext(filename)[1].lower()
        new_name = base_new + ext
        suffix = 0
        while new_name in seen_basenames:
            suffix += 1
            new_name = f"{base_new}_{suffix}{ext}"
        seen_basenames.add(new_name)
        renames.append((path, os.path.join(PHOTOS_DIR, new_name), new_name, dt))

    # 先重命名到临时名，再重命名到目标名，避免互相覆盖
    temp_list = []  # (old_path, temp_path, new_path, new_name, dt)
    for i, (old_path, new_path, new_name, dt) in enumerate(renames):
        if os.path.normpath(old_path) == os.path.normpath(new_path):
            temp_list.append((old_path, None, new_path, new_name, dt))
        else:
            temp_path = os.path.join(PHOTOS_DIR, f"__temp_{i}_{os.path.basename(old_path)}")
            temp_list.append((old_path, temp_path, new_path, new_name, dt))

    for old_p, temp_p, new_p, _, _ in temp_list:
        if temp_p is not None:
            os.rename(old_p, temp_p)
    for old_p, temp_p, new_p, _, _ in temp_list:
        if temp_p is not None:
            os.rename(temp_p, new_p)

    # 生成 photos.json 和缩略图
    photos = []
    for _, temp_p, new_path, new_name, dt in temp_list:
        thumb_name = os.path.splitext(new_name)[0] + ".jpg"
        thumb_path = os.path.join(THUMBNAILS_DIR, thumb_name)
        
        # 即使缩略图已存在也重新生成，以确保更新
        create_thumbnail(new_path, thumb_path)
        
        photos.append({
            "filename": new_name,
            "thumbnail": thumb_name,
            "title": os.path.splitext(new_name)[0],
            "date": dt.strftime("%Y-%m-%d"),
        })
    photos.sort(key=lambda x: x["date"], reverse=True)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(photos, f, ensure_ascii=False, indent=4)

    print(f"成功: 已重命名 {len(renames)} 张图片，生成缩略图并更新 {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
