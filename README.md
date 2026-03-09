# hujianbest 的技术博客

这是一个基于 GitHub Pages 的**纯技术博客网站**，采用类 Apple 官网风格设计，所有内容以 Markdown 维护，部署过程完全静态、零后端。

## 🚀 快速开始

### 1. 本地写作流程（推荐）

博客基于 [Docsify](https://docsify.js.org/) 构建，存放在 `blog/` 目录下。

- **撰写文章**：在 `blog/articles/` 目录下创建 Markdown 文件（建议带简单 Front Matter，如标题、日期、标签）。
- **配置导航**：修改 `blog/_sidebar.md` 增加新文章链接。
- **插入图片**：将图片放在 `blog/images/` 目录下，在文章中使用相对路径引用：

  ```md
  ![](../images/your-image.png)
  ```

- **发布到线上**：提交并推送到远端仓库，GitHub Pages 会自动发布。

### 2. 在线写作入口（可选）

网站提供了一个仅供作者自己使用的在线写作页面，通过 GitHub API 直接把内容写入本仓库：

- 访问路径：`/blog/admin/`
- 功能：
  - 在浏览器中编写 Markdown 正文；
  - 录入标题、日期、标签、分类等元信息，自动生成 Front Matter；
  - 选择本地图片文件，上传到 `blog/images/` 目录；
  - 一键发布到 `blog/articles/` 和 `blog/images/`。
- 使用方式：
  1. 在 GitHub 创建一个仅对本仓库有写权限的 Personal Access Token；
  2. 打开 `/blog/admin/`，在页面顶部配置仓库信息和 Token（保存在浏览器 `localStorage` 中，仅本机可见）；
  3. 编写内容并上传图片，点击「发布到 GitHub」即可完成提交。

> 注意：在线写作页面不会托管或记录你的 Token，所有请求直接从浏览器发往 GitHub API。

## 🛠️ 目录结构

```text
├── index.html              # 网站主入口（Apple 风格技术博客首页）
├── blog/                   # 博客系统目录
│   ├── index.html          # Docsify 容器页（阅读界面，已做 Apple 风格定制）
│   ├── README.md           # 博客首页内容（Docsify 默认首页）
│   ├── _sidebar.md         # 侧边栏配置（文章导航）
│   ├── admin/              # 在线写作入口
│   │   └── index.html      # 写作后台页面（GitHub API 提交 Markdown 与图片）
│   ├── articles/           # 博客文章存放处（Markdown）
│   └── images/             # 文章插图存放处
└── 架构设计.md             # 站点架构与内容生产流程说明
```

## 🎨 设计风格

- **极简主义**：遵循 Apple 设计语言，大量留白与清晰层级。
- **毛玻璃效果**：首页与写作后台使用 `backdrop-filter` 营造现代感 UI。
- **响应式**：适配移动端与桌面端浏览体验。

## 📦 部署

本网站专为 GitHub Pages 设计，只需将代码推送到 GitHub 仓库对应分支即可完成发布。

```bash
git add .
git commit -m "Update content"
git push
```

**避免提交信息中文乱码**：在 Windows 下若使用 `git commit -m "中文"` 出现乱码，请将说明写入 UTF-8 编码的文本文件后使用 `git commit -F 文件路径`，或在本仓库已配置 `i18n.commitEncoding=utf-8` 的前提下在终端中设置 UTF-8（如 `chcp 65001`）后再提交。
