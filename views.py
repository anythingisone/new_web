from django.core.paginator import Paginator

from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

from myweb.models import Types,Users,Goods,Orders,Detail
from datetime import datetime

import time,os

#商品类别函数
def basetypes(request):
	context = {}
	context['typelist'] = Types.objects.filter(pid=0)
	return context

# 商品首页
def index(request):
	context = basetypes(request)
	request.session['path']=request.path
	return render(request,'myweb/meizu/index.html',context)

#商品列表
def myweblist(request,tid):
	request.session['path']=request.path
	# 获取点击类别
	stype = Types.objects.get(id=tid)
	# 判断是否为根类别
	if stype.pid == 0:
		#保存当前根类别id
		request.session['aid']=tid
		context = basetypes(request)
		# 获取根类别子类别
		stypelist = Types.objects.filter(pid=tid)
		context['goodslist'] = Goods.objects.filter(typeid__in=Types.objects.only('id').filter(path__contains=','+str(tid)+','))
		context['stypelist'] = stypelist
	else:
		context = basetypes(request)
		# 获取同级类别
		stypelist = Types.objects.filter(pid=stype.pid)
		goodslist = Goods.objects.filter(typeid=tid)
		context['stypelist'] = stypelist
		context['goodslist'] = goodslist
	return render(request,'myweb/meizu/list.html',context)

#商品详情
def detail(request,gid):
	request.session['path']=request.path
	context = basetypes(request)
	ob = Goods.objects.get(id=gid)
	ob.clicknum+=1
	ob.save()
	context['goods']=ob
	return render(request,'myweb/meizu/meilanx.html',context)

# 用户登录
def login(request):
	return render(request,'myweb/meizu/login.html')

# 用户名ajax验证
def usernameyz(request):
	username = request.GET['username']
	user = Users.objects.all()
	falg = '1'
	for i in user:
		if username == i.username:
			falg = '0'
			break
	return JsonResponse({'falg':falg})
# 验证码
def verify(request):
	#引入随机函数模块
	import random
	from PIL import Image, ImageDraw, ImageFont
	#定义变量，用于画面的背景色、宽、高
	#bgcolor = (random.randrange(20, 100), random.randrange(
	#    20, 100),100)
	bgcolor = (242,164,247)
	width = 100
	height = 25
	#创建画面对象
	im = Image.new('RGB', (width, height), bgcolor)
	#创建画笔对象
	draw = ImageDraw.Draw(im)
	#调用画笔的point()函数绘制噪点
	for i in range(0, 100):
	    xy = (random.randrange(0, width), random.randrange(0, height))
	    fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
	    draw.point(xy, fill=fill)
	#定义验证码的备选值
	str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
	#随机选取4个值作为验证码
	rand_str = ''
	for i in range(0, 4):
	    rand_str += str1[random.randrange(0, len(str1))]
	#构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
	font = ImageFont.truetype('static/FZSTK.TTF', 21)
	#font = ImageFont.load_default().font
	#构造字体颜色
	fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
	#绘制4个字
	draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
	draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
	draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
	draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
	#释放画笔
	del draw
	#存入session，用于做进一步验证
	request.session['verifycode'] = rand_str
	"""
	python2的为
	# 内存文件操作
	import cStringIO
	buf = cStringIO.StringIO()
	"""
	# 内存文件操作-->此方法为python3的
	import io
	buf = io.BytesIO()
	#将图片保存在内存中，文件类型为png
	im.save(buf, 'png')
	#将内存中的图片数据返回给客户端，MIME类型为图片png
	return HttpResponse(buf.getvalue(), 'image/png')

# 用户检验
def yz(request):
	# 校验验证码
	verifycode = request.session['verifycode']
	code = request.POST['code']

	if verifycode != code:
		context = {'info':'验证码错误！'}
		return render(request,"myweb/meizu/login.html",context)
	try:
		ob = Users.objects.get(username=request.POST['username'])
		if ob.password == request.POST['password']:
			if ob.state == 2:
				context = {'info':'你是被禁用的!'}
				return render(request,'myweb/meizu/login.html',context)
			else:
				context = {}
				context['typelist'] = Types.objects.filter(pid=0)
				request.session['username']=ob.username
				request.session['id']=ob.id
				return redirect(request.session['path'])
		else:
			context = {'info':'用户名或密码错误!'}
			return render(request,'myweb/meizu/login.html',context)
	except:
		context = {'info':'用户名或密码错误!'}
		return render(request,'myweb/meizu/login.html',context)

# 用户退出
def loginout(request):
	context = {}
	context['typelist'] = Types.objects.filter(pid=0)
	try:
		del request.session['username']
		return redirect(request.session['path'])
	except:
		return redirect(request.session['path'])

# 用户注册
def useradd(request):
	context = {'info':''}
	return render(request,'myweb/meizu/register.html',context)

# 执行添加用户
def userinsert(request):
	try:
		ob = Users()
		ob.username = request.POST['username']
		ob.password = request.POST['password']
		ob.name = request.POST['name']
		ob.email = request.POST['email']
		ob.save()
		context = {'info':'注册成功!'}
	except:
		context = {'info':'注册失败!'}
	return render(request,'myweb/meizu/register.html',context)

# 购物车
def cart(request,gid):
	#request.session['path']='/myweb/tocart'
	#获取要放入购物车中的商品信息
	context = basetypes(request)
	goods = Goods.objects.get(id=gid)
	shop = {'id':goods.id,'goods':goods.goods,'price':goods.price,'picname':goods.picname,'num':int(request.POST['num']),'descr':goods.descr,'path':request.session['path'],'allprice':goods.price,'store':goods.store}
	#从session获取购物车信息
	if 'shoplist' in request.session:
		shoplist = request.session['shoplist']
	else:
		shoplist = {}

	#判断此商品是否在购物车中
	if gid in shoplist:
		#商品数量加
		# 判断是否超出库存
		if shoplist[gid]['num']+shop['num']>=goods.store:
			shoplist[gid]['num'] = goods.store
		else:
			shoplist[gid]['num']+=shop['num']
		shoplist[gid]['allprice']=shoplist[gid]['num']*int(shoplist[gid]['price'])
	else:
		#新商品添加
		shoplist[gid]=shop
		shoplist[gid]['allprice']=shoplist[gid]['num']*int(shoplist[gid]['price'])
	#将购物车信息放回到session
	request.session['shoplist'] = shoplist
	return render(request,'myweb/meizu/cart.html',context)
	# context = basetypes(request)
	# goods = Goods.objects.get(id = request.POST['gid'])
	# try:
	# 	# 获取商品信息
		
	# 	if str(goods.id) in request.session['shoplist']:
	# 		goodslist[str(goods.id)]['num'] += int(request.POST['num'])
	# 	else:
	# 		goodslist[str(goods.id)]={'id':goods.id,'goods':goods.goods,'price':goods.price,'picname':goods.picname,'num':int(request.POST['num'])}
	# 	request.session['shoplist'] = goodslist
	# except:
	# 	request.session['shoplist'] = {}
	# 	goodslist = {}
	# 	goodslist[str(goods.id)]={'id':goods.id,'goods':goods.goods,'price':goods.price,'picname':goods.picname,'num':int(request.POST['num'])}
	# 	request.session['shoplist'] = goodslist
	# return render(request,'myweb/meizu/cart.html',context)
#购物车修改
# def cartchange(request):
# 	context = basetypes(request)
# 	num = int(request.GET.get('num'))
# 	if num<=1:
# 		num = 1
# 	request.session['shoplist'][request.GET.get('sid')]['num']=num
# 	return render(request,'myweb/meizu/cart.html',context)

# 数量修改
def numchange(request):
	goodslist = request.session['shoplist']
	gid = request.GET['gid']
	num = int(request.GET['num'])
	flag = request.GET['flag']
	if flag == 'input':
		if num>=Goods.objects.get(id = gid).store:
			goodslist[gid]['num'] = Goods.objects.get(id = gid).store
		else:
			goodslist[gid]['num'] = num
		goodslist[gid]['allprice'] = goodslist[gid]['num']*int(goodslist[gid]['price'])
	elif flag == 'add':
		if goodslist[gid]['num']>=Goods.objects.get(id = gid).store:
			pass
		else:
			goodslist[gid]['num'] = num + 1
			goodslist[gid]['allprice'] = goodslist[gid]['num']*int(goodslist[gid]['price'])
	elif num <= 1:
		goodslist[gid]['num'] = 1
	else:
		goodslist[gid]['num'] = num - 1
		goodslist[gid]['allprice'] = goodslist[gid]['num']*int(goodslist[gid]['price'])
	request.session['shoplist'] = goodslist
	return JsonResponse({'num':goodslist[gid]['num'],'price':goodslist[gid]['price']})

#删除购物车
def delcart(request):
	gid = request.GET['gid']
	shoplist = request.session['shoplist']
	shoplist.pop(gid)
	request.session['shoplist'] = shoplist
	return JsonResponse({})

#跳转购物车
def tocart(request):
	request.session['path']=request.path
	context = basetypes(request)
	return render(request,'myweb/meizu/cart.html',context)

# 订单
def orders(request):
	return JsonResponse({})
# 订单
def order(request):
	user = Users.objects.get(id = request.session['id'])
	try:
		shopid = request.GET['shopid']
		shopid = shopid.split(',')
		# 获取登录对象
		user = Users.objects.get(id = request.session['id'])
		# 创建订单表
		order = Orders()
		order.uid = user.id
		order.linkman = user.name
		order.address = user.address
		order.code = user.code
		order.phone = user.phone
		# tz = pytz.timezone('Asia/Shanghai')
		order.addtime = datetime.now()
		order.total = 0
		order.status = 4
		
		for i in shopid:
			# 判断页面是否刷新
			if request.session['shoplist'][str(i)]:
				# 未刷新
				order.save()
				# 获取商品
				shop = Goods.objects.get(id = int(i))
				# 创建订单详情表
				ob = Detail()
				ob.orderid = order.id
				ob.goodsid = shop.id
				ob.name = shop.goods
				ob.price = shop.price
				ob.num = int(request.session['shoplist'][str(i)]['num'])
				order = Orders.objects.get(id = order.id)
				order.total  += shop.price*int(request.session['shoplist'][str(i)]['num'])
				order.save()
				ob.save()
				# 清除选中商品session
				shoplist = request.session['shoplist']
				shoplist.pop(str(i))
				request.session['shoplist'] = shoplist
			elif Orders.objects.filter(uid = user.id):
				order = Orders.objects.filter(uid = user.id)
				context = {'orders':order}
			else:	
				context={'info':'暂无订单!'}
				return render(request,'myweb/meizu/order/order.html',context)
		orders = Orders.objects.filter(uid = user.id)
		midorder = orders
		midorder = midorder.order_by('-id')
		orders = midorder
		context = {'orders':orders}
		context['detaillist'] = Detail.objects.filter(orderid__in=Orders.objects.only('id').filter(uid=user.id))
		
	except:
		if Orders.objects.filter(uid = request.session['id']):

			orders = Orders.objects.filter(uid = request.session['id'])
			midorder = orders
			midorder = midorder.order_by('-id')
			orders = midorder
			context = {'orders':orders}
			context['detaillist'] = Detail.objects.filter(orderid__in=Orders.objects.only('id').filter(uid=user.id))
			#context['goodslist'] = Goods.objects.filter(id__in=Detail.objects.only('goodsid').filter(orderid__in=Orders.objects.only('id').filter(uid=user.id)))
		else:
			context={}
			context['info'] = '暂无订单!'
	goodsidlist = []
	for i in Detail.objects.only('goodsid').filter(orderid__in=Orders.objects.only('id').filter(uid=user.id)):
		goodsidlist.append(i.goodsid)
	context['goodslist'] = Goods.objects.filter(id__in=goodsidlist)
	return render(request,'myweb/meizu/order/order.html',context)