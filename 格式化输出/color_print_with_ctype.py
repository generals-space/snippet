# -*- coding: utf-8 -*-
# 这个用于在终端上打印带有颜色的提示信息 方便显示
 
 
 
'''
        此类支持Windows控制台打印字体
        字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色
        由于该函数的限制，应该是只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合，组合后还是在这16种颜色中
        暂时只有字体色，后续根据需求可添加背景色+字体色组合
'''
import sys
import ctypes

'''
## 这个Windows在linux执行会报错, 没有实例化时也会. 需要加上对操作系统的判断
class WindowsCMDColorPrint(object):

    #设置输出类别标志
    __stdInputHandle = -10
    __stdOutputHandle = -11
    __stdErrorHandle = -12
    # Windows CMD命令行字体颜色定义
    __foreGroundBLACK = 0x00  # black.
    __foreGroundDARKBLUE = 0x01  # darkBlue.
    __foreGroundDARKGREEN = 0x02  # darkGreen.
    __foreGroundDARKSKYBLUE = 0x03  # darkSkyBlue.
    __foreGroundDARKRED = 0x04  # darkRed.
    __foreGroundDARKPINK = 0x05  # darkPink.
    __foreGroundDARKYELLOW = 0x06  # darkYellow.
    __foreGroundDARKWHITE = 0x07  # darkWhite.
    __foreGroundDARKGRAY = 0x08  # darkGray.
    __foreGroundBLUE = 0x09  # blue.
    __foreGroundGREEN = 0x0a  # green.
    __foreGroundSKYBLUE = 0x0b  # skyBlue.
    __foreGroundRED = 0x0c  # red.
    __foreGroundPINK = 0x0d  # pink.
    __foreGroundYELLOW = 0x0e  # yellow.
    __foreGroundWHITE = 0x0f  # white.
    # Windows CMD命令行 背景颜色定义 
    __backGroundDARKBLUE = 0x10  # darkBlue.
    __backGroundDARKGREEN = 0x20  # darkGreen.
    __backGroundDARKSKYBLUE = 0x30  # darkSkyBlue.
    __backGroundDARKRED = 0x40  # darkRed.
    __backGroundDARKPINK = 0x50  # darkPink.
    __backGroundDARKYELLOW = 0x60  # darkYellow.
    __backGroundDARKWHITE = 0x70  # darkWhite.
    __backGroundDARKGRAY = 0x80  # darkGray.
    __backGroundBLUE = 0x90  # blue.
    __backGroundGREEN = 0xa0  # green.
    __backGroundSKYBLUE = 0xb0  # skyBlue.
    __backGroundRED = 0xc0  # red.
    __backGroundPINK = 0xd0  # pink.
    __backGroundYELLOW = 0xe0  # yellow.
    __backGroundWHITE = 0xf0  # white.
 
 
    stdOutHandle=ctypes.windll.kernel32.GetStdHandle(__stdOutputHandle)
 
    def setCmdColor(self,color,handle=stdOutHandle):
        return ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
 
    def resetCmdColor(self):
        self.setCmdColor(self.__foreGroundRED | self.__foreGroundGREEN | self.__foreGroundBLUE)
 
    #暗蓝色
    #dark blue
    def printDarkBlue(self,msg):
        self.setCmdColor(self.__foreGroundDARKBLUE)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #暗绿色
    #dark green
    def printDarkGreen(self,msg):
        self.setCmdColor(self.__foreGroundDARKGREEN)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #暗天蓝色
    #dark sky blue
    def printDarkSkyBlue(self,msg):
        self.setCmdColor(self.__foreGroundDARKSKYBLUE)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #暗红色
    #dark red
    def printDarkRed(self,msg):
        self.setCmdColor(self.__foreGroundDARKRED)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #暗粉红色
    #dark pink
    def printDarkPink(self,msg):
        self.setCmdColor(self.__foreGroundDARKPINK)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #暗黄色
    #dark yellow
    def printDarkYellow(self,msg):
        self.setCmdColor(self.__foreGroundDARKYELLOW)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #暗白色
    #dark white
    def printDarkWhite(self,msg):
        self.setCmdColor(self.__foreGroundDARKWHITE)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #暗灰色
    #dark gray
    def printDarkGray(self,msg):
        self.setCmdColor(self.__foreGroundDARKGRAY)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #蓝色
    #blue
    def printBlue(self,msg):
        self.setCmdColor(self.__foreGroundBLUE)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #绿色
    #green
    def printGreen(self,msg):
        self.setCmdColor(self.__foreGroundGREEN)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #天蓝色
    #sky blue
    def printSkyBlue(self,msg):
        self.setCmdColor(self.__foreGroundSKYBLUE)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #红色
    #red
    def printRed(self,msg):
        self.setCmdColor(self.__foreGroundRED)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #粉红色
    #pink
    def printPink(self,msg):
        self.setCmdColor(self.__foreGroundPINK)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #黄色
    #yellow
    def printYellow(self,msg):
        self.setCmdColor(self.__foreGroundYELLOW)
        sys.stdout.write(msg)
        self.resetCmdColor()
 
    #白色
    #white
    def printWhite(self,msg):
        self.setCmdColor(self.__foreGroundWHITE)
        sys.stdout.write(msg)
        self.resetCmdColor()
 


'''
# linux的console颜色打印
#   格式：\033[显示方式;前景色;背景色m
#   说明:
#
#   前景色            背景色            颜色
#   ---------------------------------------
#     30                40              黑色
#     31                41              红色
#     32                42              绿色
#     33                43              黃色
#     34                44              蓝色
#     35                45              紫红色
#     36                46              青蓝色
#     37                47              白色
#
#   显示方式           意义
#   -------------------------
#      0           终端默认设置
#      1             高亮显示
#      4            使用下划线
#      5              闪烁
#      7             反白显示
#      8              不可见
#
#   例子：
#   \033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
#   \033[0m          <!--采用终端默认设置，即取消颜色设置-->]]]
 
class LinuxCMDColorPrint():
    STYLE = {
        'fore':{  
            # 前景色
            'black': 30,  # 黑色
            'red': 31,  #  红色
            'green': 32,  #  绿色
            'yellow': 33,  #  黄色
            'blue': 34,  #  蓝色
            'purple': 35,  #  紫红色
            'cyan': 36,  #  青蓝色
            'white': 37,  #  白色
        },
        'back':{  
            # 背景
            'black': 40,  # 黑色
            'red': 41,  #  红色
            'green': 42,  #  绿色
            'yellow': 43,  #  黄色
            'blue': 44,  #  蓝色
            'purple': 45,  #  紫红色
            'cyan': 46,  #  青蓝色
            'white': 47,  #  白色
        },
        'mode':{  
            # 显示模式
            'mormal': 0,  # 终端默认设置
            'bold': 1,  #  高亮显示
            'underline': 4,  #  使用下划线
            'blink': 5,  #  闪烁
            'invert': 7,  #  反白显示
            'hide': 8,  #  不可见
        },
 
        'default':{
            'end': 0,
        },
    }
    def UseStyle(self, msg, mode = '', fore = '', back = ''):
        mode  = '%s' % self.STYLE['mode'][mode] if self.STYLE['mode'].has_key(mode) else ''
        fore  = '%s' % self.STYLE['fore'][fore] if self.STYLE['fore'].has_key(fore) else ''
        back  = '%s' % self.STYLE['back'][back] if self.STYLE['back'].has_key(back) else ''
        style = ';'.join([s for s in [mode, fore, back] if s])
        style = '\033[%sm' % style if style else ''
        end   = '\033[%sm' % self.STYLE['default']['end'] if style else ''
        print '%s%s%s' % (style, msg, end)

if __name__ == '__main__':
    colorPrint = LinuxCMDColorPrint()
    msg = '我是小红'
    colorPrint.UseStyle(msg, fore = 'red')    
    msg = '我是小蓝'
    colorPrint.UseStyle(msg, fore = 'blue')