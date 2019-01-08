# TODOLIST
- 在线更新功能


>  pyinstaller *.py

>  pyinstaller -F *.py   单文件打包

>  pyinstaller --onedir -y Filing.spec

>  $(cd `dirname $0`; pwd)  #获取当前路径


>  打包后进行文件删减
```
   /Contents/MacOS/QtCore
   /Contents/MacOS/QtDBus
   /Contents/MacOS/QtGui
   /Contents/MacOS/QtMacExtras
   /Contents/MacOS/QtOpenGL
   /Contents/MacOS/QtPositioning
   /Contents/MacOS/QtPositioningQuick
   /Contents/MacOS/QtPrintSupport
   /Contents/MacOS/QtWidgets

   /Resources/PyQt5/Qt/qml/Qt
   /Resources/PyQt5/Qt/qml/QtPositioning
   /Resources/PyQt5/Qt/qml/QtSensors
```