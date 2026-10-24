"""Chinese UI text — dialogs, log viewer, code map, Jupyter servers, launcher.

Everything here is a label, button, title or one-line message from a dialog
that is opened on demand. Fragments from string concatenation are left out on
purpose (their runtime text never equals the fragment).
"""

UI_TEXT = {
    # ── Log viewer / crash reports / command history ────────────────────────
    "🪵 Log Viewer": "🪵 日志查看器",
    "Open Logs Folder": "打开日志目录",
    "📁 Open Logs Folder": "📁 打开日志目录",
    "Delete Logs": "删除日志",
    "Delete ALL Logs": "删除全部日志",
    "Delete ALL logs": "删除全部日志",
    "Delete Before Date": "删除指定日期之前",
    "Before a date…": "指定日期之前…",
    "Older than 7 days": "7 天前",
    "Older than 30 days": "30 天前",
    "Level:": "级别：",
    "Filter:": "筛选：",
    "Lines": "行数",
    "Auto-refresh every 2 seconds — follow ongoing operations":
        "每 2 秒自动刷新 —— 跟踪正在进行的操作",
    "Timed out": "已超时",
    "Command History": "命令历史",
    "Clear Command History": "清空命令历史",
    "🗑️ Clear History": "🗑️ 清空历史",
    "Copy All": "全部复制",
    "Copy Selected": "复制所选",
    "Copy all": "全部复制",
    "📋 Copy All": "📋 全部复制",
    "Copy command": "复制命令",
    "Copy the install command to clipboard": "复制安装命令到剪贴板",
    "Forget the saved install output for this environment": "清除该环境保存的安装输出",
    "Type to narrow — package name, tool, environment…": "输入以筛选 —— 包名、工具、环境…",

    # ── Code map ────────────────────────────────────────────────────────────
    "🕸️ Code Map": "🕸️ 代码地图",
    "🗺️ Code Map": "🗺️ 代码地图",
    "Code Map": "代码地图",
    "Choose what to read, then press Read.": "选择要读取的内容，然后点击“读取”。",
    "🔍  Read": "🔍  读取",
    "Read:": "读取：",
    "Filter by file or definition name…": "按文件或定义名称筛选…",
    "Findings": "结果",
    "Tree": "树形",
    "Library": "库",
    "Application": "应用",
    "Links": "引用",
    "Could not open the Code Map:\n": "无法打开代码地图：\n",

    # ── Jupyter servers ─────────────────────────────────────────────────────
    "📓  Running Jupyter Servers": "📓  运行中的 Jupyter 服务",
    "Running Jupyter Servers": "运行中的 Jupyter 服务",
    "Looking for running servers…": "正在查找运行中的服务…",
    "Kernels": "内核",
    "Port": "端口",
    "PID": "PID",
    "Serving": "服务中",
    "Stop this server?": "停止该服务？",
    "Stop all servers?": "停止所有服务？",
    "⏹  Stop": "⏹  停止",
    "⏹  Stop all": "⏹  全部停止",
    "↻  Refresh": "↻  刷新",
    "Register": "注册",
    "Unregister": "注销",
    "Register all installed": "注册全部已安装项",
    "Register all — Results": "全部注册 —— 结果",
    "(detecting...)": "（检测中…）",
    "(not registered)": "（未注册）",
    "(not set)": "（未设置）",
    "Registered": "已注册",
    "Unregistered": "未注册",
    " — Registered": " — 已注册",
    " — Unregistered": " — 未注册",
    "○ Not found": "○ 未找到",
    "● Installed": "● 已安装",

    # ── Editor integration ──────────────────────────────────────────────────
    "📝 Editor Integration": "📝 编辑器集成",
    "📝 Open in Editor": "📝 在编辑器中打开",
    "Editor": "编辑器",
    "No editors": "没有可用编辑器",
    "No supported editors detected on this machine.": "此机器上未检测到受支持的编辑器。",
    "Re-detect installed editors": "重新检测已安装的编辑器",
    "Could not open an editor": "无法打开编辑器",
    "The default editor setting could not be written:\n": "无法写入默认编辑器设置：\n",
    "Set Default": "设为默认",
    "Status": "状态",
    "Name": "名称",
    "File:": "文件：",
    "Contents:\n": "内容：\n",
    "Current Path": "当前路径",

    # ── Project dialogs ─────────────────────────────────────────────────────
    "New Project": "新建项目",
    "Create Project": "创建项目",
    "What it is for": "用途",
    "Where should we install?": "要安装到哪里？",
    "Where the project folder will be created": "项目文件夹将创建在此处",
    "Initialize a git repository": "初始化 git 仓库",
    "With a command-line interface": "带命令行界面",
    "Switch to Packages tab after install": "安装后切换到“包管理”页",
    "Install into existing env:": "安装到已有环境：",
    "Remember this location for next time": "记住该位置以便下次使用",
    "Fill in a name and a location.": "请填写名称与位置。",
    "This path already exists:\n": "该路径已存在：\n",
    "That folder is not there any more.": "该文件夹已不存在。",
    "Where the project folder will be created": "项目文件夹将创建在此处",
    "Creating…": "创建中…",
    "Import packages from requirements.txt": "从 requirements.txt 导入包",
    "Install Packages": "安装包",
    "⚡ Install Packages": "⚡ 安装包",
    "⬇ Install to selected": "⬇ 安装到所选环境",
    "➕ Create a new env:": "➕ 新建环境：",
    "📥 Import": "📥 导入",
    "📦 Install as pipx app (isolated, system-wide)": "📦 作为 pipx 应用安装（隔离、全局）",
    "Type the project name to confirm:\n\n": "输入项目名以确认：\n\n",
    "Delete and recreate…": "删除并重建…",
    "Rename folder only — fast, but pip/python paths may break on Windows":
        "仅重命名文件夹 —— 快，但在 Windows 上可能破坏 pip/python 路径",
    "Clone with new name + delete old — slow but safe, all packages reinstalled":
        "以新名称克隆并删除旧环境 —— 较慢但安全，会重装所有包",
    "Renaming Environment (Full)": "正在重命名环境（完整）",

    # ── External apps / launcher cards ──────────────────────────────────────
    "📊  External Apps": "📊  外部应用",
    "Launch applications installed in the selected environment.\nIf an app is not installed, you can install it with one click.":
        "启动所选环境中已安装的应用。\n若应用未安装，可一键安装。",
    "Choose an environment to export:": "选择要导出的环境：",
    "🔍  Search presets...": "🔍  搜索预设…",
    "🔍 Search catalog...": "🔍 搜索目录…",
    "🔍 Filter installed packages...": "🔍 筛选已安装的包…",
    "🌐  Open in browser": "🌐  在浏览器中打开",
    "💡 You can copy this command and run it in any terminal.":
        "💡 你可以复制该命令，在任意终端中运行。",
    "Equivalent terminal command:": "等效终端命令：",
    "💾  Save as Markdown…": "💾  另存为 Markdown…",
    "📁  Browse…": "📁  浏览…",
    "📁 Open Folder": "📁 打开目录",
    "📂 Open Script": "📂 打开脚本",
    "📋 Copy to Clipboard": "📋 复制到剪贴板",
    "⧉ Copy": "⧉ 复制",
    "✓ Copied!": "✓ 已复制！",
    "➕ Add Category": "➕ 添加分类",
    "➕ Add Package": "➕ 添加包",
    "🌐 Website": "🌐 官网",
    "🏠 Home Directory": "🏠 主目录",
    "🔴 Live": "🔴 运行中",
    "⭐ Custom": "⭐ 自定义",
    "★ Default": "★ 默认",
    "☑ installed  |  Check→install  Uncheck→remove": "☑ 已安装  |  勾选→安装  取消勾选→移除",
    "⚠️ Not found on system — install separately": "⚠️ 系统中未找到 —— 请单独安装",
    "⚠️ Orange3 installed but import failed — see warning": "⚠️ Orange3 已安装但导入失败 —— 见警告",
    "One at a Time": "一次一个",
    "That leftover file could not be removed.": "无法删除残留文件。",
    "No interpreter found in:\n": "未找到解释器：\n",
    "VenvStudio — Internal Error": "VenvStudio —— 内部错误",
    "Venv directory error": "虚拟环境目录错误",
    "Venv directory doesn't exist and could not be created:\n": "虚拟环境目录不存在且无法创建：\n",
    "The name did not match, so nothing was deleted.": "名称不匹配，未删除任何内容。",
    "This will permanently delete:\n": "这将永久删除：\n",
    "Select one or more rows first.": "请先选择一行或多行。",
    "Already there": "已存在",
    "Standard": "标准",
    "Python venv module missing": "缺少 Python venv 模块",
    "Please select an environment to export packages from.": "请选择要导出包的环境。",
    "Remove all packages in this preset from the selected environment":
        "从所选环境中移除该预设的所有包",
    "Open terminal with this environment activated": "打开已激活该环境的终端",
    "Open the environment folder in your file manager": "在文件管理器中打开环境目录",
    "Language changed. VenvStudio needs to restart.\n\nRestart now?":
        "语言已更改。VenvStudio 需要重启。\n\n现在重启？",
    "Restart Required": "需要重启",
    "Settings": "设置",
    "OK": "确定",
    "File:": "文件：",
    "Findings": "结果",
    "📁  Browse…": "📁  浏览…",
    "Emoji Font Missing": "缺少 emoji 字体",
    "Could not save": "无法保存",
    "Could not write the file": "无法写入文件",
    "Could not open folder.": "无法打开文件夹。",
    "Failed:\n": "失败：\n",
    "Not installed:\n": "未安装：\n",
    "Library for building interactive CLI applications": "构建交互式命令行应用的库",
    "Rapid framework for terminal-based UIs": "快速构建终端界面（TUI）的框架",
    "Rich text and beautiful formatting in the terminal": "终端中的富文本与精美格式",
    "Terminal-based coding agent": "基于终端的编码智能体",
    "The fastest terminal emulator. GPU-accelerated, minimal, blazing fast.":
        "最快的终端模拟器。GPU 加速、极简、极速。",
    "Modern, feature-rich terminal with SSH/Telnet/Serial built-in. Plugin ecosystem.":
        "现代、功能丰富的终端，内置 SSH/Telnet/串口，并有插件生态。",
    "Native, fast, and modern. Zig-powered with platform-native feel.":
        "原生、快速、现代。Zig 驱动，拥有平台原生手感。",
    "JS/HTML/CSS based terminal. Highly customizable with plugins and themes.":
        "基于 JS/HTML/CSS 的终端，可用插件与主题深度定制。",
    "GPU-accelerated, Lua config, built-in multiplexer. The power user's choice.":
        "GPU 加速、Lua 配置、内置分屏。高级用户之选。",
    "Could not fetch available Python versions.\nCheck your internet connection.":
        "无法获取可用的 Python 版本。\n请检查网络连接。",
    "On Arch, venv is included in the python package.\nTry: sudo pacman -S python":
        "在 Arch 上 venv 已包含在 python 包中。\n可尝试：sudo pacman -S python",
    "Failed to create shortcut:\n": "创建快捷方式失败：\n",
    "Failed to launch install:\n": "启动安装失败：\n",
    "Failed to launch script:\n": "启动脚本失败：\n",
    "The snippet could not be saved before opening:\n": "代码片段在打开前无法保存：\n",
    "Downloading the source…": "正在下载源码…",
    "Downloading...": "下载中…",
    "⬇  Download source…": "⬇  下载源码…",
    "Create a shortcut on your Desktop to launch VenvStudio without a terminal":
        "在桌面创建快捷方式，无需终端即可启动 VenvStudio",
    "Increase font size": "增大字号",
    "Decrease font size": "减小字号",
    "You already have the latest version (": "你已是最新版本（",
    "Clear all stale": "清理全部失效项",
    "🧹  Clear all stale": "🧹  清理全部失效项",
    "🗑  Forget stale entry": "🗑  忽略失效项",
    "Already Active": "已启用",
    "📊  External Apps": "📊  外部应用",
    "This path already exists:": "该路径已存在：",
    "🖥️ Open a terminal with this env activated.\n\n💡 Equivalent command (":
        "🖥️ 打开已激活该环境的终端。\n\n💡 等效命令（",
    "🐍 python": "🐍 python",
    "🔖 Bookmark this": "🔖 收藏本主题",
    "✅ Bookmarked": "✅ 已收藏",
    "  📚 Learn": "  📚 学习",
    "  Explore Python": "  探索 Python",
    "  LGPL-3.0 License": "  LGPL-3.0 许可证",
    "  No bookmarks yet.\n  Use 'Bookmark this'\n  inside any topic.":
        "  还没有书签。\n  在任意主题内点击“收藏本主题”。",
    "  No bookmarks yet.\n  Use 🏷️ in Learn to bookmark topics.":
        "  还没有书签。\n  在“学习”页用 🏷️ 收藏主题。",
}

# Second pass: launcher app cards and the long help texts in Settings. They are
# longer than a label, but they are exactly the copy a user reads before
# clicking Install, so leaving them in English would undercut the rest.
UI_TEXT.update({
    # ── Launcher / external app cards ───────────────────────────────────────
    "Bayesian & frequentist statistics — beautiful, free, open source":
        "贝叶斯与频率统计 —— 美观、免费、开源",
    "Build ML model demos & web apps": "搭建机器学习演示与 Web 应用",
    "Build conversational LLM/chat UIs quickly": "快速搭建大模型对话界面",
    "Build data apps in minutes — launches demo app": "几分钟做出数据应用 —— 会启动演示应用",
    "C/C++ IDE — the real one, with compiler integration": "C/C++ IDE —— 正统之选，集成编译器",
    "Classic Jupyter Notebook — simple, document-centric interface":
        "经典 Jupyter Notebook —— 简洁的文档式界面",
    "Code editor — extensions, debugger, integrated terminal":
        "代码编辑器 —— 扩展、调试器、集成终端",
    "Data & model monitoring — drift, quality, performance": "数据与模型监控 —— 漂移、质量、性能",
    "Enhanced interactive Python shell": "增强的交互式 Python 解释器",
    "Explore & publish SQLite databases": "浏览与发布 SQLite 数据库",
    "Google's agent-first IDE": "Google 的智能体优先 IDE",
    "HoloViz dashboards & data apps": "HoloViz 仪表板与数据应用",
    "Large-scale scientific visualisation": "大规模科学可视化",
    "Linked-view exploration of related datasets": "关联数据集的联动视图探索",
    "ML experiment tracking & model registry": "机器学习实验跟踪与模型登记",
    "Machine learning workbench — classifiers, clustering, visualisation":
        "机器学习工作台 —— 分类、聚类、可视化",
    "Modern fast web API framework — launches demo": "现代快速 Web API 框架 —— 会启动演示",
    "Multi-user Jupyter server": "多用户 Jupyter 服务",
    "Next-generation notebook interface for interactive computing": "面向交互计算的新一代笔记本界面",
    "Offline ChatGPT alternative — runs models on your machine": "离线版 ChatGPT —— 在本机运行模型",
    "Point-and-click statistics — SPSS alternative, free & open source":
        "点选式统计 —— SPSS 的开源替代品",
    "Publish documents, reports & dashboards from Python/R notebooks":
        "由 Python/R 笔记本发布文档、报告与仪表板",
    "R statistical computing language — open R console": "R 统计计算语言 —— 打开 R 控制台",
    "RStudio IDE — full R development environment": "RStudio IDE —— 完整的 R 开发环境",
    "Reactive notebook — next-gen Jupyter alternative": "响应式笔记本 —— 下一代 Jupyter 替代品",
    "Reactive web apps in pure Python (Posit Shiny)": "纯 Python 的响应式 Web 应用（Posit Shiny）",
    "Run language models locally — desktop chat application": "本地运行语言模型 —— 桌面聊天应用",
    "Run local LLMs (Llama, Mistral, Gemma…) — starts Ollama server":
        "本地运行大模型（Llama、Mistral、Gemma…）—— 启动 Ollama 服务",
    "S3-compatible object storage server": "兼容 S3 的对象存储服务",
    "Scientific Python development environment": "科学 Python 开发环境",
    "Scientific plotting and graphing": "科学绘图与作图",
    "The classic Jupyter Notebook interface on modern Jupyter Server":
        "在现代 Jupyter Server 上运行经典 Notebook 界面",
    "Turn notebooks into standalone web apps": "把笔记本变成独立的 Web 应用",
    "Universal database manager — explore SQLite, PostgreSQL, MySQL…":
        "通用数据库管理器 —— 浏览 SQLite、PostgreSQL、MySQL…",
    "Version control — the tool VenvStudio's own commands assume":
        "版本控制 —— VenvStudio 自身命令所依赖的工具",
    "Visual data pipelines — drag-and-drop analytics": "可视化数据流水线 —— 拖拽式分析",
    "Visual programming for data mining and machine learning": "面向数据挖掘与机器学习的可视化编程",
    "Visualize training metrics — pick a log directory": "可视化训练指标 —— 选择日志目录",
    "Web-based UI with Python — buttons, charts, 3D & more": "用 Python 构建网页界面 —— 按钮、图表、3D 等",
    "Workflow orchestration — runs the Prefect server UI": "工作流编排 —— 启动 Prefect 服务界面",

    # ── Long help texts in Settings ────────────────────────────────────────
    "Add custom packages. Category column uses a dropdown from built-in + custom categories.":
        "添加自定义包。分类列的下拉框包含内置分类与自定义分类。",
    "Add, edit or remove package presets. Built-in presets are shown read-only. Custom presets appear in the Packages → Presets tab.":
        "添加、编辑或移除包预设。内置预设为只读，自定义预设会出现在“包管理 → 预设”页。",
    "Applies to apps installed into the pipx environment from now on. Existing apps keep the Python they were installed with. Deleting the pipx environment no longer resets this choice.":
        "仅对之后安装到 pipx 环境的应用生效。已安装的应用仍使用其原有 Python。删除 pipx 环境不会再重置此选项。",
    "By default, each tool stores environments in its own standard location. Enable a row to override that location — the tool will be directed to use your chosen path instead.":
        "默认情况下，每个工具把环境存放在各自的标准位置。勾选某一行即可覆盖该位置 —— 工具会改用你选择的路径。",
    "Changes take effect immediately for new environments. Existing environments are not moved — they remain in their original locations and will still appear in the list.":
        "对新建环境立即生效。已有环境不会被移动 —— 它们保留在原位置，并仍会出现在列表中。",
    "Check all packages installed in the current environment\nagainst known compatibility rules.":
        "按已知兼容性规则检查当前环境中已安装的全部包。",
    "Logs rotate automatically and never exceed this total. A busy session writes roughly 200 KB, so the default holds about six weeks. Applies after restarting VenvStudio; Tools › View Logs can delete entries at any time.":
        "日志会自动轮转，总量不会超过该值。繁忙会话约写入 200 KB，因此默认值大致相当于六周。重启 VenvStudio 后生效；随时可在“工具 › 查看日志”中删除日志。",
    "Python used when pipx installs an app (pipx install --python ...).\npipx gives every app its own environment, so this is the default for new installs.\nUseful when the newest Python is ahead of the packages you need.":
        "pipx 安装应用时使用的 Python（pipx install --python ...）。\npipx 为每个应用创建独立环境，因此这是新安装的默认解释器。\n当最新版 Python 领先于你所需的包时很有用。",
    "Shared cache speeds up repeated installs and saves disk space on downloads. pip/uv environments only — conda, poetry, pipx, hatch, pdm and pixi are not affected.":
        "共享缓存可加速重复安装并节省下载占用的磁盘。仅对 pip/uv 环境生效 —— conda、poetry、pipx、hatch、pdm 与 pixi 不受影响。",
    "Show the terminal command behind each action, in the command panel and the log.\nTurn off if you already know the commands and want a quieter log.":
        "在命令面板与日志中显示每个操作背后的终端命令。\n如果你已熟悉这些命令、希望日志更清爽，可以关闭。",
    "This will remove the micromamba binary managed by VenvStudio.\n\n⚠️ Conda environments will no longer be accessible until you\nre-install micromamba via Toolchain Manager.\n\nProceed?":
        "这将移除 VenvStudio 管理的 micromamba 二进制文件。\n\n⚠️ 在通过工具链管理器重新安装 micromamba 之前，\nConda 环境将无法访问。\n\n继续？",
    "Tick to change the pipx interpreter.\nLocked by default so scrolling cannot alter it by accident.":
        "勾选后可更改 pipx 使用的解释器。\n默认锁定，避免滚动时误改。",
    "Total size of venvstudio.log and its rotated backups.\nOlder entries are dropped automatically once the limit is reached.\nTakes effect on the next start.":
        "venvstudio.log 及其轮转备份的总大小上限。\n达到上限后会自动丢弃较旧的记录。\n下次启动时生效。",
    "Use VenvStudio from the terminal: <code>venvstudio list</code>, <code>venvstudio create ml</code>, <code>venvstudio install ml numpy</code>, <code>venvstudio delete ml</code> … (see <code>venvstudio --help</code>)":
        "在终端中使用 VenvStudio：<code>venvstudio list</code>、<code>venvstudio create ml</code>、<code>venvstudio install ml numpy</code>、<code>venvstudio delete ml</code> …（见 <code>venvstudio --help</code>）",
    "Used for conda environments only. Tried in order — if one is slow or serves broken metadata, VenvStudio moves to the next. During an install you can also press Skip Mirror to jump ahead immediately.":
        "仅用于 conda 环境。按顺序尝试 —— 若某个镜像缓慢或元数据异常，VenvStudio 会转到下一个。安装过程中也可按“跳过镜像”立即跳到下一个。",
    "When enabled, pip and uv will use a single shared download cache.\nDownloaded packages are stored here and reused across all pip/uv environments,\nsaving bandwidth and speeding up installs.\n\nOnly applies to pip and uv environments — conda/poetry/pipx are unaffected.":
        "启用后，pip 与 uv 共用同一个下载缓存。\n下载的包存放在此处，供所有 pip/uv 环境复用，\n可节省带宽并加快安装。\n\n仅对 pip 与 uv 环境生效 —— conda/poetry/pipx 不受影响。",
    "Which conda-compatible binary VenvStudio uses for creating and\nmanaging conda environments.\n\n  Auto          — bundled micromamba, then system micromamba\n  micromamba (bundled) — VenvStudio's own download\n  micromamba (system)  — system PATH only\n  mamba         — system mamba (faster solver)\n  conda         — system conda / Anaconda\n  miniforge     — miniforge / mambaforge installation\n  Custom path…  — browse to any compatible binary":
        "VenvStudio 创建与管理 conda 环境时使用的兼容二进制程序。\n\n  Auto          —— 先用内置 micromamba，再用系统 micromamba\n  micromamba（内置）—— VenvStudio 自行下载的版本\n  micromamba（系统）—— 仅用系统 PATH 中的版本\n  mamba         —— 系统 mamba（求解更快）\n  conda         —— 系统 conda / Anaconda\n  miniforge     —— miniforge / mambaforge 安装\n  Custom path…  —— 选择任意兼容的二进制文件",
    "conda-forge mirrors, tried top to bottom.\nAll mirrors serve the same packages — only the download server differs.\nPut the fastest one for your network first.":
        "conda-forge 镜像，自上而下尝试。\n所有镜像提供相同的包 —— 区别仅在下载服务器。\n把对你网络最快的放在最前面。",
    "venv is part of the Python standard library — there's\nnothing to pip install. This checks whether a newer\nstandalone Python build is available and, if so, offers\nto open the download dialog.":
        "venv 属于 Python 标准库 —— 无需 pip 安装。\n此处检查是否有更新的独立 Python 构建，\n若有则提示打开下载对话框。",
    "pipx is a single global tool, not something you name --\nit always shows up as \"pipx\" in the Environments table.\nInstall CLI apps later from the Installed/Catalog tabs.":
        "pipx 是单一全局工具，不需要命名 ——\n它在环境表中始终显示为 \"pipx\"。\n之后可在“已安装/目录”页安装命令行应用。",
    "Enter an environment name for managing pipx apps.\nYou can install CLI apps later from the Installed/Catalog tabs.":
        "输入用于管理 pipx 应用的环境名称。\n之后可在“已安装/目录”页安装命令行应用。",
    "Pixi project name — a new folder will be created with pixi.toml inside.":
        "Pixi 项目名 —— 将创建新文件夹并在其中生成 pixi.toml。",
})

