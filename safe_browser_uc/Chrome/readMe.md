## 自动加载插件配置文件工作流程
* folder_control.py 会建立系统临时文件夹, 然后把 UserData 里的配置文件拷贝到该临时文件夹
* __init__.py 里的 ptions.add_argument(f"--user-data-dir={path}") 参数指定了该临时文件夹的路径
* Chrome 启动时会加载临时文件夹下的配置文件

## 如何更新插件设置
* 先开启 safe_browser_uc/__init__.py 里 68 行对 path 的设置，然后执行 __init__.py
* 在打开的 Chrome 浏览器里改变插件的配置, 找到插件的路径，然后正常退出浏览器, 此时修改的配置会保存到磁盘
* chrome://extensions/ 勾选右上角 “开发者模式” 可以找到插件ID
* 然后去 "UserData - 用来设置" 目录下的 "Default" - "Local Extension Settings" 找到插件对应的配置文件夹
* 拷贝文件夹到 “UserData” - “Default” - "Local Extension Settings" 目录下
