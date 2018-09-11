# coding=utf-8
import os as _os;import sys as _sys;from os import path as _p
if __name__.endswith('qgb.F'):from . import py,T
else:import py,T
gError=[]
def setErr(ae):
	global gError
	py.importU()
	if U.gbLogErr:# U.
		if type(gError) is list:gError.append(ae)
		elif gError:gError=[gError,ae]
		else:gError=[ae]
	else:
		gError=ae
	if U.gbPrintErr:U.pln('#Error ',ae)
	
def copy(src,dst):
	r''' src : sFilePath , list ,or \n strs
dst:sPath
	'''
	from shutil import copy as _copy
	if not py.istr(dst):raise py.ArgumentError('dst must be str')
	if py.istr(src):
		if '\n' in src:
			src=src.splitlines()
			return copy(src,dst)
		return _copy(src,dst)
	if py.iterable(src):
		fns=[]
		for i in src:
			fn=getName(i)
			if fn in fns:
				fn=T.fileName(i)
			fns.append(fn)
			_copy(i,getPath(dst)+fn)
		return fns
def modPathInSys(mod=None):
	if mod:
		if not py.istr(mod):mod=mod.__file__
	else:mod=__file__
	
	mod=mod.replace('\\','/')
	inPath=False
	if os.path.isabs(mod):
		for i in sys.path:
			i=i.replace('\\','/')
			if i and mod.startswith(i):
				if not i.endswith('/'):i+='/'
				i+='qgb'
				if mod.startswith(i):inPath=True
	else:
		raise NotImplementedError('__file__ not abs')
	return inPath
def lineCount(a):
	def blocks(files, size=65536):
		while True:
			b = files.read(size)
			if not b: break
			yield b

	with open(a, "r") as f:
		return sum(bl.count("\n") for bl in blocks(f))
		
def getPath(asp):
	asp=asp.replace('\\','/')
	if asp.endswith('/'):return asp
	else:
		if isDir(asp):return asp+'/'
		else:
			# _p.dirname('.../qgb/')# 'G:/QGB/babun/cygwin/lib/python2.7/qgb'
			# _p.dirname('.../qgb')# 'G:/QGB/babun/cygwin/lib/python2.7'
			return _p.dirname(asp)+'/'
def getPaths(a):
	r''' a:str 
	'''
	py.importU()
	if U.iswin():
		sp=a.replace('\\','/').split('/')
		rlist=[]
		def append(r):
			if r and r not in rlist:rlist.append(r)
		r=''
		for i,v in enumerate(sp):
			if len(v)>1 and v[-2] in T.AZ and v[-1]==':':
				append(r)
				r=v[-2:]+'/'
				continue

			for j in v:
				if j not in T.PATH_NAME:
					append(r)
					r=''
					continue

			if r and v:
				if isdir(r+v):r=r+v+'/'
				else:
					append(r)
					r=''
					continue
		return rlist
	else:
		raise NotImplementedError('*nux')
	
def getNameFromPath(a):
	''' if a.endswith('/'):return ''
	'''
	a=a.replace('\\','/')
	if '/' not in a:return a
	else:
		# import T
		return T.subr(a,'/','')
filename=fileName=getname=getName=name=getNameFromPath
		
def getNameWithoutExt(a):
	''' see getNameFromPath
	'''
	
	a=getNameFromPath(a)
	if '.' in a:
		return T.subr(a,'','.')
	else:return a

	
def autof(head,ext='',r='Default auto accroding to the head'):
	'''r :recursion
	return str  
	# TODO # ext=?ext*     '''
	if not py.type(ext)==py.type(head)==py.str or head=='':
		return ''
	
	if len(ext)>0 and not ext.startswith('.'):ext='.'+ext
	head=head.lower();ext=ext.lower()
	head=head.replace('\\','/')
	if '/' in head:
		if py.type(r) is py.str:
			r=True
		else:
			r=False
	
	ap='.'
	if _p.isabs(head):
		ap=dir(head)
		if not isExist(ap):
			if head.endswith(ext):return head
			else:return head+ext
	
	# import F
	ls=[i.lower() for i in list(ap,r=r)]
	if head+ext in ls:return head+ext
	# import U
	# U.pprint(ls)
	for i in ls:		
		if i.startswith(head) and i.endswith(ext):return i
	
	for i in ls:
		if head in i and ext in i:return i
		
	# if inMuti(ext,'*?'):ext=ext.replace('*')
	
	if not head.endswith(ext):head+=ext
	
	return head
autoFileName=autof
		
def new(a):
	'''will overwrite'''
	try:
		f=open(a,'w')
		f.write('')
		f.close()
		return f.name
	except Exception as e:
		setErr(e)
		return False
def isDir(ast):
	'''#TODO:
	
	'''	
	if not py.istr(ast):ast=py.str(ast)
	if not ast:return False
	ast=ast.replace('\\','/')
	if exist(ast):
		return _p.isdir(ast)
	else:
		if ast.endswith('/'):return True
		else:                return False
isPath=isdir=isDir
	# if not ast.replace('.','').strip():return True # （不是 点和空格 返回 T） 
	# return ('/' in ast) or ('\\' in ast)
	# return _p.sep in ast
# def is	
def intToBytes(a):
	import T
	a=T.intToStr(a)
	return hexToBytes(a)
i2b=intToBytes

def bytesToHex(a,split=''):
	r=''
	for i in a:
		r+=DIH[ord(i)]+split
	return r
b2h=bytesToHex
	
def hexToBytes(a,split=''):
	it=2
	if len(split)>0:it+=len(split)
	if it==2 and len(a) % it!=0:return ()
	
	a=a.upper();r=''
	
	if it>2:
		a=a.split(split)
		if len(a[-1]) == 0:a=a[:-1]
		for i in a:
			r+=chr(DHI[ i ])
		return r
		
	for i in xrange(len(a)/2):
		r+=chr(DHI[a[i*2:i*2+2]])
	return r
h2b=hexToBytes

def writeIterable(file,data,end='\n',overwrite=True):
	if overwrite:new(file)	
	f=open(file,'a')
	for i in data:
		f.write(py.str(i)+end)

def write(file,data,mod='w',mkdir=False,autoArgs=True):
	py.importU()
	try:
		if autoArgs:
			if py.istr(data) and py.len(file)>py.len(data)>0:				
				if '.' in data and '.' not in file   and  isFileName(data):
					file,data=data,file
					U.warring('F.write fn,data but seems data,fn auto corrected（v 纠正')
	except:pass		
	
	# try:
	file=autoPath(file)
	if mkdir:makeDirs(file,isFile=True)
	if py.is3() and isinstance(data,py.bytes) and 'b' not in mod:
		mod+='b'
		
	with open(file,mod) as f:
		if py.istr(data) or (py.is3() and isinstance(data,py.bytes) )	:
			f.write(data)
		elif py.is2() and type(data) is py.unicode:
			f.write(data.encode(U.encoding))
		else:
			# if py.is2():print >>f,data
			# else:
			U.pln(data,file=f)
		return f.name
	# except Exception as e:
		# setErr(e)
		# return False

def append(file,data):
	'''builtin afile.write() No breakLine'''
	write(file,data,mod='a')
	
def detectEncoding(file,confidence=0.7,default=''):
	if py.istr(file):
		file=open(file,'rb')
	if py.isfile(file):
		r=T.detect(file.read())
		if r['confidence']>confidence:return r['encoding']
		else:
			if default:return default
			raise Exception(
			'{0} encoding {1} confidence {2} less then {3}'.format(
			file,r['encoding'],r['confidence'],confidence)  )
	else:raise py.ArgumentError('need str or file')
detect=detectEncoding
	
def read(file,mod='r',returnFile=False,encoding=''):
	'''if returnFile:
			return content,f.name
			'''
	# try:
	file=autoPath(file)
	if py.is2():f=open(file,mod)
	else:
		encoding=encoding or detectEncoding(file,confidence=0.9,default='utf-8')
		#utf-8 /site-packages/astropy/coordinates/builtin_frames/__init__.py  {'confidence': 0.73, 'encoding': 'Windows-1252'
		f=open(file,mod,encoding=encoding)
	s=f.read()
	f.close()
	if returnFile:
		return s,f.name
	else:
		return s
	# except Exception as e:
		# return f,e
		# if 'f' in py.dir() and f:f.close()
		# return ()
def readBytes(file):
	'''is2 rb return str'''
	file=autoPath(file)
	return open(file,'rb').read()
	
def readJSON(file):
	''' '''
	import json
	file=autoPath(file)
	file=open(file)
	return json.load(file)
	
def isDir(file):
	return _p.isdir(file)
isFolder=isdir=isDir
	
def exist(fn,zero=False):
	''': path.exist('c:')
Out[57]: False

In [58]: path.exist('o:')#这是因为当前目录下存在 'o:'，但是只能用ls完整查看
Out[58]: True
## 在cygwin中 只能判断 c:\ 或 c:/ ,单独 c: 总为False
#############
>>> path.exists('c:')
True
>>> path.exists('o:')
True
'''
	py.importU()
	if U.iscyg():
		if len(fn)==2 and fn[-1]==':':fn+='/'
		# raise NotImplementedError
	if _p.exists(fn):
		if _p.isdir(fn):return True
		if _p.getsize(fn)<1 and not zero:
			return False
		return True
	else:
		return False
isExist=exists=exist

def walk(top):
	'''2&3 : os.walk(top, topdown=True, onerror=None, followlinks=False)
	'''
	if py.is2():
		return _os.walk(top).next()
	else:
		return _os.walk(top).__next__()
		
def list(ap='.',type='',t='',r=False,d=False,dir=False,f=False,file=False):
	'''Parms:bool r recursion
			 str (type,t) '(d,f,a,r)'
	default return all'''
	py.importU()
	if dir:d=True
	if file:f=True
	if t and not type:type=t
	
	if 'd' in type:d=True
	if 'f' in type:f=True
	if 'a' in type:d=True;f=True
	if 'r' in type:r=True
	
	if d or dir or f or file:pass
	else:d=f=True		#default return all
	
	if not py.istr(ap) or py.len(ap)<1:
		setErr('F.list arguments ap error')
		ap='.'
	# if len(ap)==2 and ap.endswith(':'):ap+='/'	
	ap=ap.replace('\\','/')
	if not ap.endswith('/'):#U.inMuti(ap,'/','\\',f=str.endswith):
		if isDir(ap):
			ap+='/'
		else:
			return [abs(ap)]
		# if not ap.endswith('/'):ap+='/'
		# else:ap+='\\'
	
	# U.repl()
	########## below r is result
	rls=[]
	try:r3=py.list(walk(ap))
	except Exception as ew:
		# pln ap;raise ew
		return []
	
	if ap=='./':ap=''
	# U.repl()
	r3[1]=[ap+i for i in r3[1]]
	r3[2]=[ap+i for i in r3[2]]
	
	
	if d:rls.extend(r3[1])
 
	# 
	if r:
		for i in r3[1]:rls.extend(list(i,r=r,d=d,f=f))
			
	if f:rls.extend(r3[2])
	
	return rls
	# else:return r3[1]+r3[2]
ls=list

def ll(ap='.',readable=True,type='',t='',r=False,d=False,dir=False,f=False,file=False):
	'''return {file : [size,atime,mtime,ctime,st_mode]}
	readable is True: Size,Stime,..
	linux struct stat: http://pubs.opengroup.org/onlinepubs/009695399/basedefs/sys/stat.h.html'''
	dr={}
	for i in list(ap,type=type,t=t,r=r,d=d,dir=dir,f=f,file=file):#ls 肯定返回 list类型！
		# importU;if U.DEBUG:U.pln ap,repr(i)
		s=_os.stat(i)
		dr[i]=[size(i),s.st_atime,s.st_mtime,s.st_ctime,s.st_mode]
		if readable:
			py.importU()
			for j in py.range(len(dr[i])):
				# U.pln i,j,repr(dr[i][j])
				if py.type(dr[i][j]) is py.float:dr[i][j]=U.stime(time=dr[i][j])
				if py.type(dr[i][j]) is py.long:dr[i][j]=readableSize(dr[i][j])
	return dr

SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
			1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}
def numToSize(size, b1024=True):
	'''Convert a file size to human-readable form.
	Keyword arguments:
	size -- file size in bytes
	b1024 -- if True (default), use multiples of 1024
	if False, use multiples of 1000
	Returns: string
	test git
	'''
	if size < 0:
		return size
		# raise ValueError('number must be non-negative')

	multiple = 1024.0 if b1024 else 1000.0 #another if statement style
	
	if size<=multiple:return py.str(size)+' B'
	
	for suffix in SUFFIXES[multiple]:
		size /= multiple
		if size < multiple:
			return '{0:.3f} {1}'.format(size, suffix)
	raise ValueError('number too large')
readableSize=numToSize
def size(asf): 
	'''file or path return byte count
	not exist return -1'''
	size =0 #0L  SyntaxError in 3
	if not _p.exists(asf):
		return -1#-1L
	if not _p.isdir(asf):
		size= _p.getsize(asf)
		if size<=0:
			try:size=len(read(asf))
			except:return -1#-1L
		return size
	for root, dirs, files in _os.walk(asf):  
		size += sum([_p.getsize(_p.join(root, name)) for name in files])  	
	return size 
	
# U.pln size(U.gst)
# exit()
	
def csvAsList(fn):
	import csv
	with open(fn, 'rb') as f:
		reader = csv.reader(f)
		return py.list(reader)
		
def getSourcePath():
	f=_sys._getframe().f_back
	def back(af,ai=0):
		if af is None:return ''
		if '__file__' in af.f_globals:return af.f_globals['__file__']
		else:return back(af.f_back,ai+1)
		
	return back(f)
	
	# U.pln globals().keys()
	# U.pln __file__, __name__ , __package__
	
def delFile(file):
	file=autoPath(file)
	sp=getSplitor(file)
	# for i in a.split(ap):
	py.importU()
	def Error():
		if U.iswin():
			return WindowsError
	
	
	try:
		_os.remove(file)
		return True
	except Error():
		if isDir(file):
			U.pln('#TODO')
	#Error  {'G:\\test\\npp': WindowsError(5, '')}
	# Docstring: MS-Windows OS system call failed.  
	#*nix NameError: name 'WindowsError' is not defined  '''
	except Exception as e:
		setErr({file:e})
		return False
	
rm=delete=delFile
	
def getSplitor(ap):
	if '/' in ap:return '/'
	if '\\' in ap:return '\\'		
	return '/'#default	
getsp=getSp=getSplitor		
		
		
def makeDirs(ap,isFile=False):
	py.importU()
	ap=autoPath(ap)
	sp=getSplitor(ap)
	ap=ap.split(sp)
	if isFile:ap=ap[:-1]
	# if not isabs(ap):
		# if not ap.startswith('.'):
			# if ap.startswith(sp):ap=U.gst[:-1]+ap
			# else:ap=U.gst+ap
	# else:
	base=''
	
	for i in ap:
		base+=(i+sp)
		if exist(base):continue
		else:
			try:
				_os.mkdir(base)
			
			except Exception as e:
				if U.iswin():
					if e.winerror==5:continue#WindowsError(5, '') 拒绝访问
					if e.winerror==183:continue#WindowsError 183 当文件已存在时，无法创建该文件。
				
				if 'exists' in e.args[1]:#(17, 'File exists') cygwin;
					continue
				# U.repl(printCount=True)
				setErr(e)
				return False
	return True	
	
	# if U.iswin():
		
		# _os.system('md "{0}"'.format(ap))
md=mkdir=makeDirs		

gbAutoPath=True
def autoPath(fn,default=''):
	''' default is U.gst
if fn.startswith("."): 如果路径中所有文件夹存在，则可以写入读取。否则无法写入读取。file io 都是这个规则吧
FileNotFoundError: [Errno 2] No such file or directory: '.

	'''
	if not gbAutoPath:return fn
	if default:
		default=default.replace('\\','/')
		if not default.endswith('/'):default+='/'
	else:
		py.importU()
		default=U.gst
	fn=str(fn)
	fn=fn.replace('\\','/')
	if fn.startswith("."):
		return fn;
	if fn.startswith("~/"):
		import os
		if U.isnix():
			home=os.getenv('HOME')
		else:
			home=os.getenv('USERPROFILE')# 'C:/Users/Administrator'  not  cyg home os.getenv('HOME')
		# else:		home=os.getenv('HOMEPATH')#  HOMEPATH=\Users\Administrator
		return home+fn[1:];
	
	if isAbs(fn):
		return fn
	else:
		# if _p.exists(fn):return abs(fn)
		while fn.startswith('/'):fn=fn[1:]
		return (default + fn);
def abs(file):
	return _p.abspath(file)
		
def isAbs(file):
	'''in cygwin:
In [43]: U.path.isabs( 'M:/Program Files/.babun/cygwin/lib/python2.7/qgb/file/attr.html')
Out[43]: False

In [45]: U.path	.isabs('M:\\Program Files\\.babun\\cygwin\\lib\\python2.7\\qgb\\file\\attr.html' )
Out[45]: False
##### win py3.6    fixed
--------> F.isabs('2d:\1\2')# False
--------> F.isabs('d:\1\2')# False
--------> F.isabs('/babun/cygwin/lib/python2.7\\qgb\\F.py')# True
#TODO 更加精细判断，文件名不合法 return None?
'''	
	py.importU()
	if U.iscyg() or U.iswin():
		if ':' in file:return True
		else:return False
	return _p.isabs(file)
isabs=isAbs
		
def name(a):
	'''Anti abs
	得到 单独文件（夹）名字
	'''
	py.importU()
	if not U.T.istr(a):return ''
	if U.inMuti(a,'/','\\',f=str.endswith):a=a[:-1]
	if not isAbs(a):return a
	else:
		
		a=T.sub(a,dir(a))
		# U.repl()
		if U.inMuti(a,'/','\\',f=str.startswith):return a[1:]
		else:return a
		
def dir(a):
	#TODO a 为文件夹 应该直接返回
	return _p.dirname(a)
	# exit()

def readlines(a):
	r=[]
	for i in py.open(autoPath(a)):r.append(i)
	return r
# F.isFileName('g:/a')
# []
def isFileName(a):
	'''a:str'''
	# from . import U #ValueError: Attempted relative import in non-package
	py.importU()
	for i in a:
		if i not in T.PATH_NAME:return py.No(i,a)
		
	return a
	

DIH=DINT_HEX=INT_HEX={0:'00',1:'01',2:'02',3:'03',4:'04',5:'05',6:'06',7:'07',8:'08',9:'09',10:'0A',11:'0B',12:'0C',13:'0D',14:'0E',15:'0F',16:'10',17:'11',18:'12',19:'13',20:'14',21:'15',22:'16',23:'17',24:'18',25:'19',26:'1A',27:'1B',28:'1C',29:'1D',30:'1E',31:'1F',32:'20',33:'21',34:'22',35:'23',36:'24',37:'25',38:'26',39:'27',40:'28',41:'29',42:'2A',43:'2B',44:'2C',45:'2D',46:'2E',47:'2F',48:'30',49:'31',50:'32',51:'33',52:'34',53:'35',54:'36',55:'37',56:'38',57:'39',58:'3A',59:'3B',60:'3C',61:'3D',62:'3E',63:'3F',64:'40',65:'41',66:'42',67:'43',68:'44',69:'45',70:'46',71:'47',72:'48',73:'49',74:'4A',75:'4B',76:'4C',77:'4D',78:'4E',79:'4F',80:'50',81:'51',82:'52',83:'53',84:'54',85:'55',86:'56',87:'57',88:'58',89:'59',90:'5A',91:'5B',92:'5C',93:'5D',94:'5E',95:'5F',96:'60',97:'61',98:'62',99:'63',100:'64',101:'65',102:'66',103:'67',104:'68',105:'69',106:'6A',107:'6B',108:'6C',109:'6D',110:'6E',111:'6F',112:'70',113:'71',114:'72',115:'73',116:'74',117:'75',118:'76',119:'77',120:'78',121:'79',122:'7A',123:'7B',124:'7C',125:'7D',126:'7E',127:'7F',128:'80',129:'81',130:'82',131:'83',132:'84',133:'85',134:'86',135:'87',136:'88',137:'89',138:'8A',139:'8B',140:'8C',141:'8D',142:'8E',143:'8F',144:'90',145:'91',146:'92',147:'93',148:'94',149:'95',150:'96',151:'97',152:'98',153:'99',154:'9A',155:'9B',156:'9C',157:'9D',158:'9E',159:'9F',160:'A0',161:'A1',162:'A2',163:'A3',164:'A4',165:'A5',166:'A6',167:'A7',168:'A8',169:'A9',170:'AA',171:'AB',172:'AC',173:'AD',174:'AE',175:'AF',176:'B0',177:'B1',178:'B2',179:'B3',180:'B4',181:'B5',182:'B6',183:'B7',184:'B8',185:'B9',186:'BA',187:'BB',188:'BC',189:'BD',190:'BE',191:'BF',192:'C0',193:'C1',194:'C2',195:'C3',196:'C4',197:'C5',198:'C6',199:'C7',200:'C8',201:'C9',202:'CA',203:'CB',204:'CC',205:'CD',206:'CE',207:'CF',208:'D0',209:'D1',210:'D2',211:'D3',212:'D4',213:'D5',214:'D6',215:'D7',216:'D8',217:'D9',218:'DA',219:'DB',220:'DC',221:'DD',222:'DE',223:'DF',224:'E0',225:'E1',226:'E2',227:'E3',228:'E4',229:'E5',230:'E6',231:'E7',232:'E8',233:'E9',234:'EA',235:'EB',236:'EC',237:'ED',238:'EE',239:'EF',240:'F0',241:'F1',242:'F2',243:'F3',244:'F4',245:'F5',246:'F6',247:'F7',248:'F8',249:'F9',250:'FA',251:'FB',252:'FC',253:'FD',254:'FE',255:'FF'}
DHI=DHEX_INT=HEX_INT={y:x for x,y in DIH.items()}




if __name__=='__main__':
	import T,U
	# l=csvAsList('process.csv')
	# U.shtml(l)
	# U.pln getSourcePath()
	# U.repl()
	exit()	
	r=hexToBytes(T.HEX.lower())
	# U.write('h.r',r)
	