import sys
if __name__.endswith('qgb.N.Backend.taobao_list'):from ... import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U,T,N,F=py.importUTNF()
gdshop_dui=gtb_list=U.set(__name__,  U.get(__name__,{})  )
gn=__name__+'.'
get_set=lambda a,default='':U.set(gn+a,  U.get(gn+a,default)  )
gshop=get_set('shop','')

grows=[]
# g=get_set('')

from urllib.parse import parse_qs

def init(shop):
	global gshop
	shop=shop.lower()
	if '.taobao.com' in shop:
		shop=T.netloc(shop).replace('.taobao.com','')
	if shop not in gtb_list:
		gtb_list[shop]={}
	gshop=U.set(gn+'shop',shop)
	return gshop

gdu_pageNo_null=get_set('pageNo_null',{})
def recycle_pageNo_null_url():
	for shop,dui in gdshop_dui.items():
		for u in list(dui):
			if 'pageNo=' not in u:
				gdu_pageNo_null[u]=dui.pop(u)
				U.pln('recycled:',shop,u)
remove_pageNo_null_url=pop_pageNo_null_url=recycle_pageNo_null_url

def pop_item_url_from_id_list(a):
	if not a:return ''
	id=''
	if py.isdict(a):
		id,v=a.popitem()
	if py.islist(a):
		id=a.pop() #-1
	if not id:return ''
	if 'id=' not in id:
		return 'https://item.taobao.com/item.htm?id='+id
	else:
		return 'https://item.taobao.com/item.htm?id='+T.sub(id,'id=','')
get_item_url=pop_item_url=pop_item_url_from_id_list

def pop_url_from_shop(url,shop=None):
	if not shop:shop=gshop
	

def insert(request):
	''' [href,items,new Date(),  ,...]
	'''
	href,items,*_ = T.json_loads(request.get_data())
	gtb_list[gshop][href]=items
	return len(gtb_list[gshop] )
	
def include(u):
	getn=lambda url:parse_qs(url).get('pageNo',[0])[0]
	n=getn(u)
	for url in gtb_list[gshop]:
		if n==getn(url):
			return True
	return False
	
def max_num():
	mi=[1]
	for url in gtb_list[gshop]:
		if 'pageNo=' not in url:
			U.beep()
			U.pln(gshop,'no pageNo:',url)
			continue
		i=int(parse_qs(url).get('pageNo')[0] )
		mi.append(i)
	return max(mi)

def iter_items(shop=None):
	if not shop:shop=gshop
	for url in py.list(gtb_list[shop]):
		page=gtb_list[shop][url]
		yield from page


def iter_sprice(shop=None):
	if not shop:shop=gshop
	for i in iter_items(shop):
		if('class="s-price"' in i):
			yield i
			
def rty(rows=None,**ka):
	if not rows:rows=grows
	rt=''
	for index,row in enumerate(U.sort(rows,**ka)):
		if 'item.taobao.com/item.htm?id=' in row[-3]:
			row[-3]=T.sub(row[-3],'id=','')
		tb=f'''{row[-1]}
<span>{row[:4]}</span>  <br>
<a target="_blank" href="taobao://item.taobao.com/item.htm?id={row[-3]}">{'%4s'%index}  {row[-2]} </a>
<br><hr>
'''
		rt+=tb
	return rt

imgs=[];dis=[];ts=[];ds={}

def result(shop=None):
	global grows
	if not shop:shop=gshop
	rows=py.set()
	for html in U.progressbar( iter_items(shop) ):
		bs = T.BeautifulSoup(html)
		a=bs.select('.item-name')[0]
		h=a.get('href')
# '//item.taobao.com/item.htm?spm=a1z10.3-c.w4002-21992529001.30.1887510dqsrC5C&id=597761481418'		
		if not h.startswith('//item.taobao.com/item.htm?') or 'id=' not in h:
			U.pln('not correct taobao item href',U.stime())
			py.pdb()
		id=T.get_url_arg(h,'id')
		cp=bs.select('[class=c-price]')[0]
		cp=float(cp.text)
		sp=bs.select('[class=s-price]')
		if sp:
			sp=sp[0]
			sp=float(sp.text)
		else:
			sp=cp
		img=bs.select('img')[0]
		row=[int((sp-cp)*100)/100,cp,sp, id, T.replacey(a.text.strip() ,['【优信电子】',],''),img ]
		row.insert(0,int( (row[0]/row[1])* 100 ) )
		row=tuple(row)
		rows.add(row)
	grows=rows
	return F.dill_dump(obj=rows,file='{}-{}'.format(shop,len(rows)))