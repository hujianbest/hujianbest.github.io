# hujianbest 的个人空间

这是一个集成“技术博客”与“摄影画廊”的个人网站系统，采用类苹果风格设计。

## 🚀 快速开始

### 1. 博客系统 (`/blog`)
博客基于 [Docsify](https://docsify.js.org/) 构建，存放在 `blog/` 目录下。

- **撰写文章**：在 `blog/articles/` 目录下创建 Markdown 文件。
- **配置导航**：修改 `blog/_sidebar.md` 增加新文章链接。

### 2. 摄影系统 (`/photography`)
摄影系统支持自动化发布，存放在 `photography/` 目录下。

- **发布作品**：将照片文件（jpg/png/webp 等）放入 `photography/photos/` 目录。
- **更新列表与重命名**：在项目根目录运行脚本（会从 EXIF 读取拍摄时间与地点，并将照片重命名为「地点_时间」格式，再生成索引）：
  ```bash
  pip install -r requirements.txt   # 首次需安装 Pillow、geopy
  python generate_photos.py
  ```
- **说明**：脚本会从照片 EXIF 中读取拍摄时间（DateTimeOriginal）和 GPS；若有 GPS 且已安装 `geopy`，会逆地理编码得到地点名称；无 EXIF 或无 GPS 时，时间用文件修改时间、地点默认为「中国」。文件名格式为 `地点_YYMMDD_HHMMSS.扩展名`（如 `北京_260223_181642.jpg`）。
- **查看效果**：访问 `/photography/` 即可看到自动生成的瀑布流画廊。

## 🛠️ 目录结构

```text
├── index.html              # 网站主入口（类苹果风格导航页）
├── blog/                   # 博客系统目录
│   ├── index.html          # 博客入口
│   ├── README.md           # 博客首页内容
│   ├── _sidebar.md         # 侧边栏配置
│   └── articles/           # 博客文章存放处
├── photography/            # 摄影系统目录
│   ├── index.html          # 画廊页面
│   ├── photos.json         # 自动生成的图片索引
│   └── photos/             # 摄影作品原图存放处
├── generate_photos.py      # 摄影作品索引与重命名脚本（EXIF 时间+地点）
└── requirements.txt       # Python 依赖（Pillow、geopy）
```

## 🎨 设计风格
- **极简主义**：遵循 Apple 设计准则。
- **毛玻璃效果**：使用 `backdrop-filter` 实现现代感 UI。
- **响应式**：完美适配移动端与桌面端。

## 📦 部署
本网站专为 GitHub Pages 设计。只需将代码推送到 GitHub 仓库即可完成发布。

```bash
git add .
git commit -m "Update content"
git push
```

**避免提交信息中文乱码**：在 Windows 下若使用 `git commit -m "中文"` 出现乱码，请将说明写入 UTF-8 编码的文本文件后使用 `git commit -F 文件路径`，或在本仓库已配置 `i18n.commitEncoding=utf-8` 的前提下在终端中设置 UTF-8（如 `chcp 65001`）后再提交。
