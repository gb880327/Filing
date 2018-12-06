pyinstaller *.py

pyinstaller -F *.py   单文件打包


$(cd `dirname $0`; pwd)  #获取当前路径