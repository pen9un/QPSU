#coding=utf-8
__all__=['KeyCode','Constants']
import sys,ctypes
try:
	if __name__.endswith('qgb.Win'):
		from .. import py
	else:
		import py
except Exception as ei:
	sys.path.append(sys.path[0][:-1-3])
	try:import py
	except:import pdb;pdb.set_trace()
	
try:from . import Constants
except:
	try:import Constants
	except Exception as ei:
		import pdb;pdb.set_trace()	
#python G:\QGB\babun\cygwin\lib\python2.7\qgb\Win/__init__.py 	
#sys.path ['G:\\QGB\\babun\\cygwin\\lib\\python2.7\\qgb\\Win',
#sys.path ['G:\\QGB\\babun\\cygwin\\lib\\python2.7\\qgb'   can import py
# 
	# py.pdb()
	# from . import Constants


globals().update([i for i in Constants.__dict__.items() if not i[0].startswith('__')])	
c=C=Constants




	# from Constants import *
#if 'qgb.U' in sys.modules:U=sys.modules['qgb.U']
#elif 'U' in sys.modules:  U=sys.modules['U']
#else:
#	from sys import path as _p
#	# 'G:/QGB/babun/cygwin/lib/python2.7/qgb'
#	_p.insert(-1,_p[0][:-3-1])#-3-1  插入变倒数第二
#	# for i,v in enumerate(_p):  #这会导致 ImportError: No module named Constants
#		# if 'qgb' in v and 'Win' in v:
#			# _p.pop(i)
#	# U.pln( _p
#	try:from qgb import U
#	except:'#Err import U'

class WinDLL(ctypes.CDLL):
	"""This class represents a dll exporting functions using the
	Windows stdcall calling convention.
	"""
	_func_flags_ = 0
	
windll = ctypes.LibraryLoader(WinDLL)
	
if py.iswin() or py.iscyg():
	DWORD,WCHAR,LPSTR=C.DWORD,C.WCHAR,C.LPSTR
	User32=user32=windll.user32
	Kernel32= kernel32=windll.kernel32
	Advapi32= advapi32=windll.advapi32
	C.advapi32=advapi32
# elif U.iscyg():#Not Win
	# try:
		# from ctypes import cdll
		# user32=cdll.LoadLibrary("user32.dll")
		# kernel32=cdll.LoadLibrary("kernel32.dll")
		# advapi32=cdll.LoadLibrary("advapi32.dll")
	# except:
		# pass
else:
	raise NotImplementedError
# U.pln( _p;U.pln( advapi32


try:
	from ctypes import wintypes
	import win32gui
except Exception as ei:pass

#######################################################################
class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', wintypes.BYTE),
        ('BatteryFlag', wintypes.BYTE),
        ('BatteryLifePercent', wintypes.BYTE),
        ('Reserved1', wintypes.BYTE),
        ('BatteryLifeTime', wintypes.DWORD),
        ('BatteryFullLifeTime', wintypes.DWORD),
    ]

SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)

GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
GetSystemPowerStatus.restype = wintypes.BOOL

systemPowerStatus = SYSTEM_POWER_STATUS()

def batteryIsOn():
    if not GetSystemPowerStatus(ctypes.pointer(systemPowerStatus)):
        raise ctypes.WinError()
    return systemPowerStatus.ACLineStatus == 0
    
def batteryPercent():
    if not GetSystemPowerStatus(ctypes.pointer(systemPowerStatus)):
        raise ctypes.WinError()
    return systemPowerStatus.BatteryLifePercent

def batteryFlag():
    if not GetSystemPowerStatus(ctypes.pointer(systemPowerStatus)):
        raise ctypes.WinError()
    return systemPowerStatus.BatteryFlag
#########################################################################

gdAddressType={1: ['MIB_IPADDR_PRIMARY', 'Primary IP address', '主IP地址'],
 4: ['MIB_IPADDR_DYNAMIC', 'Dynamic IP address', '动态IP地址'],
 8: ['MIB_IPADDR_DISCONNECTED', 'Address is on disconnected interface', '断开连接的接口对应的IP地址'],
 64: ['MIB_IPADDR_DELETED', 'Address is being deleted', '删除的IP地址'],
 128: ['MIB_IPADDR_TRANSIENT', 'Transient address', '临时IP地址']}

def getAllNetworkInterfaces():
	'''['dwIndex','dwAddr', 'dwBCastAddr',  'dwMask', 'dwReasmSize', 'wType', 'unused1']
dwAddr
Type: DWORD
The IPv4 address in network byte order.
dwIndex
Type: DWORD
The index of the interface associated with this IPv4 address.
dwMask
Type: DWORD
The subnet mask for the IPv4 address in network byte order.
dwBCastAddr
Type: DWORD
The broadcast address in network byte order. A broadcast address is typically the IPv4 address with the host portion set to either all zeros or all ones.
The proper value for this member is not returned by the GetIpAddrTable function.
dwReasmSize
Type: DWORD
The maximum re-assembly size for received datagrams.
unused1
Type: unsigned short
This member is reserved.
wType
Type: unsigned short
The address type or state. This member can be a combination of the following values.
	适配器（Interface Card  ,  Adapter）
	网络接口控制器（英语：network interface controller，NIC），又称网络接口控制器，网络适配器（network adapter），网卡（network interface card）
	http://www.cnblogs.com/leftshine/p/5698732.html'''
	py.importU()
	GetIpAddrTable = windll.iphlpapi.GetIpAddrTable
	GetIpAddrTable.argtypes = [
		ctypes.POINTER(MIB_IPADDRTABLE),
		ctypes.POINTER(ctypes.c_ulong),
		ctypes.wintypes.BOOL,
		]
	GetIpAddrTable.restype = DWORD
	table = MIB_IPADDRTABLE()
	size = ctypes.wintypes.ULONG(ctypes.sizeof(table))
	table.dwNumEntries = 0
	rk=['dwIndex','dwAddr', 'dwMask','wType', 'dwBCastAddr',   'dwReasmSize', 'unused1']
	GetIpAddrTable(ctypes.byref(table), ctypes.byref(size), 0)
	r=[]
	# for i in rk:U.pln( i)
	U.pln('Interface count:', table.dwNumEntries)
	for n in range(table.dwNumEntries):
		row = table.table[n]
		rn=[]
		for i in rk:
			if i in('dwIndex','dwReasmSize'):
				rn.append(getattr(row,i))
			elif i=='wType':
				i=getattr(row,i)
				t=[]
				for j in sorted(gdAddressType.keys(),reverse=True):
					if j<=i:
						t.append(gdAddressType[j][0])
				rn.append(t)
			else:
				rn.append(str(getattr(row,i)))
		r.append(rn)
		
	# raise IndexError("interface index out of range")
		# U.repl()
	return tuple(r)
getAllNetwork=getAllNetworkInterfaces

def getCmdHandle():
	return kernel32.GetConsoleWindow()
getcmdw=getCmdHandle
	
def getCmdLine():
	'''------> k.GetCommandLineW()
Out[9]: 'G'
	'''
	kernel32.GetCommandLineA.restype=LPSTR
	return kernel32.GetCommandLineA()
getCmd=getCmdLine
	
def getTitle(h=0,size=1024):
	'''h:window Handle'''
	if not h:h=getCmdHandle()
	title = ctypes.create_string_buffer(size)
	user32.GetWindowTextA(h,title,size)
	return title.value
getitle=getTitle
	
def setTitle(st,h=0):
	'''在python内设置的，退出后 会还原  
'''
	if type(st)!=str:st=str(st)
	if not h:h=getCmdHandle()
	return user32.SetWindowTextA(h,st)
setitle=setTitle

def EnumWindowsProc(hwnd, resultList):
	if win32gui.IsWindowVisible(hwnd) and getitle(hwnd) != '':
		resultList.append((hwnd, getitle(hwnd)))

def getAllWindows():
	mlst=[]
	win32gui.EnumWindows(EnumWindowsProc, mlst)
	# for handle in handles:
		# mlst.append(handle)
	return [(i[0],i[1].decode('mbcs')) for i in mlst]
EnumWindows=getAllWindow=getAllWindows
	
def setWindowPos(h=0,x=199,y=-21,width=999,height=786,top=None,flags=None):
	if not h:h=getCmdHandle()
	if not top:top=HWND_TOP
	if not flags:flags=SWP_SHOWWINDOW
	if top is True:top=HWND_TOPMOST
	return user32.SetWindowPos(h,top,x,y,width,height,flags)
setPos=setpos=setWPos=setWindowPos
	
def setOskPos(w=333,h=255,x=522,y=-21):
	flags=SWP_SHOWWINDOW
	if x<1 or y<-21:flags+=SWP_NOMOVE
	if w<30 or h <30:flags+=SWP_NOSIZE
	for i,k in getAllWindows():
		if k=='\xc6\xc1\xc4\xbb\xbc\xfc\xc5\xcc':
			setPos(i,width=w,height=h,x=x,y=y,flags=flags)
	
	
def msgbox(s='',st='title',*a):
	''' st title'''
	if(a):
		a=list(a)
		a.insert(0,s)
		a.insert(1,st)
		st='length %s'%len(a)
		s=str(a)
	# s=str(s)+ ','+str(a)#[1:-2]
	if py.is2():
		return user32.MessageBoxA(0, str(s), str(st), 0)		
	else:
		return user32.MessageBoxW(0, str(s), str(st), 0)		

def getCursorPos():
	from ctypes import Structure,c_ulong,byref
	class POINT(Structure):
		_fields_ = [("x", c_ulong), ("y", c_ulong)]
	pt = POINT()
	user32.GetCursorPos(byref(pt))
	return pt.x,pt.y		
getMousePos=GetCursorPos=getCurPos=getCursorPos

setMousePos=setCursorPos=SetCursorPos=setCurPos=user32.SetCursorPos
######################
def mouse_event(x,y,event=0,abs=True,move=True):
	'''
	x,y int :depand abs (Don't input base 65535)
	x,y float 0-1.0:  rel screen x
	
	abs False:从上一次鼠标位置移动
	Win.mouse_event(0,0)  没有反应？
	Return value

	This function has no return value.
	Remarks

	dwData>0 scroll up
	<0  down

If the mouse has moved, indicated by MOUSEEVENTF_MOVE being set, dx and dy hold information about that motion. The information is specified as absolute or relative integer values.
If MOUSEEVENTF_ABSOLUTE value is specified, dx and dy contain normalized absolute coordinates between 0 and 65,535. The event procedure maps these coordinates onto the display surface. Coordinate (0,0) maps onto the upper-left corner of the display surface, (65535,65535) maps onto the lower-right corner.

If the MOUSEEVENTF_ABSOLUTE value is not specified, dx and dy specify relative motions from when the last mouse event was generated (the last reported position). Positive values mean the mouse moved right (or down); negative values mean the mouse moved left (or up).	
=======================================
	MOUSEEVENTF_ABSOLUTE
0x8000
The dx and dy parameters contain normalized absolute coordinates. If not set, those parameters contain relative data: the change in position since the last reported position. This flag can be set, or not set, regardless of what kind of mouse or mouse-like device, if any, is connected to the system. For further information about relative mouse motion, see the following Remarks section.
MOUSEEVENTF_LEFTDOWN
0x0002
The left button is down.

x,y useless?  |MOUSE_MOVE
Win.mouse_event(90,90,2|1,False)#x,y 无用
Win.mouse_event(90,90,2|1,True)#有用，并立即返回

Win.mouse_event(65536,65536,0)
-------> Win.getCursorPos()
Out[76]: (1365L, 767L)

	'''
	
	
	W,H=getScreenSize()
	
	if type(x) is float :
		if abs:x=int(65535*x);y=int(65535*y)
		else:x=int(W*x);y=int(H*y)
	else:
		if abs:
			x=float(x)/W;	y=float(y)/H
			x=int(65535*x);y=int(65535*y)
	dwData=0
		
	if abs:	event=event|mouse_event.ABSOLUTE
	if move:event=event|mouse_event.MOVE  #2|1|1|1== 3
	# if WHEEL&event:
	if mouse_event.WDOWN&event:dwData=-9;event|=mouse_event.WHEEL
	if mouse_event.WUP&event:dwData=9;event|=mouse_event.WHEEL
	
	
	User32.mouse_event.argtypes=[DWORD,
                                 DWORD,
                                 DWORD,
                                 DWORD,
                                 ctypes.wintypes.c_void_p]#ULONG_PTR	
	py.importU()
	if U.debug():U.pln(event,x,y,dwData,None)
	User32.mouse_event(event,x,y,dwData,None)
mouse_event.ABSOLUTE = 0x8000
mouse_event.HWHEEL = 0x01000
mouse_event.LEFTDOWN = 0x0002
mouse_event.LEFTUP = 0x0004
mouse_event.MIDDLEDOWN = 0x0020
mouse_event.MIDDLEUP = 0x0040
mouse_event.MOVE = 0x0001
mouse_event.MOVE_NOCOALESCE = 0x2000
mouse_event.RIGHTDOWN = 0x0008
mouse_event.RIGHTUP = 0x0010
mouse_event.VIRTUALDESK = 0x4000
mouse_event.WHEEL = 0x0800
mouse_event.XDOWN = 0x0080
mouse_event.XUP = 0x0100
mouse_event.WDOWN=0x200
mouse_event.WUP=0x400
mouse_event.RC=mouse_event.RIGHTDOWN|mouse_event.RIGHTUP
mouse_event.LC=mouse_event.LEFTDOWN|mouse_event.LEFTUP
	
def getScreenSize():
	return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
	
def CreateProcess(appName,cmd,):pass
# aa= 233
def getLastError(errCode=None,p=True):
	'''  need .decode('gb18030') '''
	py.importU()
	from ctypes import c_void_p,create_string_buffer
	GetLastError = kernel32.GetLastError
	FormatMessage = kernel32.FormatMessageA
	LocalFree = kernel32.LocalFree
	
	FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
	FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000
	FORMAT_MESSAGE_IGNORE_INSERTS = 0x00000200

	try:
		msg = create_string_buffer(256)
		FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM,
						c_void_p(),
						2,
						0,
						msg,
						len(msg),
						c_void_p())
	except Exception as e:
		U.pln( e)
	# return 233
	# from win32con import (
		# FORMAT_MESSAGE_FROM_SYSTEM,
		# FORMAT_MESSAGE_ALLOCATE_BUFFER,
		# FORMAT_MESSAGE_IGNORE_INSERTS)

	if errCode is None:
		errCode = GetLastError()
	U.pln( errCode)
	message_buffer = ctypes.c_char_p()
	FormatMessage(
		FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_IGNORE_INSERTS,
		None,
		errCode,
		0,
		ctypes.byref(message_buffer),
		0,
		None
	)

	error_message = message_buffer.value
	LocalFree(message_buffer)

	r= '{} - {}'.format(errCode, error_message).decode('gb18030')#unicode
	# error_message = error_message.decode('cp1251').strip()
	if U.isipy() and not U.DEBUG:#TODO  如果修改了repr 方式  可以去除这个
		U.pln( r)
	else:
		return r
geterr=getErr=getLastErr=getLastError
##############################################
gdWinVerNum={'10':10.0,# 6.2,#使用 GetVersionExW
			 '2000': 5.0,
			 '2003': 5.2,
			 '2008': 6.0,
			 '2008R2': 6.1,
			 '2012': 6.2,
			 '2012R2': 6.3,
			 '2016': 10.0,
			 '7': 6.1,
			 '8': 6.2,
			 '8.1': 6.3,
			 'vista': 6.0,
			 'xp': 5.1}
for w,i in gdWinVerNum.items():
	py.execute('''def is{0}():return getVersionNumberCmdVer()=={1}'''.format(
		w.replace('.','_'),i)    )			 
			 
def getWinName():
	for w,i in gdWinVerNum.items():
		if i==getVersionNumber():
			return 'Windows '+w
	raise EnvironmentError('Unknown Windows VersionNumber',getVersionNumber())

name=systemName=getSysName=getWinName
def GetProcessImageFileName(pid=None):
	'''if pid ignore Process name
	Windows XP or later
	Windows Server 2003 and Windows XP:  The handle must have the PROCESS_QUERY_INFORMATION access right.'''
	if not pid:
		py.importU()
		pid=U.pid
	PROCESS_ALL_ACCESS = 0x001F0FFF
	# bInheritHandle [in]
# If this value is TRUE, processes created by this process will inherit the handle. Otherwise, the processes do not inherit this handle.
	hprocess=kernel32.OpenProcess(PROCESS_ALL_ACCESS,True,pid)
	dll=windll.psapi
	from ctypes import c_void_p,create_string_buffer
	im=256
	fn = create_string_buffer(im)
	if dll.GetProcessImageFileNameA(hprocess,fn,im)==0:
		return False
	else:
		fn= fn.value
		for d,v in getAllDisk().items():
			if fn.startswith(v):
				return fn.replace(v,d)
		return fn
getProcessPath=GetProcessImageFileName
gversionInfo=gVersionInfo=None
def getVersionInfo():
	global gVersionInfo
	if gVersionInfo:return gVersionInfo
	# from Constants import DWORD,WCHAR
	class OSVersionInfo(ctypes.Structure):
		_fields_ = (('dwOSVersionInfoSize', DWORD),
					('dwMajorVersion', DWORD),
					('dwMinorVersion', DWORD),
					('dwBuildNumber', DWORD),
					('dwPlatformId', DWORD),
					('szCSDVersion', WCHAR * 128))

		def __init__(self, *args, **kwds):
			# super(OSVersionInfo, self).__init__(*args, **kwds)
			self.dwOSVersionInfoSize = ctypes.sizeof(self)
			kernel32.GetVersionExW(ctypes.byref(self))
	gVersionInfo=OSVersionInfo()
	return gVersionInfo
def getVersionNumberCmdVer():
	'''
Microsoft Windows [版本 10.0.16299.125]
Microsoft Windows [版本 6.1.7601]
Microsoft Windows XP [版本 5.1.2600]
	'''
	py.importU()
	import subprocess as sb
	T=U.T
	r=sb.Popen('cmd.exe /c ver',stdout=sb.PIPE)
	r=r.stdout.read(-1)
	r=T.subLast(r,' ',']')
	r=r.split('.')
	if len(r)<3:raise Exception('cmd ver ',r)
	major,minor,build=r[:3]
	return float('{0}.{1}'.format(major,minor))
	
def getVersionNumber():
	'''TODO 实现有问题  在win10下为 6.2
	
	
In [3]: Win.getVersionNumber
------> Win.getVersionNumber()
Out[3]: 6.1

In [4]: Win.is7
------> Win.is7()
Out[4]: True
	
	'''	
	# return getVersionNumberCmdVer()
	v=getVersionInfo()	
	return float('{0}.{1}'.format(v.dwMajorVersion,v.dwMinorVersion))
def getpid():
	return kernel32.GetCurrentProcessId()
def getAllDisk():
	'''return {'B:': '\\Device\\HarddiskVolumeRD',...'''
	r={}
	from ctypes import create_string_buffer
	im=256
	s=create_string_buffer(im)
	for i in [chr(i) for i in range(65,65+26)]:
		i=i+':'
		if 0==kernel32.QueryDosDeviceA(i,s,im):
			pass
		else:
			r[i]=s.value
		# if U.F.exist(i):r.append(i)
	return r
def main():
	py.importU()
	py.importU()
	py.pdb()
	# U=globals()['U']#  为何在此不能自动引用 globals
	import U
	U.pln( getAllNetwork())
	exit()
	import sys,os;sys.path.append('d:\pm');from qgb import U,T,F
	
	o=getVersionInfo()
	U.pln( o.dwMajorVersion,o.dwMinorVersion)
	
	# CreateProcessWithLogonW(
	# lpUsername='qgb',
	# lpPassword='q',

	# lpApplicationName=r'C:\WINDOWS\system32\calc.exe')	
	U.pln( '[%s]'%getTitle(),getProcessPath(),U.getModPath())
	# U.msgbox()
	# U.repl()
# U.pln( 233
if __name__ == '__main__':main()