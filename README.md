# simple_git_download
One python script for download resource that on git in a easy and simple way.

## HOW TO USE ##


#### USAGE: ####

**first** download scriptfile , 
**then** run "python simple_git_download.py src_url target_path type".

#### EXAMPLE: ####

> wget -P . https://raw.githubusercontent.com/nemon-/simple_git_download/master/simple_git_download.py

> python simple_git_download.py https://github.com/nemon-/simple_git_download.git . down

or

> python simple_git_download.py https://github.com/nemon-/simple_git_download.git . wget

## 使用说明 ##


#### 用法： ####

**首先**下载py脚本，
**然后**运行"python simple_git_download.py 源地址链接 目标路径 处理类型".
其中目标路径必须存在，处理类型可以为wget（默认）或down。
当处理类型为wget或省略时，会在目标路径下生成download.sh文件；
当处理类型为down时，会将原地址的文件都下载到在目标路径下。

#### 示例： ####

> wget -P . https://raw.githubusercontent.com/nemon-/simple_git_download/master/simple_git_download.py

> python simple_git_download.py https://github.com/nemon-/simple_git_download.git . down

或者

> python simple_git_download.py https://github.com/nemon-/simple_git_download.git . wget
