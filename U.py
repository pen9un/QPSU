# coding=utf-8
gsImport='''
from qgb import U,T
'''
true=True;false=False
gimax=IMAX=imax=2147483647;gimin=IMIN=imin=-2147483648
import sys
stdin=sys.stdin;stdout=sys.stdout;stderr=sys.stderr
gsdecode=decoding='utf-8';gsencode=encoding=stdout.encoding
modules=sys.modules
try:
	import py
	if not py.istr:raise Exception('not qgb.py')
except Exception as eipy:
	try:from . import py
	except Exception as ei:import pdb;pdb.set_trace()
	
'''TODO：应该设计一个配置类，__getattr__ on a module 属性拦截,这样可以同步多个变量名， 在python2中没有很好的方法,  在Python 3.7+中，你只需要做一个明显的方法。
# my_module.py
def __getattr__(name: str) -> Any:
	return attr
目前使用单变量名	
'''
gbPrintErr=True
gbLogErr=True

gbDebug=DEBUG=sys.flags.debug or False#gbDebug只在这里出现一次
def debug(a=False):
	if 'debug' in os.environ:
		e=os.getenv('debug').strip()#not .trim()
		if e and e!='0':a=True
		else:a=False
	globals()['DEBUG']=a;return DEBUG

# if(calltimes()<1):DEBUG=True #ct not defined

########
gError=[]
def setErr(ae,msg='#Error '):
	global gError
	if gbLogErr:# U.
		if type(gError) is list:gError.append(ae)
		elif gError:gError=[gError,ae]
		else:gError=[ae]
	else:
		gError=ae
	if gbPrintErr:print (msg,ae)# U.
	
if 'qgb.U' in modules:modules['_U']=modules['qgb.U']
elif 'U' in modules:modules['_U']=modules['U']
################  import python lib  #######################
try:
	import os;path=os.path
	from threading import Thread
	thread=Thread
	from multiprocessing import Process;process=Process
	from collections import OrderedDict
except Exception as ei:
	setErr(ei,msg='#Error py lib import')
	
try:
	_U=modules['_U']
	gError=_U.gError
	gbPrintErr=_U.gbPrintErr
except Exception as _e:pass
	# pass# 已经存在于globals 中，是否有必要重新赋值给 gError？
# else:
try:
	if __name__.endswith('qgb.U'):from . import F,T
	else:import F,T
	# if isMain():import F,T
	# else:from . import F,T
	write,read,ls,ll,md,rm=F.write,F.read,F.ls,F.ll,F.md,F.rm
	from pprint import pprint
	if __name__.endswith('qgb.U'):from . import Clipboard
	else:import Clipboard

	clipboard=cb=Clipboard#  
except Exception as ei:
	setErr(ei,msg='#Error import '+str(ei))
	
aError=ArgsErr=argserr=argErr=argerr=argumentError=ArgumentException=py.ArgumentError	
ArgumentUnsupported=py.ArgumentUnsupported
############
module=py.module
Class=py.Class
instance=py.instance
Class=classtype=classType=py.classType
iterable=py.iterable
#########################
def one_in(vs,*t):
	'''(1,2,3,[t])	or	([vs].[t])'''
	if not hasattr(vs, '__iter__'):vs=[vs]#  is3 str has __iter__  while  is2 not
	if len(t)==1:
		t=t[0]
	elif len(t)>1:
		vs.extend(t[:-1])
		t=t[-1]
	else:raise Exception(one_in.__doc__)
	r=[]
	for i in vs:
		try:
			if i in t:r.append(i)
		except:pass
	return r
#########################
def getPyVersion():
	'''return float 2.713
	'''
	r=T.sub(sys.version,'',' ')
	r=r.replace('.','')
	r=r[0]+'.'+r[1:]
	return float(r)
	

import platform
def iswin():
	if platform.system().startswith('Windows'):return True
	else:return False
glnix=['nix','linux','darwin']
def isnix():
	return [i for i in glnix if i in platform.system().lower()]
	# return one_in('nix','linux','darwin',platform.system().lower())
def istermux():
	return 'com.termux' in os.getenv('PATH')
	
def iscyg():
	return 'cygwin' in  platform.system().lower()
# gipy=None#这个不是qgb.ipy, 是否与U.F U.T 这样的风格冲突？
def isipy():
	# global gipy
	try:
		if not py.modules('IPython'):return None
		import IPython
		return IPython.get_ipython()
	except:return False
	# ipy=False  #如果曾经有过实例，现在没有直接返回原来
	# f=sys._getframe()
	# while f and f.f_globals:# and 'get_ipython' not in f.f_globals.keys()
		# try:
			# ipy=f.f_globals['get_ipython']()#下个循环没有直接跳出while
			# break
		# except:
			# pass
		# f=f.f_back	
	# return ipy
getipy=isipy
def isrepl():
	i,o=sys.stdin.isatty(),sys.stdout.isatty()
	if i==o:return i
	else:
		raise Exception('std(in,out) isatty conflit')
isatty=istty=isrepl
########################
if iswin() or iscyg():
	try:
		if __name__.endswith('qgb.U'):from . import Win
		else:import Win
		setWindowPos,msgbox=Win.setWindowPos,Win.msgbox
		pos=cmdPos=setWindowPos
		pid=Win.getpid()
	except Exception as ei:
		# def msgbox(s='',st='title',*a):
			# if(a!=()):s=str(s)+ ','+str(a)[1:-2]
			# if iswin():windll.user32.MessageBoxA(0, str(s), str(st), 0)
		setErr(ei,msg='#Error import Win'  )
#'G:\\QGB\\babun\\cygwin\\lib\\python2.7\\qgb'   ValueError('Attempted relative import beyond toplevel package',)
		py.pdb()
		# {0} {1}'.format(__name__,isMain() )
		
###########################
	if iscyg():
		def getCygPath():
			r=getProcessPath()
			if 'cygwin' in r:
				return T.subLast(r,'','cygwin')+'cygwin\\'
			else:
				raise EnvironmentError(r)
else:# *nix etc..， #TODO:isAndroid
	pid=os.getpid()
				
if isnix():
	def isroot():
		return os.getuid()==0
		
		
#TODO: if not has ei,import error occur twice,why?
def driverPath(a,reverse=True):
	'''from Z to C'''
	if not a.startswith(':'):a=':'+a
	# try:AZ=T.AZ;exist=F.exist
	# except:
	AZ=''.join([chr(i) for i in range(65,65+26)])
	exist=os.path.exists
	if reverse:AZ=AZ[::-1]
	for i in AZ:
		if exist(i+a):return i+a
	return ''

def getTestPath():
	if isnix():
		s='/test/'
		if isroot():
			return s
		else:
			home=os.getenv('HOME')
			if home.startswith('/home/coding'):
				home+='/workspace'
			return home+s
	if iswin() or iscyg():
		s='c:/test/'
		return driverPath(s[1:]) or s
gst=gsTestPath=getTestPath()


def getShellPath():
	'''wsPath=G:\QGB\babun\cygwin\home\qgb\wshell\
	'''
	if isnix():s='/bin/qgb/'
	if iswin() or iscyg():
		if 'wsPath' in os.environ:
			s=os.environ['wsPath']
		s='G:/QGB/babun/cygwin/home/qgb/wshell/'#如果开头多一个空格，在Pycharm 下返回False，其他环境下为True
		if path.exists(s):
			pass
		else:
			s='E:/sourceCode/shell/'
		s=driverPath(s[1:]) or s
	return s.replace('\\','/')
gsw=gsWShell=getShellPath()


def pln(*a,**ka):
	'''pln *data,  [en]cod[ing]='gb18030' ,r=False
	if r 应该返回参数  [U.pln(i) for i in _211]
	应该正确处理 中文 list dict ...'''
	# def den(k):
		# if py.type(k) is py.unicode:k=k.encode(encoding)
		# if py.type(k) is py.str:
			# rd=T.detect(k)
			# if rd.popitem()[0]>0.9:dc=rd[1]
			# else:dc=decoding
			# k=k.decode(dc).encode(encoding)
		# return k
	if 	'end' not in ka:ka['end']='\n'
	return p(*a,**ka)	
println=pln
	
def p(*a,**ka):
	'''
 # in  py 3.6
	print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
	----> 1 sys.stdout.write(_21)
	TypeError: write() argument must be str, not bytes
	sys.stdout.write('[\u9999')#[香

	in 2.7
	# print(k,end='')#SyntaxError: invalid syntax in 2.7 ;use from __future__ import print_function
	U.p(123,456,file=file ,end='\n')#  输出多个参数没有正确换行
iterable 的元素,没有特殊处理
	'''
	cod=''
	r=False
	sep=' '
	end=''
	file=sys.stdout
	flush=True#default
	for k in ka:
		k=k.lower()
		if 'sep'   in k:sep  =ka[k];continue
		if 'end'   in k:end  =ka[k];continue
		if 'file'  in k:file =ka[k];continue
		if 'flush' in k:flush=ka[k];continue
		if 'cod'   in k:cod  =ka[k];continue# 解码
		if 'r'     in k:r    =ka[k];continue#  放最后，防止名字冲突
	if py.len(a)==0:#print (end='233') #233
		file.write(end)
		if flush:
			if getattr(file,'flush',None):file.flush()
# in npp pythonScript :  AttributeError: 'Console' object has no attribute 'flush' 
		return
	if py.len(a)==1:
		a=a[0]
		at=py.type(a)
		# if a=='':file.write(a)#no effect;	#u''==''#True
		if cod:a=a.decode(cod)
		if py.is2():
			if at is py.unicode:a=a.encode(encoding)#编码
			# elif not py.istr(a):
		a=py.str(a)	
		file.write(a)
		p(end=end,file=file,flush=flush)
		if r:return a
		else:return
	elif py.len(a)>1:
		# if 'sep' in ka.keys():sep=ka['sep']
		# else:sep=' '
		for i in a:
			p(i  ,sep='no useful',r='no useful',end='',file=file,flush=flush,cod=cod)
			p(sep,sep='no useful',r='no useful',end='',file=file,flush=flush,cod=cod)
			#只能使用一个参数位置，不然死循环,最后结尾sep
		p(end,sep='no useful',r='no useful',end='',file=file,flush=flush,cod=cod)
	if r:return a
	else:return
# p(4,2,sep='9')
# exit()

def readStdin(size=-1):
	'''size<0 read all, 
	If the size argument is negative or omitted, read until EOF is reached.'''
	if not stdin.isatty():
		stdin.seek(0)
		return stdin.read(size)
	else: return ''
getStdin=readStdin

def rindex(a,sub,start=0,end=-1):
	''' 'print(dir())'
		 _14[::-1]
		 '))(rid(tnirp' 
 '''
	return len(a)-a[::-1].index(sub)
def flat(*a,**options):
	'''Breadth-First Traversal'''
	noNone=False
	for o in options:
		if 'nonone' in o.lower():noNone=options[o]
		if one_in('isnone','hasnone', o.lower()):noNone=not options[o]
		# repl()
		
	a=list(a);r=[];i=0
	while i<len(a):
		if hasattr(a[i], '__iter__'):a.extend(a[i])
		else:
			if noNone and not a[i]:pass
			#TODO other condition
			else:r.append(a[i])
		i+=1
	# repl()
	return tuple(r)
	
# pln flat([[1,2,3], [5, 2, 8], [7,8,9]])
##(1, 2, 3, 5, 2, 8, 7, 8, 9)
# pln flat([1,2,3,[4,5,[1,2],6]],['aaa'])
##  (1, 2, 3, 'aaa', 4, 5, 6, 1, 2)
	
def md5(a='',file=''):
	'''[a] : string or buffer
	[file]:fileName
	return 32 hex(lowerCase) str'''
	import hashlib   
	
	if file:
		myhash = hashlib.md5()
		f = py.file(file,'rb')
		while True:
			b = f.read(8096)
			if not b :
				break
			myhash.update(b)
		f.close()
		return myhash.hexdigest()
	
	
	md5 = hashlib.md5()   
	md5.update(a)	
	return md5.hexdigest()  
	
def inMuti(a,*la,**func):
	'''bool a.func(la[i])'''
	r=[]
	la=flat(la)
	# repl()
	if len(func)!=1:func=None
	elif not func.keys()[0].startswith('f'):func=None
	else:
		func=func.values()[0]
		if type(func) is str:
			func=a.__getattribute__(func)
		else:func=a.__getattribute__(func.__name__)
			
		# if callable(func):			
	if not callable(func):
		for i in la:
			try:
				if a==i or a in i:r.append(i)
			except TypeError:continue
			except Exception as e:continue
	else:
		for i in la:
			if func(i):r.append(i)
		
		# return False
	# repl()
		
	return r
inmuti=inMuti

def getMethod(a,func):
	if callable(func):
		func=py.getattr(func,'__name__',None)
	if T.istr(func):
		fs=[]
		for i in py.dir(a):
			if i.startswith(func):
				i=py.getattr(a,i,None)
				if py.callable(i):fs.append(i)
		if py.len(fs) >1:raise ArgumentError('need unique func(Name) for a')
		return fs[0]
	return func
getmethod=getMethod

def inMulti(target,elements,*functions):
	if not functions:functions=[None]
	functions=py.set(flat(functions))
	r=[]
	for f in functions:
		for e in elements:
			if f==None:
				if target in e:r.append(e);continue
				continue
			method=getMethod(target,f)
			if method(target):r.append(e);continue
			elif py.callable(f):
				if f(target,e):r.append(e);continue
			#else: # 参数函数 无效
	return r
def multin(elements,target,*functions):
	'''函数为None时：element in target
	element.f(target) #  target.f(element) : py.map
	or f(element,target)
	只要element满足一个函数 ：就会作为结果添加。
		要想得到所有 函数结果，怎么办？
		要想 element满足所有函数，怎么办？ '''
	if not functions:functions=[None]
	functions=py.set(flat(functions))
	if DEBUG:pln(functions)   #set(['startswith', None])=={None, 'startswith'}
	r=[]
	for f in functions:
		for e in elements:
			if f==None:
				if e in target:r.append(e);continue
				continue
			method=getMethod(e,f)
 # '123'.startswith
 # <function startswith>
 # _('1')
 # True
			if method:
				if method(target):r.append(e);continue
#当 混用 inMulti 和 multin 时，注意调用参数应该交换，否则 --> 376 TypeError: startswith first arg must be str, unicode, or tuple, not list				
			elif py.callable(f):
				if f(e,target):r.append(e);continue
			#else: # 参数函数 无效
	return r
def mutin(la,a,func=None):
	'''#TODO : 重写 multin ,同时支持多个函数，方法，func=None 代表 xs[i] in a: '''
	if len(la)<1:return False
	r=[]
	if type(func) not in (str,) and not callable(func) :
		for i in la:
			try:
				if i in a:r.append(i)
			except:
				if i is a:r.append(i)
	else:
		if type(func) is str:
			for j in dir(la[0]):
				if j.startswith(func) and callable(la[0].__getattribute__(j)):
					func=la[0].__getattribute__(j)
			# if not callable(func):
				# raise Exception('not found "{0}" in la[0] methods'.format(func))
		if callable(func):
			if func.__name__ in dir(la[0]):
				for i in la:
					i=i.__getattribute__(func.__name__)(a)
					if i:r.append(i)
			else:
				for i in la:
					i=func(i,a)
					if i:r.append(i)
	return r
inMutiR=mutiIn=mutin
# exit()
def in_one(v,*ts):
	'''if v in i:return [v]
U.in_one('p',*Out.values())
Out[142]: ['p']
	'''
	for i in ts:
		try:
			if v in i:return [v]
		except:pass
	return []	
inOne=in_one
def all_in(vs,*t):
	'''for i in vs:i all_in t 
	U.all_in(list(string),T.PATH_NAME)  
	
	(1,2,3,[t])	or	([vs].[t])'''
	if not hasattr(vs, '__iter__'):vs=[vs]
	if len(t)==1:
		t=t[0]
	elif len(t)>1:
		vs.extend(t[:-1])
		t=t[-1]
	else:raise Exception(all_in.__doc__)
	# U.pln(vs,t)
	if DEBUG:pprint((vs,'*t:',t)  )
	for i in vs:
		try:
			if i not in t:return []
		except:return []
	return vs
allIn=all_in	
def in_all(v,*ts):
	for i in ts:
		try:
			if v not in i:return []
		except:pass
	return [v]
inAll=in_all
##########################################
def cmd(*a,**ka):
	'''show=False :show command line
	默认阻塞，直到进程结束返回
	subprocess
	sb.stdin.close() 才返回  stdout stderr
	
	'''
	s=''
	if iswin() or iscyg():quot='"'
	else:quot="'"
	
	if len(a)==0:
		if iswin() or iscyg():a=['cmd']
		# TODO #
	if len(a)==1:
		if type(a[0])==type(''):
			if not s.startswith(quot):
				s=quot+a[0]+quot
			if ':' in s and iscyg():
				s='cmd /c start "" '+s
		elif len(a[0])==1:s=T.string(a[0])
		elif len(a[0])>1:a=a[0]
	if len(a)>1:
		a=list(a)
		s=T.string(a.pop(0))+' '
		for i in a:
			if type(i)==type([]):
				for j in i:	
					s+=quot+T.string(i)+quot+' '
			else:
				s+=quot+T.string(i)+quot+' '
			
	# pln(s)
	# exit()
	try:
		if 'show' in ka and ka['show']:pln (repr(s))
		import subprocess as sb
		r=sb.Popen(s,stdin=sb.PIPE,stdout=sb.PIPE,stderr=sb.PIPE)
		r= r.stdout.read(-1)
		if py.is3():r=r.decode('mbcs')
		return r
		# return os.system(s)
	except Exception as e:return e
	# exit()
# cmd('echo 23456|sub','3','')	
def sleep(aisecond):
	__import__('time').sleep(aisecond)
	
def pause(a='Press Enter to continue...\n',exit=True):
	'''a=msg'''
	if iswin():
		# cmd('pause');return
		try:
			raw_input(a)
		except BaseException:#SystemExit is BaseException
			if exit:x()
			return False
	return True	
def run(a,*args):
	'''默认不阻塞

If you're using Pyhton 3, command.args is the easiest way:
	from subprocess import Popen
	command = Popen(['ls', '-l'])
pln command.args #['ls', '-l']
'''
	if DEBUG:pln (a,args)
		
	if type(a)==type(''):a=[a]
	if type(a)!=type([]):a=list(a)
	if len(args)>0:a.extend(args)
	if type(a)==type([]):
		for i,v in enumerate(a):
			if not py.istr(v):
				a[i]=v=str(v)
			if py.iswin() and v.startswith('"') and v.endswith('"'):
				a[i]=v[1,-1]
			
		r= __import__('subprocess').Popen(a)
		if getPyVersion()<3.3:r.args=a
		return r
	'''
In [151]: _131.poll?
Signature: _131.poll()
Docstring:
Check if child process has terminated. Set and return returncode
attribute.
File:      c:\qgb\anaconda2\lib\subprocess.py
Type:      instancemethod

In [152]: _131.poll
--------> _131.poll()
Out[152]: 0

In [153]:

In [153]: U.run 'calc'
--------> U.run('calc')
Out[153]: <subprocess.Popen at 0x24415d0>

In [154]: _153.poll
--------> _153.poll()

In [155]: repr _153.poll()
--------> repr(_153.poll())
Out[155]: 'None'

In [156]: repr _153.poll()
--------> repr(_153.poll())
Out[156]: '0'              #killed
'''	
	
def curl(a):
	if type(a)!=type(''):return
	if a.lower().startswith('curl '):
		a=a.replace('""','')
	if a.startswith('http'):
		cmd('curl',a)
	cmd(a)

# def isfile
# del __name__

def delMuti(a):
	r=[]
	rt= type(a)
	for i in a:
		if i not in r:r.append(i)
	if py.istr(rt):
		return ''.join([rt(i) for i in r])
	return r
delmuti=delMuti
def this():
	''' local dir'''
	repl()
	if not py.globals().has_key('__name__'):
		__name__='233qgb.U'
		# txt(globals())
		pln (__name__)
		
def repl(_=None,printCount=False,msg=''):
	# a=1
	ic=count('__repl__')
	if printCount:pln (ic)
	if msg:pln (msg)
	######################
	f=sys._getframe().f_back
	locals=f.f_locals
	try:
		locals['U']=sys.modules['qgb.U']
		locals['T']=sys.modules['qgb.T']
		locals['F']=sys.modules['qgb.F']
	except:
		locals['U']=sys.modules['U']
		locals['T']=sys.modules['T']
		locals['F']=sys.modules['F']
	# try:
		# locals['U']=__frame.f_locals['U']
	# except:  #KeyError: 'U'  if use in qgb.U Module
		# locals=mergeDict(locals,py.globals())
	if _!=None:
		if '_' in locals:
			locals['_qgb']=_
		else:
			locals['_']=_
	__import__('code').interact(banner="",local=locals)
	return
	
	# try:
		# from ptpython.repl import embed
		# embed(f.f_globals, f.f_locals, vi_mode=False, history_filename=None)
		# return
	# except:pass
	
	# try:import IPython;IPython.embed();return
	# except:pass
	
repl=pys=pyshell=repl

def reload(*mods):
	''' 不是一个模块时，尝试访问mod._module'''
	import sys,imp
	if len(mods)<1:#如果 mods 中含有长度为0的元素，会导致U重新加载
		# sys.modules['qgb._U']=sys.modules['qgb.U'] #useless, _U is U
		#if pop qgb.U,can't reload
		if 'qgb.U' in sys.modules:   imp.reload(sys.modules['qgb.U'])
		elif 'U' in sys.modules:     imp.reload(sys.modules['U'])
		elif 'qgb._U' in sys.modules:imp.reload(sys.modules['qgb._U'])
		else:raise EnvironmentError('not found qgb.U ?')
		# pln 233
	elif len(mods)==1:
		mod=mods[0]
		if not isModule(mod):
			# sys.a=mod
			# return
			try:
				if py.type(mod) is py.str:
					return reload(sys.modules[mod])
				elif '_module' in py.dir(mod):
					if not isModule(mod._module):raise Exception('instance._module is not module')
					mod=mod._module
					modules[mod.__name__]=mod
					return reload(mod)
					
					# if mod.__name__ in modules:#'qgb.ipy'
				else:raise Exception('instance._module not exists')
			except Exception as em:
				raise em
			
			# else:gbPrintErr=True#在函数局域覆盖全局属性
		try:
			imp.reload(mod)
		except Exception as ei:
			setErr(ei)
	else:
		for i in mods:
			reload(i)
R=r=reload

def tab():
	import readline, rlcompleter;readline.parse_and_bind("tab: complete")
autoc=tab

class __wrapper(object):
	def __init__(self, wrapped):
		self.wrapped = wrapped
	def __getattr__(self, name):
		try:
			
			return getattr(self.wrapped, name)
		except AttributeError:
			return 'default' # Some sensible default

__frame=sys._getframe().f_back
	
	
def clear():
	# sys.modules[__name__] = __wrapper(sys.modules[__name__])
	if iswin():os.system('cls')
	if isnix():os.system('clear')
C=c=cls=clear


def chdir(ap=gst,*a,**ka):
	if not ap:ap=gst
	if not py.istr(ap):raise py.ArgumentError('ap must be str Not:{0}'.format(ap))
	ap=path.join(ap,*a)
	

	mkdir=True
	if 'md' in ka:mkdir=ka['md']
	if 'mkdir' in ka:mkdir=ka['mkdir']
	if iscyg():mkdir=False#cyg下可以创建带:的目录，导致切换异常
	if mkdir:F.mkdir(ap)
	
	global gscdb
	# repl()
	# if path.abspath(gscdb) != pwd():
	gscdb.append(pwd())
	
	if path.isdir(ap):
		os.chdir(ap);return ap#True
	
	app=path.dirname(ap)
	if path.isdir(app):return chdir(app)
	else:pass
		
	if iswin() or iscyg():
		if ap[0]=='/'==ap[2] and ap[1] in T.az:#!cdv&pwd == '/c/Users/lenovo/Videos'
			return chdir(ap[1]+':'+ap[2:])
			
	for i in ap:
		if i not in T.PATH_NAME:raise Exception('need file path',ap,i)
	return py.No("#Can't cd "+ap)
cd=chdir

gscdb=[]
def cdBack(index=-1):
	'''False: cd path list []'''
	if gscdb:
		return cd(gscdb[index])
	else:
		return False
cdb=cdBack

def cdCurrentFile(*a):
	f=sys._getframe().f_back.f_globals
	if '__file__' in f:
		sp=os.path.abspath(f['__file__'])
		sp=os.path.dirname(sp)
		return cd(sp,*a)
	return False
cd__file__=cdc=cdCurrent=cdcf=cdCurrentFile

def cdTest(a=''):
	return cd(gst+a)
cdt=cdTest
	
def cdQPSU(a=''):
	return cd(getModPath()+a)
# @property
cdqp=cdqpsu=cdQPSU
	
def cdWShell(a=''):
	return cd(gsWShell+a)
cds=cdws=cdWShell

def cdpm():
	return cd('e:/pm')
	
def cdbabun(a=''):
	s=r'C:\QGB\babun\cygwin\home\qgb/'
	s=driverPath(s[1:])
	return cd(s+a)
def pwd(p=False,display=False):
	s=os.getcwd()
	if p or display:pln (s)
	# try:pwd.sp=F.getsp(s)
	# except:pass
	if not py.getattr(pwd,'sp',''):
		pwd.sp='/'
	s=s.replace('\\','/')
	
	return s+pwd.sp#带sp方便使用者拼接路径
getCurrentPath=pwd
	
def sort(a, cmp=None, key=None, reverse=False):
	'''sorted _5,cmp=lambda a,b:len(a)-len(b)  按长度从小到大排序
	在python2.x中cmp参数指定的函数用来进行元素间的比较。此函数需要2个参数，然后返回负数表示小于，0表示等于，正数表示大于。'''
	t=py.type(a)
	a=py.sorted(a,cmp,key,reverse)
	if py.istr(py):
		return ''.join([t(i) for i in a])
	else:
		return a
def sortDictV(ad,des=True):
	'''des True,,, python dict key auto sort ?'''
	if type(ad) is not dict:return {}
	return sorted(ad.iteritems(),key=lambda ad:ad[1],reverse=True)
# d={}
# for i in range(7):
	# d[i]=i*i-5*i
	
# d={'ok':1,'no':2}
# d={0: 0, 5: 0, 6: 6, 1: -4, 2: -6, 3: -6, 4: -4}

# d=sortDictV(d)

# exit()

def evalSafely(source, globals=None, locals=None,noErr=False):
	''' '''
	if globals==locals==None:
		f=sys._getframe().f_back
		globals=f.f_globals
		locals =f.f_locals		
	try:
		return py.eval(source,globals,locals)
	except Exception as e:
		if noErr:
			return py.No(e)
		else:
			return e
eval=evalSafely

def execHelp():
	'''use py.execute(s,{g:},{l:})
	is2 ： exec_stmt ::=  "exec" or_expr ["in" expression ["," expression]]
	参数1  字符串，文件对象，代码对象，或者元组。如果它是一个字符串，该字符串将被当做Python 语句组解析，然后执行（除非发生语法错误）。[1] 如果它是一个打开的文件，将解析该文件直到EOF并执行。如果它是一个代码对象，将简单地执行它。对于元组的解释，参见下文。对于所有的情况，都期望执行的代码和文件输入一样有效（参见文件输入一节）。注意即使在传递给exec语句的代码中，return和yield语句也不可以在函数定义之外使用。

在所有情况下，如果可选的部分被省略，代码将在当前的作用域中执行。如果in 之后给出第一个表达式，它应该是一个字典，全局和局部变量都将使用它。如果给出两个表达式，它们将分别用于全局和局部变量。如果给出，局部变量可以是任意一个映射对象。记住在模块级别，全局变量和局部变量是同一个字典。如果给出两个不同的对象作为全局变量 和 局部变量，代码的执行将像是在类定义中一样。

第一个表达式也可以是一个长度为2或者3的元组。在这种情况下，可选的部分必须被省略。exec(expr, globals) 形式等同于exec expr in globals， 而exec(expr, globals, locals) 等同于exec expr in globals, locals。exec 的元组形式提供了与Python 3的兼容性，在Python 3中exec 是一个函数而不是语句。

Changed in version 2.4: Formerly, locals was required to be a dictionary.

As a side effect, an implementation may insert additional keys into the dictionaries given besides those corresponding to variable names set by the executed code. 例如，当前的实现可能以键__builtins__添加一个指向内建模块__builtin__ 的引用(!)。

给程序员的提示：内建函数eval()支持动态计算表达式。内建函数 globals()和locals()分别返回当前的全局变量和局部变量字典，可传递给exec使用。
	diff between eval and exec in python
	exec not return 
	    a=exec('1')
         ^
		SyntaxError: invalid syntax
'''
	return py.help('exec')  # py2 & py3  OK
	# exec(s)

def calltimes(a=''):
	a='_count'+T.string(a)
	if a in calltimes.__dict__: 
		calltimes.__dict__[a]+=1
	else:
		calltimes.__dict__[a]=0
	return calltimes.__dict__[a]
ct=count=counter=calltimes
def _ct_clear():
	r=calltimes.__dict__
	calltimes.__dict__={'clear':_ct_clear}
	return {k:v for k,v in r.items() if k.startswith('_count')}
calltimes.clear=_ct_clear




def setStd(name,file):
	'''name=[std]out err in'''
	name=name.lower()
	if py.istr(file):
		file=open(file,'w+')
	if py.isfile(file):
		if file.closed:raise ArgumentError('need an opened mode=w+ file')
	if py.len(name)<4:name='std'+name
	d=py.globals()
	if d.has_key('__'+name) and d['__'+name]:
		old=getattr(sys,name)
		old.close()
		py.execute('''sys.{0}=file'''.format(name))
	else:
		
		py.execute("d['__{0}'],sys.{0}=sys.{0},file".format(name))
	return True
setstd=setStd	

def resetStd(name=''):
	name=name.lower()
	if py.len(name)<4:
		std='std'+name
		name='__std'+name
	elif not name.startswith('__'):
		if name.startswith('std'):
			std=name
		name='__'+name
	else:
		raise ArgumentError('stdxxx')
		
	try:
		sm=globals()[name]
		stdm=getattr(sys,std)
	except Exception as e:
		setErr(e)
		return False
	if(sm and sm != stdm):
		stdm.close()#以前设置的std
		py.execute('sys.{0}=sm'.format(std))
	return True
resetstd=resetStd#=resetStream
gsBrowser=''
def browser(url,browser=gsBrowser,b=''):
	'''b,browser='yandex'
	'''
	if istermux():return run('termux-open-url',url) 
	import webbrowser
	if gsBrowser:browser=gsBrowser
	if b:browser=b
	sp=''
	def _open(asp,url):
		b=sys._getframe().f_back.f_code.co_names[-1]#get caller function name 
		webbrowser.register(b, None, webbrowser.BackgroundBrowser(asp))
		return webbrowser.get(b).open_new_tab(url)
	def chrome(url):
		###TODO: auto Find system base everything
		try:sp=getProcessList(name='chrome.exe')[-1].cmdline()[0]
		except:sp='''C:\QGB\Chrome\Application\chrome.exe'''
		_open(sp,url)		
	def yandex(url):
		sp=getProcessList(name='browser.exe')[-1].cmdline()[0]
		_open(sp,url)
	for i in py.dir():
		if not browser:
			webbrowser.open(url)
			break
		if py.eval('callable({0})'.format(i)):
			if browser.lower()== i:
				py.execute('{0}(url)'.format(i) ) in globals(),locals()  
		
	 
	# webbrowser.open_new_tab(url)
	# if iswin():os.system('''start '''+str(url))
# browser('qq.com')

gsHtmlTextarea=('<textarea style="width:100%; height:100%;">','</textarea>')
		
def autohtml(file=None):
	import T
	if not py.istr(file):
		if file is None:file=stime()+'.html'
		else:
			if hasattr(file,'__name__'):
				if '.htm' not in file.__name__:
					file=file.__name__+'.html'
			else:file='obj_{0}.html'.format(hash(file))
	elif  len(T.filename(file))<1:file=stime()+'.html'
	elif '.htm' not in file.lower():file=file+'.html'
	return file	

	
def shtml(txt,file='',browser=True,b=''):
	# import T,F
	import pprint
	if file=='' and not py.istr(txt):
		try:file=T.filename(T.max(txt.__str__(),txt.__repr__(),txt.__name__)[:19])
		except:pass
	
	# if type(txt) in (dict,list):
	txt=pprint.pformat(txt)
		# if len(txt)==0:return
		# s=[]
		# for i in txt.keys():
			# s.append(T.string(i)+'   :   '+T.string(txt[i])+'\n')
		# txt=T.listToStr(s)
		# 
	if len(file)<1:file=T.filename(getObjName(txt)+stime())[:19]
	if not file.lower().endswith('.txt'):file+='.txt'
	file=F.write(file,txt)
	# f=open(file+'.txt','a')
	# rm(f.name)
	# txt=txt.replace(gsHtmlTextarea[1],gsHtmlTextarea[1][:1]+'!!!qgb-padding!!!'+gsHtmlTextarea[1][1:])	
	# f.write(gsHtmlTextarea[0])
	# f.write(txt)
	# f.write(gsHtmlTextarea[1])
	# f.close()
	if b:browser=b 
	if(browser):
		if T.istr(browser):
			globals()['browser'](file,browser=browser)
		else:globals()['browser'](file)
	return file
txt=shtml	

def add(*a):
	a=flat(a)
	r=0
	for i in a:
		if py.isnum(i):
			r+=i
		else:
			raise NotImplementedError('not num type')
	return r		
def maxLen(*a):
	if py.len(a)==1:a=flat(a)
	im=-1
	for i in a:
		i=len(i)
		if i>im:im=i
	return im
def minLen(*a):
	if py.len(a)==1:a=flat(a)
	if not a:return -1
	im=gimax
	for i in a:
		i=len(i)
		if i<im:im=i
	return im
def avgLen(*a):
	if py.len(a)==1:a=flat(a)
	if not a:return -1
	im=0
	for i in a:
		im+=len(i)
	return float(im)/len(a)
	
	
def printAttr(a,b='chrome',console=False,call=False):
	'''if call: aoto call __methods which is no args'''
	d=py.dir(a)
	
	if console:
		sk='%-{0}s'.format(maxLen(d))
		si='%-{0}s'.format(len(py.len(  d  )))
		for i,k in py.enumerate(d):
			pln (si%i,sk%k,py.eval('a.{0}'.format(k)))
		return
		
	sh='''<tr>
	 <td>{0}</td>
	 <td id=name>{1}</td>
	 <td><textarea>{2}</textarea></td>
	 <td>{3}</td>
    </tr>'''
	sp=getModPath()+'file/attr.html'
	r='';v='';vi=-1
	for i,k in py.enumerate(d):
		try:
			v=getattr(a,k,'Error getattr')#py.eval('a.{0}'.format(k))			
			vi=len(v)
			# import pdb;pdb.set_trace()
			# if py.callable(v):
				# if k.startswith('__'):
					# vv='# ErrCall {0}()'.format(k)
					# try:
						# if isipy():#在ipython 中存在用户名字空间自动清空的问题
							# pass
						# else:
							# vv=v()
					# except:pass
					# v='{0} == {1}'.format(v,vv)
				
				# v=str(v)
				# v+=getHelp(v)
			if type(v) is not str:
				import pprint				
				try:#  调用非内置函数可能会造成严重的副作用
					if call and py.callable(v) and k.startswith('__'):vv=v()
					else:vv=''
				except Exception as ev:vv='#call Err:'+py.repr(ev)
				if v in (None,True,False) or py.isnum(v):v=str(v)
				else:
					if isinstance(v,(py.list,py.tuple,py.dict,py.set)):
						v=pprint.pformat(v)
					else:
						v='{0}=========== {1} \n{2}'.format(getHelp(v,del_head_line=2),vv,pprint.pformat(v))
		except Exception as e:v=py.repr(e)
		
		v=v.replace(gsHtmlTextarea[0], '*'*33)
		v=v.replace(gsHtmlTextarea[1], '*'*11)
		
		r+=sh.format(i,k,v,vi)
	# cdt('QPSU')
	# import T,F
	name=gst+'QPSU/'+T.filename(getObjName(a))+'.html'
	# pln (name)
	browser(name,b)
	if not r.strip():py.pdb()
	return F.write(name,F.read(sp).replace('{result}',r),mkdir=True)
	
	
	# cdBack()
pa=printattr=printAttr
# repl()
# printAttr(5)

def dir(a,fliter='',type=py.no):
	r=[i for i in py.dir(a) if fliter in i]
	rv=[]
	err=py.No("#can't getattr ")
	for i in r:
		ok=True
		v=py.getattr(a,i,err)
		if type!=py.no:#只要满足以下一条 就ok
			ok=False
			if py.istr(type):type=type.lower()
			
			if type==py.callable or type=='callable':
				if ok or py.callable(v):ok=1
				else:                   ok=0
			#############
			if ok or py.type(v) is type or isinstance(v,type) or py.type(v)==py.type(type):
				ok=1
			else:ok=0
			
		if ok:rv.append([py.len(rv),i,v])
	return rv

gAllValue=[]
def dirValue(a=None,fliter='',type=None,recursion=False,depth=2,timeout=6,__ai=0):
	'''a=None is dir()
	约定：只有无参数函数才用 getXX  ?'''
	if not __ai:dirValue.start=getTime();dirValue.cache=[]
	r={}
	if getTime()-dirValue.start>timeout:return py.No('#timeout')#r[i]='!timeout %s s'%timeout;break
	
	if a==None:
		import inspect
		f=inspect.currentframe().f_back
		dr=f.f_locals
	else:	
		dr=py.dir(a)
	for i in dr:
		
		try:
			if a==None:
				tmp=dr[i]
			else:
				tmp=getattr(a,i,'!Error getattr')#py.eval('a.'+i)
			if tmp in dirValue.cache:r[i]=('!cache',tmp);continue
			else:dirValue.cache.append(tmp)
			if recursion:
				if __ai>depth:return '!depth reached'
				tmp=dirValue(tmp,fliter,type,recursion,__ai=__ai+1,depth=depth,timeout=timeout)
			if fliter not in i:continue	
			if type!=None:
				if T.istr(type):type=type.lower()
				if type==py.callable or type=='callable':
					if py.callable(tmp):
						r[i]=tmp
						continue
				if py.type(i)==type or isinstance(i,type):pass
				else:continue	
			r[i]=tmp
				
		except Exception as e:
			r[i]=Exception('can not get value '+i)
			r[i]=e
	return r
DirValue=getdir=getDirValue=dirValue

def searchIterable(a,fliter='',type=None,depth=2,ai=0):
	'''iterable
	# typo deepth
	'''
	if ai>depth:return
	r=[]
	for i in a:
		try:
			if fliter in i or searchIterable(i,fliter,type,depth,ai+1):
				r.append(i)
				if ai==0:continue
				else:break
		except:pass
	return r	
searchIterable.r=[]
findIterable=iterableSearch=searchIterable
def isinstance(obj,Class):
	'''isinstance(obj, class_or_tuple, /)
	#3:isinstance(None, None)#False
#2:TypeError: isinstance() arg 2 must be a class, type, or tuple of classes and types
'''
	try:
		return py.isinstance(obj,Class)
	except Exception as e:
		return py.No(e)

def issubclass(cls, class_or_tuple):
	try:
		return py.issubclass(cls,class_or_tuple)
	except Exception as e:
		return py.No(e)
		
def getObjName(a,value=False):
	try:#is3 len(None)==4
		if a.__name__ and len(a.__name__)>0:
			return a.__name__
	except:pass
	
	try:
		r=str(a.__class__)
		if 'type' in r:
			return T.sub(r,T.quote,T.quote).strip()
	except:pass
	
	if py.isnum(a) and not type(a) is py.float:return 'i_'+str(a)
	if py.istr(a):return 's_'+a[:7]
		
	return str(type(a))
	# exit()
getName=getObjName

def getVarName(a,funcName='getVarName'):
	'''funcName :defined for recursion frame search
	
	在python2中 str unicode 字面相同情况下， == True
	
	'''
	import inspect#,re,T
	for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
		return line[line.index('(')+1:line.rindex(')')].strip()
		#2017-6-24 01:29:13   正常
		
		r=T.sub(line,'(',')')
		if '(' not in r:
			return r
		# if funcName not in line:continue
		# line=T.sub(line,funcName,'').strip()
		# i0=line.find('(')
		# i1=line.find('(',i0+1)
		# if i1==0:return T.sub(line,'(',')').strip()
		# else:
		
		
		pln (repr(line))
		arr = []
		i=-1
		# repl()
		for c in line:
			i+=1				
			if c=='(':
				arr.append((i,c))
			elif c==')':
				if arr and arr[-1][1] == '(':
					il=arr.pop()[0]+1
					# ir is i
					pln (il,i,repr(line[il:i])   )
					if line.find(funcName,il,i)!=-1:
						il=il+line[il:i].find('(')+1 
						i =il+line[il:i].rfind(')')
						
						pln (repr(line[il:i].strip())  )
					else:
						pass
					# ra(i,c)
				else:
					return False
	
	# pln il,i,repr(line)
		# if inMuti():return line
name=getArgName=getVarName
# repl()
# exit()
# getVarName(1l)
def getArgs(a):
	import inspect
	try:
		return inspect.getargspec(a)
	except Exception as e:
		return py.No(e)
getargspec=getargs=getarg=getArgs
#npp funcList 不索引注释
def enumerate(a,start=0,ignoreNull=False,n=False):#todo 设计一个 indexList类，返回 repr 中带有index，用下标访问与普通list一样
	'''enumerate(iterable[, start]) -> iterator for index, value of iterable
	
	list <enumerate at 0x6a58d00>
	ignoreNull : return if a[i]
	
	'''
	if n:ignoreNull=True
	r=[]
	# index=start
	for i,v in py.enumerate(a):
		if ignoreNull:
			if not v:continue
		r.append( (start,v) )
		start+=1
	return r
il=ilist=indexList=enumerate
	
def isModule(a):
	return type(a) is module
isMod=ismod=ismodule=isModule

def getHelp(a,del_head_line=0):
	import pydoc,re
	try:a=pydoc.render_doc(a,'%s')
	except:a='#getHelp Err'
	a=re.sub('.\b', '', a)
	originURL='docs.python.org/library/'
	targetURL='python.usyiyi.cn/documents/python_278/library/{0}.html\n'+originURL
	# msgbox(isModule(a))
	if originURL in a:
		a=a.replace(originURL,targetURL.format(T.sub(a,originURL,'\n')))
	elif isModule(a):
		a=a.replace('NAME',   targetURL.format(T.sub(a,'NAME',' - ').strip() ) )
		# repl()
	if del_head_line:
		a='\n'.join(a.splitlines()[del_head_line:])
	return a
gethelp=getHelp
	
def helphtml(obj,*aos):
	txt=''
	if aos:
		aos=flat(obj,aos,noNone=True)
		for i in aos:
			txt+=getHelp(i)
			txt+='\n==============%s=======================\n'%ct(aos)
	else:txt=getHelp(obj)	

	file='Uhelp_obj.txt'
	try:
		import T
		if obj:file=T.filename(getObjName(obj))+'.txt'
		elif aos:file=T.filename(getObjName(aos[0]))+'..%s.txt'%len(aos)
	except:pass
	

	with open(file,'w') as f:
		f.write(txt)
	# write(file,txt)
	globals()['browser'](file)
h=help=helphtml
# if __name__=='__main__':help(h);exit()

def getLine():
	import inspect,re
	for line in inspect.getframeinfo(sys._getframe().f_back)[3]:
		return line
		# if m:return m.group(1)
	# repl()

	
def dicthtml(file,dict,aikeylength=10,browser=True):
	for i in dict.keys():
		if(len(i)>aikeylength):aikeylength=len(i)+1
	sformat='%-'+str(aikeylength)+'s:'
	txt=''
	for i in dict.keys():
		txt+= (sformat%i)+str(dict[i])+'\n'
	txt=txt.replace(gsHtmlTextarea[1],gsHtmlTextarea[1][:1]+'!!!qgb-padding!!!'+gsHtmlTextarea[1][1:])	
	f=open(file,'w+')
	f.write(gsHtmlTextarea[0]+txt+gsHtmlTextarea[1])
	f.close()
	if(browser==True):globals()['browser'](f.name)
	# pln vars()
	# vars()['browser'](f.name)

def phtml(file):
	raise Exception('#TODO')
	if(file.lower()[-1]!='l'):file=file+'.html'
	# setOut0(file)
	pln (gsHtmlTextarea[0])
def phtmlend():
	raise Exception('#TODO')
	pln (gsHtmlTextarea[1])
	sf=sys.stdout.name
	# resetOut0()
	globals()['browser'](sf)
# dicthtml('uvars.html',vars())

def mergeDict(*a):
	r={}
	for i in a:
		if type(i) != py.dict:
			try:i=py.dict(i)
			except:continue
		for k,v in i.iteritems():
			r[k]=v
	return r
	
def getTimestamp():
	'''return: float
--------> U.time()
Out[304]: 1490080570.265625

In [305]: U.time
--------> U.time()
Out[305]: 1490080571.125
'''
	return __import__('time').time()
time=getime=getTime=timestamp=getCurrentTime=getTimestamp
	
	
	
def getFloaTail(a,ndigits=20,s=False,str=False,string=False,i=False,int=False):
	''' see help round()
 0.1**5
 1.0000000000000003e-05

 0.1**4
 0.00010000000000000002 小数位数20
 '''
 
	if type(a) is float:
		a=round(a-py.int(a),ndigits)#This always returns a floating point number.
		if s or str or string:
			return py.str(a)[1:]
		if i or int:
			return py.int(py.str(a)[2:])#
		return a	
gsTimeFormatFile='%Y-%m-%d__%H.%M.%S__'
gsymd=gsYMD=gsTimeFormatYMD='%Y%m%d'
gsTimeFormat='%Y-%m-%d %H:%M:%S'
#ValueError: year=1 is before 1900; the datetime strftime() methods require year >= 1900

def getStime(time=None,format=gsTimeFormatFile,ms=True):
	'''http://python.usyiyi.cn/translate/python_278/library/time.html#time.strftime
	TODO: 可以指定 ms'''
	if not py.istr(format):raise ValueError('format is str')
	
	import time as tMod
	
	# if ':' in format:format=gsTimeFormatFile.replace('.',':')
	
	if not py.isnum(time):time=getTimestamp()#TODO:  转换 字符串 或其他时间格式
	if not time:time=0.000001
	if py.type(time) is not py.float:time=py.float(time)
	if format=='':return str(time)
	
	if '%' in format:
		if time:
			r=tMod.strftime(format,tMod.localtime(time))
#localtime: time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=8,....
			if type(time) is float and ms:
				# if '__' in format:
					# if not r.endswith('__'):r+='__'
				# else:#r endswith '.' 
					# pass
				r+=getFloaTail(time,ndigits=3,s=True)
			return r
		else:return tMod.strftime(format)
stime=getCurrentTimeStr=timeToStr=getStime
	
def int(a,default=0,error=-1):
	if not a:return default
	try:return py.int(a)
	except:return error
	
def primes(n):
	''' 

	'''
	#in py3 fliter return	<filter at 0x169a9704e80>
	r=filter(lambda x: not [x%i for i in range(2, int(x**0.5)+1) if x%i ==0], range(2,n+1))	
	return py.list(r)
  
  
def traverseTime(start,stop=None,step='day'):
	'''range(start, stop[, step])
	datetime.timedelta(  days=0, seconds=0, microseconds=0,
                milliseconds=0, minutes=0, hours=0, weeks=0)
	step default: 1(day)  [1day ,2year,....]  [-1day not supported]'''
	import re,datetime as dt
	sregex='([0-9]*)(micro|ms|milli|sec|minute|hour|day|month|year)'
	timedeltaKW=('days', 'seconds', 'microseconds',
 'milliseconds', 'minutes', 'hours', 'weeks')
	if py.type(step) in (py.str,py.unicode):
		step=step.lower()
		rm=re.match(sregex,step)
		if not rm or not step.startswith(rm.group()):
			raise Exception('Invalid argument step '+py.repr(step))
		istep,step=int(rm.group(1),default=1,error=0),rm.group(2)
		if step.startswith('year'):
			istep,step=365*istep,'day'#没考虑闰年
		if step.startswith('ms'):step='milliseconds'
		astep={}
		for i in timedeltaKW:
			if i.startswith(step):
				astep[i]=istep
		tdelta=dt.timedelta(**astep)
	elif py.type(step) in (py.int,py.long):
		tdelta=dt.timedelta(days=step)
	elif py.type(step) is py.type(dt.timedelta.min):
		tdelta=step
	# return tdelta
	start=datetime(start)
	if stop:stop=datetime(stop)
	else:stop=dt.datetime.max
	while start<=stop:
		start+=tdelta
		yield start
	# return i #SyntaxError: 'return' with argument inside generator

timeTraverser=timeTraversal=traverseTime	
def datetime(a,month=0, day=0,hour=0,minute=0,second=0,microsecond=0):
	''' a : string
	return datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required. tzinfo may be None, or an
instance of a tzinfo subclass. The remaining arguments may be ints or longs.
	'''
	from datetime import datetime as dt
	import re
	if py.type(a) is py.type(dt.min):
		return a
	elif py.type(a) in (py.str,py.unicode):
		rm=re.match('([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}).([0-9]{2}).([0-9]{2}) .([0-9]{3})',a)
		if rm:
			a=T.parseReMatch(rm,'i'*6)+(py.int(rm.group(7))*1000,)
			return dt(*a)
		
		if re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}',a) or\
		re.match('[0-9]{4}-[0-9]{4}',a):a=a.replace('-','')
		if re.match('[0-9]{8}',a):
			return dt(py.int(a[:4]),
				py.int(a[4:6]),py.int(a[6:8]))
	elif py.type(a) in (py.float,py.int):
		return dt.fromtimestamp(a)
	else:
		raise ArgumentError(a)
		
		
		# if '-' in a and py.len:

from threading import enumerate as getAllThreads
threads=gethreads=getAllThreads
def getThreads():
	r=()
	for threadId, stack in sys._current_frames().items():
		r+=(threadId,)
	return r
	


SG_EXIT='exit'
SG_ASK='ask'
__bsg=False
def __single(port,callback,reply):
	import socket
	__bsg=True
	sock=None
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	sock.bind(('0.0.0.0', port))
	sock.listen(5) 
	while True:	
		if(not __bsg):break
		connection,address = sock.accept()	
		try:	
			connection.settimeout(50)
			buf=''
			while buf!=None:
				
				buf = connection.recv(4096) 
				if(reply!=None):connection.send(reply+buf)
				Thread(target=callback,args=[buf]).start()
				# msgbox(buf)
		except Exception as e:  #如果建立连接后，该连接在设定的时间内无数据发来，则time out  
			# if(str(e)!='[Errno 10053] '):
			if(DEBUG):pln (e ,'#%s#'%str(e)  )
			continue
	connection.close()   

def notsingle(port,ip='127.0.0.1'):
	try: 
		import socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
		sock.connect((ip, port))
		sock.send(SG_ASK)	
		sock.close()
		return True
	except Exception:
		return False 
def single(port,callback,reply='\naccepted:'):
	'''singleton'''
	Thread(target=__single,args=[port,callback,reply]).start()
	
def singlexit():
	pass
	

def fields(obj):
	import inspect
	return inspect.getmembers(obj)

def methods(obj):
	def y():
		for i in py.dir(obj):
			if py.callable(py.eval('obj.'+i)):
				yield i
	# printAttr(y)
	
	# printAttr([])
	return list(y())
	
	# exit()
# pln methods([])	
	
def x(msg=None):
	'''sys.exit'''
	if(msg!=None):pln (msg)
	sys.exit(235)
	
def exit(i=2357,msg='\n{} pid {} exit!'.format('#'*22,pid)):
	'''terminate process,will not call atexit'''
	print(msg)
	os._exit(i)

def getModsBy__all__(modPath=None):
	r=[]
	if modPath==None:modPath=getModPath()
	modPath=F.getPath(modPath)
	fs= F.ls(modPath,t='r')
	for f in fs:#大写 畸形 不考虑
		if not f.endswith( '__init__.py'):continue
		content= F.read(f)
		ia=T.re_search('\s*__all__\s*=\s*.*',content)
		if '[' in ia and ']' in ia:
			i=T.sub(ia,'[',']')
		else:
			if '[' not in  ia:
				# print(i[0][-30:-10],'[   ] 都没有',repr(i[1]))
				ct('n [');
				continue
			i=T.sub(content,ia,']')
		i=evalSafely('['+i+']',noErr=1)
		if not i:ct('n i');continue
		r.append(i)
		try:
			print(f[-17-12:-12], i [:8] )
		except Exception as e:
			return f,i
	# for i in:
	return r
	fs=[i for i in fs if i.lower().endswith('.py')]
	
	
def getAllMods(modPath=None):
	r=[]
	if not modPath:modPath=getModPath()
	if 'F' in globals():
		for i in F.ls(modPath,t='r'):
			if not i.lower().endswith('.py'):continue
			i=i.replace(modPath,'')
			# if F.isPath(i):
			if i.lower().endswith('__init__.py'):
				if i.startswith('__init__.py'):continue#/qgb/*  去除qgb
				r.append(path.dirname(i))
			elif '__' not in i:
				r.append(T.subLast(i,'','.'))
	else:raise EnvironmentError('no qgb.F in U')
		# return r
	for i in os.listdir(modPath):
		if(len(i)<3):continue
		if(i.find('__')!=-1):continue
		if(i.lower()[-3:]!='.py'):continue
		r.append(i[:-3])
	if r:return [i.replace('/','.') for i in r]
	else:return   ['U', 'T', 'N', 'F', 'py', 'ipy', 'Win', 'Clipboard']
getAllMod=getAllModules=getAllMods
def getModPathForImport():
	return getModPath(qgb=False)
	sp=os.path.dirname(getModPath())# dirname/ to dirname
	sp=os.path.dirname(sp)
	if iswin():return sp#cygwin None
	else:raise NotImplementedError('todo: cyg  nix')
def getModPath(mod=None,qgb=True,slash=True,backSlash=False,endSlash=True,endslash=True,trailingSlash=True):
	'''不返回模块文件，返回模块目录
	@English The leading and trailing slash shown in the code 代码中的首尾斜杠'''
	# if mod:
		# sp=os.path.abspath(mod.__file__)
	if mod:sp=os.path.abspath(getMod(mod).__file__)
	else:sp=__file__
	sp=os.path.abspath(sp)
	sp=os.path.dirname(sp)
	sp=os.path.join(sp,'')
	#sp is qgb\ if qgb/.. import
	# if debug():py.pdb()
	if iscyg():#/usr/lib/python2.7/qgb/  
		sp=getCygPath()+sp[1+4:].replace('/','\\')
	if not qgb:
		sp=sp[:-4]
	
	if not endslash or not endSlash:trailingSlash=False
	if trailingSlash:
		if sp[-1] not in ('/','\\'):sp+='/'
	else:
		while sp[-1] in ('/','\\'):
			sp=sp[:-1]
			
	if backSlash or not slash:
		sp=sp.replace('/','\\')
	else:sp=sp.replace('\\','/')

	return sp
	
	
def len(a,*other):
	'''Exception return -1'''
	if other:
		r=[len(a)]
		for i in other:
			r.append(len(i))
		return r
	try:return py.len(a)
	except:
		# if type(a) in (int,float,list,tuple,dict):
			# return py.len(str(a))
		try:return py.len(str(a))
		except:return -1
		
def dis(a):
	from dis import dis
	return dis (compile(a,'<str>','exec'))

def getParentPid():
	import psutil
	return psutil.Process(os.getpid()).ppid()
getppid=getParentPid	
	
def getParentCmdLine():
	import psutil
	return psutil.Process(getppid()).cmdline()
getpargv=getParentCmdLine	
	
def getProcessList(name='',cmd='',pid=0):
	'''if err return [r, {i:err}  ]
_62.name()#'fontdrvhost.exe'
_62.cmdline()#AccessDenied: psutil.AccessDenied (pid=8, name='fontdrvhost.exe')
pid=0, name='System Idle Process', cmdline=[]
	
'''
	import psutil
	r=[]
	err=py.dict()
	for i in psutil.process_iter():
		try:
			i.cmd=' '.join(i.cmdline())
		except Exception as e:
			i.cmd=str(e) #NoneObj #TODO 需要一个 空字符 类，携带出错或其他信息				

		if pid:
			if pid==i.pid:r.append(i)
			continue# 找到 找不到 ，都下一条
		if cmd:
			if cmd in i.cmd:r.append(i)
			continue			
		# if name:
		iname=i.name()
		if name.islower():iname=iname.lower()# 忽略大小写匹配,(是否应该限定在Windows？)
		if name in iname:r.append(i)
		else:continue
				
		# except Exception as e:err[i]=e
	# r=py.list
	# if err:return r,err
	# else:  
	return r
ps=getProcess=getProcessList	
def getProcessPath(name='',pid=0):
	if not (name or pid):pid=globals()['pid']
	r=getProcessList(name=name,pid=pid)
	rs=[]
	if r:
		for i,p in enumerate(r):
			i=p.cmdline()
			if i:i=i[0]
			else:continue# 'System Idle Process', cmdline=[]
			if i not in rs:rs.append(i)
		if py.len(rs)!=1:raise Exception('multi path',rs)
		return rs[0].replace('\\','/')
	else:
		return ()
psp=getProcessPath
def kill(a,caseSensitive=True,confirm=True):
	'''TODO:use text Match if any
	'''
	import psutil,subprocess
	if isinstance(a,subprocess.Popen):a=a.pid
		
	ta=py.type(a)
	r=[]
	
	if ta in (py.str,py.unicode):
		for i in psutil.process_iter():
			if caseSensitive:
				if i.name() == a:r.append(i)
			else:
				if i.name().lower() == a.lower():r.append(i)
	elif ta is type(0):
		if not psutil.pid_exists(a):
			raise ArgumentError('pid %s not exist!'%a)
		r=[psutil.Process(a)]
	else:
		raise ArgumentUnsupported()
	if confirm:
		pprint(r)
		c=raw_input('kill Process？(n cancel)')
		if c.lower().startswith('n'):return
	for i in r:
		i.kill()
def getTasklist():
	''''''
	return
def notePadPlusPlus(a='',line=0,autof=True):
	'''
--------> os.system('"M:\\Program Files\\Notepad++\\notepad++.exe" "IP.py"')
'M:\Program' 不是内部或外部命令，也不是可运行的程序
或批处理文件。
Out[114]: 1

--------> os.system('"M:\\Program Files\\Notepad++\\notepad++.exe" IP.py')
Out[115]: 0

'''
	nppexe='/Notepad++/notepad++.exe'.lower()
	args=py.getattr(a,'args',None)
	if args and py.iterable(args):
		args=py.list(args)
		if py.istr(args[0]) and nppexe in args[0].lower():return run(args)
	
	if isModule(a):
		a=a.__file__
		autof=False
		
	a=py.getattr(a,'func_code',None) or a
	a=py.getattr(a,'__code__',None)  or a#is3
	
	if py.getattr(a,'co_filename',None): 	
		if not line:line=a.co_firstlineno#先获取line,再改变 a
		a=a.co_filename
		autof=False
	if py.getattr(a,'lineno',None):#is3 <FrameSummary  .__module__=='traceback'
		line=a.lineno
		a=a.filename
	if py.type(a) in (py.list,py.tuple):
	#,py.set TypeError: 'set' object does not support indexing
		if not line and py.len(a)>1:line=a[1]
		a=a[0]
	if py.isfile(a):a=a.name	
	#########################多个 elif 只会执行第一个匹配到的
	if py.istr(a):
		gsm=[['qgb.ipy.save ',' success!'],
				]
		for i in gsm:
			a=T.sub(a,i[0],i[1]) or a
		pass
	else:
		if py.getattr(a,'__module__',None):
			a=getModule(a)#python无法获取class行数？https://docs.python.org/2/library/inspect.html
			return notePadPlusPlus(a)
		raise ArgumentUnsupported(a)
		
		
	if a.endswith('.pyc'):#AttributeError: 'code' object has no attribute 'endswith'
		a=a[:-3]+'py'
	if Win.getVersionNumber()>=6.1:#win7
		npath=os.getenv('appdata').replace('\\','/')+nppexe
	if not os.path.exists(npath):	
		npath=getModPath()[:3]+r'QGB'+nppexe
	if not os.path.exists(npath):	
		npath=getModPath()[:3]+r'QGB'+'/npp/notepad++.exe'
	if not os.path.exists(npath):
		npath=driverPath(r":\Program Files"+nppexe)#如果最后没有匹配到，则为 空.....
	if DEBUG:pln (repr(npath),nppexe)
	# npath='"%s"'%npath
	if a:
		if autof:
			return run(npath,F.autof(a),'-n {0}'.format(line))
		else:
			return run(npath,a,'-n {0}'.format(line))
	else:
		run(npath)
		return npath 
		
	# cmd('npp',str(a))
npp=notePadPlus=notePadPlusPlus
	
def nppMods(modName='qgb'):
	r=py.modules(modName)
	pprint(r)
	py.input('npp above all ? Ctrl-c cancel')
	for i in r:
		npp(i)
		
def backLocals(f=None,i=0,r=[]):
	pln (i+1,'='*(20+i*2)  )
	
	if f is None and i==0:f=__import__('sys')._getframe()
	try:pln (f.f_locals.keys()  );r.append(f.f_locals)
	except:return r
	return backLocals(f.f_back,i+1,r)	
printFrame=backLocals
	
def getDate():
	'''return '20170301' #From os time'''
	from datetime import date
	t=date.today()
	return ('%4s%2s%2s'%(t.year,t.month,t.day)).replace(' ','0')
today=getdate=getDate
# sys.argv=['display=t','pressKey=t','clipboard=f']
def getAST(mod):
	import ast,inspect
	return ast.parse(getSource(mod))
getModAST=getAST

def getSource(a):
	import inspect
	if py.istr(a):
		return F.read(a)
		# return #fileName
	return inspect.getsource(a) # module, class, method, function, traceback, frame, or code object
getsource=getSource

def isSyntaxError(a):
	import ast
	try:
		ast.parse(a)
		return False
	except:
		return True
isyntaxError=iSyntaxError=isSyntaxError

def parse(code,file):
	from ast import parse,AST,iter_fields
	a=parse(code)
	annotate_fields=True
	include_attributes=False
	def _format(node,i=0):
		msgbox(node,i)
		if isinstance(node, AST):
			fields = [(a, _format(b,i+1)) for a, b in iter_fields(node)]
			rv = '%s\n{0}(%s'.format('\t'*i ) % (
					node.__class__.__name__, ', '.join(
						('%s=%s' % field for field in fields)
						if annotate_fields else
						(b for a, b in fields)
					)
				)
			if include_attributes and node._attributes:
				rv += fields and ', ' or ' '
				rv += ', '.join('%s=%s' % (a, _format(getattr(node, a),i+1))
								for a in node._attributes)
			return rv +'\n'+'\t'*i +')'
		elif isinstance(node, list):
			return '\n' +'[%s]' % ', '.join(_format(x,i+1) for x in node)
		return repr(node)
	F.new(file.name)
	# file.seek(0) 没用
	# print >>file,_format(a)
	pln(a,file=file)
	file.flush()
	return file.tell()
	
def replaceModule(modName,new,package='',backup=True):
	if package:
		if not package.endswith('.'):package+='.'
		if package+modName in sys.modules:
			modName=package+modName
	if backup:
		sys.modules['_'+modName] = sys.modules[modName]
	
	# if modName in sys.modules:
	sys.modules[modName]=new
	return sys.modules[modName]
	# else:return False
	# try:
		# sys.modules['qgb.ipy'] = IPy()
	# except:
		# sys.modules['ipy'] = IPy()
replacemod=replaceMod=replaceModule
def getModule(modName=None,surfixMatch=True):
	'''no Arg return U
	surfixMatch ==name All match
	difference between py.modules('name') : return only one matched module
	'''
	if not modName:modName='qgb.U'
	
	if isModule(modName):return modName
	modName=getattr(modName,'__module__',0) or modName
	# if debug():pln(modName,type(modName))
	
	if not py.istr(modName):
		raise ArgumentUnsupported(modName)
	for i in sys.modules:
		if surfixMatch:
			if modName ==i:return sys.modules[i]
		else:
			if i.endswith(modName):return sys.modules[i]
	if modName.startswith('qgb.'):
		modName=modName[4:]
		return getModule(modName)
	return ()
getmod=getMod=getModule

def test():
	pln('sys.path *U* :',[i for i in sys.modules if 'U' in i])
	
	gm=getAllMods()
	
	# repl()
	gm.extend(['U','T','N','F',])
	gm=py.set(gm)
	
	pln(gm)
	for i in gm:
		pln('='*55)
		try:
			i='''
import {0}
pln({0})
			'''.format(i) #只能顶开头写，不然  unexpected indent (<string>, line 2)
			py.execute(i)
				# exec(i,globals={}, locals={})      TypeError: exec() takes no keyword arguments
		except Exception as ei:
			pln('###import {0}'.format(i))
			pln(ei)
def explorer(path='.'):
	''' exp can not open g:/qgb '''
	path=path.replace('/','\\')
	if iswin():
		os.system('explorer.exe '+path)
exp=explorer

def log(*a):
	pln(a)

def logWindow():
	import Tkinter as tk
	#TODO:

def set(name,value=None):
	if py.type(name) is not py.str and value==None:
		set.__dict__['_']=name
		return
	set.__dict__[name]=value
def get(name='_'):
	return set.__dict__[name]
	#TODO
def google(a):
	a=T.urlEncode(a)
	return browser('https://init.pw/search?q='+a)
	browser('https://www.google.com.my/#q='+a)
	
def subprocess(cmd):
	from subprocess import PIPE,Popen
	return Popen(cmd,stdin=PIPE,stdout=PIPE,stderr=PIPE)
	
def sub(a,len='default return len 9',start=0,step=1):
	'''sub dict,list,tuple....iterable
	like a[start:start+len:step]
			postive stands for left>right
	minus	negative stands for right<left
	text sub use T.sub
	无法处理子元素过大的输出情况
	'''
	m=py.len(a)
	# if py.max(py.abs(start),py.abs(step))>m or len==0:
		# raise ArgumentError(len,start,step)
	if step==0:return py.type(a)()
	if isinstance(a,py.dict):r={}
	else:r=[]
	
	if start<0:start=m+start
	
	if step<0:reverse=True;step=-step
	else:reverse=False
	
	if py.type(len) is py.str:
		# if m/step>9:len=
		len=py.min(9*step,m/step)
	len=py.int(len)#int(9999999999999999999999999999999)=9999999999999999999999999999999L			
	
	n=-1
	ns=-1
	end=start+len*step
	for i in a:
		n+=1
		if len>0:
			if not start<=n<end:continue
		else:
			if not end<n<=start:continue
		
		ns+=1
		if ns<step and ns>0:continue
		else:ns=0
				
		# if step>0:
		
		# else:
			# if 
		if isinstance(a,py.dict):#所有不能用for in一次取出的类型
			r[i]=a[i]
		else:
			if reverse:r.insert(0,i)
			else:r.append(i)
	return r
def subLast(a,len='default',step=1):
	return sub(reversed(a),len=len,step=step)
subr=subLast
def reversed(a):
	if isinstance(a,py.dict):return reversedDict(a)
	r=[]
	for i in py.reversed(a):
		r.append(r)
	return r
def reversedDict(d):
	r=OrderedDict()
	for i in py.reversed(OrderedDict(d)):
		r[i]=d[i]
	return r
	
def difference(a,b):
	'''差集 a-b'''
	return py.set(a)-py.set(b)
cj=diff=difference	
	
def j(a,b):
	'''intersection 交集
	
	TypeError: unhashable type: 'dictproxy' #TODO
	'''
	isdict=isinstance(a,py.dict) and isinstance(b,py.dict)
	r=[]
	for i in a:
		if i in b:
			if isdict:
				if a[i]==b[i]:r.append((i,a[i]))
				else:		  r.append((i,a[i],b[i]))
				continue
			r.append(i)
			
			
	return r
	# return py.set(a).intersection(py.set(b))

def jDictValue(a,b):
	'''
	'''
	r={}
	vb=b.values()
	for i in a.items():
		if i[1] in vb:
			r[i[0]]=i[1]
	return	r
jdv=jDictValue

def getNestedValue(a,*key):
	'''safely get nested  a[k1][k2][...]
	
setErr( gError 还是要保留，像这种 出错 是正常流程的一部分，但是又想把错误记录下来
#todo
	'''
	if py.len(key)==0:raise ArgumentError('need at least one key')
	if py.len(key)==1:
		try:return a[key[0]]
		except:return ()
	else:
		try:return getNestedValue(a[key[0]],*key[1:]) 
		except:return ()	
getDictNestedValue=getNestedValue
def getLastException():
	'''a callable
	return Exception'''
	import traceback as tb
	r=tb.extract_tb( sys.last_traceback)
	r.append(sys.last_value)
	return r
	
	if py.callable(a):
		try:a()
		except Exception as e:return e
		return 'No Exception found'
	else:
		return	getException.__doc__
lastErr=err=geterr=getErr=error=getException=getLastException

def print_tb():
	import traceback
	ex_type, ex, tb_obj = sys.exc_info()
	traceback.print_tb(tb_obj)

def getClassHierarchy(obj):
	'''In [68]: inspect.getmro?
Signature: inspect.getmro(cls)
Docstring: Return tuple of base classes (including cls) in method resolution order.
File:      g:\qgb\anaconda2\lib\inspect.py
Type:      function
'''
	import inspect
	if py.getattr(obj,'__base__',None) or py.getattr(obj,'__mor__',None):
		return inspect.getmro(obj)

	if py.getattr(obj,'__class__',None):
		return inspect.getmro(obj.__class__)
	return ()
getclassInherit=getClassHierarchy

def getFile(a):
	import inspect
	try:
		inspect.getfile(a)
	except Exception as e:
		if 'is not a module' in e.message:
			return getFile(py.type(a))
		if 'built-in' in e.message:
			return e.message
getfile=getFile

#def 	#把一个数分解成2的次方之和。

def selectBox(*a):
	if py.is2():
		import Tkinter as tk
	else:
		import tkinter as tk
	top=tk.Tk()
	tk.mainloop()

def getCmd():
	if iswin() or iscyg():
		return Win.getCmd()
getCmdline=getCmd

def save(a,name=0):
	global gst;gst='g:/qgb/'
	return F.write(name,a)
	# if name:
	# else:#TODO 写入一个新文件并保证 别进程 load 可以读到最新的save；可以保存到网络？？
def load(name=0,returnFile=False):
	global gst;gst='g:/qgb/'
	return F.read(name,returnFile=returnFile)
	# if name:#TODO 配合 save 并正确转换到相应类型，使用对象序列化？ 

	
def	renameDictKey(d,new,old={}):
	if not old:
		for i in d:
			old=i
			break
	if isinstance(d, OrderedDict):
		d.rename(old,new)
	else:
		d[new] = d.pop(old)
	return d
		# del d[old]#这个可以删除item,py27
def beep(ms=1000,hz=2357):
	if iswin():
		try:
			import winsound
			return winsound.Beep(hz,ms)
		except:
			pass
	p('\a')

def unique(iterable):
	r=[]
	for i in iterable:
		if i not in r:r.append(i)
	return r

def main(display=True,pressKey=False,clipboard=False,escape=False,c=False,ipyOut=False,cmdPos=False,reload=False,*args):
	anames=py.tuple([i for i in py.dir() if not i .startswith('args')])
	if not args:args=sys.argv
	for i in args:
		for j in anames:
			if i.lower().startswith(j.lower()+'='):
				# args.remove(i)
				i=T.sub(i,'=','').lower()
				if i.startswith('t'):exec(j+'=True' )#only for python2?
				if i.startswith('f'):exec(j+'=False')
				# repl()
	###############################
	'''call order Do Not Change! '''
	###############################
	sImport=gsImport
	if c:sImport+=';C=c=U.clear'
	
	if reload:sImport+=";R=r=U.reload"
		
	if ipyOut:sImport+=';O=o=U.ipyOutLast'
	
	if cmdPos:sImport+=";POS=pos=U.cmdPos;npp=NPP=U.notePadPlus;ULS=Uls=uls=F.ls;ll=ULL=Ull=ull=F.ll"
		
	if escape:sImport=sImport.replace("'",r"\'")
	
	if display:pln(sImport)
	
	if pressKey:
		try:
			import win32api
			win32api.ShellExecute(0, 'open', gsw+'exe/key.exe', sImport+'\n','',0)
		except:pln('PressKey err')
	if clipboard:
		try:
			Clipboard.set(sImport)
		except:pln('Clipboard err')
	
	return sImport
gsImport='''import sys;'qgb.U' in sys.modules or sys.path.append('{0}');from qgb import *'''.format(getModPathForImport())	
if __name__ == '__main__':
	main()
