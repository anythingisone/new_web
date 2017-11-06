
//数量减少
$('.subtract').click(function(){
	// 增减标志
	var flag = 'subtract'
	// 获取增减商品数量及id
	var num = $(this).next('div').find('input').attr('value')
	var id = $(this).next('div').find('span').attr('value')
	// 当前点击数量input
	var numn=$(this).next('div').find('input')
	var allprice = $(this).parent().parent().parent().next('td').find('span')
	$.ajax({
		url:'/myweb/numchange',
		type:'get',
		data:{'gid':id,'num':num,'flag':flag},
		dataType:'json',
		success:function(data){
			//ajax请求成功后执行的代码
			numn.attr('value',data.num)
			allprice.text(data.num*data.price)
			$('#totalprice').text()
		},
	})
	var tjtd = $(this).parent().parent().parent()
	var num = $(this).siblings('div').find('input').val()
	if ($(this).parent().parent().parent().siblings('.check').find('.checked').is(':checked')){
		var price = tjtd.siblings('.dj').find('span').text()

		if (num==1){

		}
		else{
			price = Number($('#totalPrice').text())-Number(price)
			$('#totalPrice').text(price)
		}
		
	}
})
//数量增加
$('.add').click(function(){
	// 增减标志
	var flag = 'add'
	var num = $(this).prev('div').find('input').attr('value')
	var id = $(this).prev('div').find('span').attr('value')
	var numn=$(this).prev('div').find('input')
	var allprice = $(this).parent().parent().parent().next('td').find('span')
	$.ajax({
		url:'/myweb/numchange',
		type:'get',
		data:{'gid':id,'num':num,'flag':flag},
		dataType:'json',
		success:function(data){
			//ajax请求成功后执行的代码
			if (numn.attr('value')==data.num){
				alert('亲,我只有这么多货哦')
			}
			else{
				numn.attr('value',data.num)
				allprice.text(data.num*data.price)
			}
			
		},
	})
	var tjtd = $(this).parent().parent().parent()
	var num = $(this).siblings('div').find('input').val()
	// 判断当前商品是否选中
	if ($(this).parent().parent().parent().siblings('.check').find('.checked').is(':checked')){
		var price = tjtd.siblings('.dj').find('span').text()
		price = Number($('#totalPrice').text())+Number(price)
		$('#totalPrice').text(price)
	}
})
// 输入框获取焦点
var oldnum = 0
$('.shopnum').focus(function(){
	// 保存旧数量
	oldnum = $(this).attr('value')
})

// 输入框失去焦点
$('.shopnum').blur(function(){
	// 定义正则
	var reg = /^[0-9]+$/;
	if (reg.test($(this).attr('value'))){
		if (Number($(this).attr('value'))<=1){
			$(this).attr('value',1)
		}
		if (Number($(this).attr('value'))>=Number($(this).attr('max'))){
			alert('亲,我就这么多了')
			$(this).attr('value',Number($(this).attr('max')))
		}
	}
	else {
		alert('请输入整数')
		$(this).attr('value',oldnum)
	}
	// 保存修改前小计
	var oldprice = Number($(this).parents('.num').siblings('.ptd').find('span').text())
	$(this).parents('.num').siblings('.ptd').find('.total').text(Number($(this).parents('.num').siblings('.dj').find('span').text())*Number($(this).attr('value')))
	// 判断当前修改数量商品是否被选中
	if ($(this).parents('.num').siblings('.check').find('.checked').is(':checked')){
		// 重新计算总价
		// 计算修改差价
		var cprice = Number($(this).parents('.num').siblings('.ptd').find('span').text()) - oldprice  
		// 总价加差价
		$("#totalPrice").text(Number($("#totalPrice").text())+cprice)
	}
	// 输入框标志
	var flag = 'input'
	var num = $(this).attr('value')
	var id = $(this).siblings('span').attr('value')
	$.ajax({
		url:'/myweb/numchange',
		type:'get',
		data:{'gid':id,'num':num,'flag':flag},
		dataType:'json',
	})

})

// 选中
$('.checked').click(function(){
	var price=$(this).parent().siblings().find('.allprice').text()
	// 判断是否选中
	if ($(this).is(':checked')){
		// 更新总价:总价+小计
		price = Number($('#totalPrice').text())+Number(price)
		$('#totalPrice').text(price)
		$('.checknum').text(Number($('.checknum').text())+1)
	}
	else{
		// 更新总价:总价-小计
		price = Number($('#totalPrice').text())-Number(price)
		$('#totalPrice').text(price)
		$('.checknum').text(Number($('.checknum').text())-1)
	}
	
})

// 全选
$('.allcheck').click(function(){
	// 获取全部复选框
	var coll = $('input').filter('.checked');
	// 判断全选是否选中
	if ($('.allcheck').is(':checked')){
		// 遍历复选框
		for(var i=0;i<coll.length;i++){
			// 判断复选框是否选中
			if ($(coll[i]).is(':checked')){

			}
			else{
				coll[i].checked=true;
				var price=$(coll[i]).parent().siblings().next('.ptd').find('span').text();
				price = Number($('#totalPrice').text()) + Number(price)
				$('#totalPrice').text(price)
				$('.checknum').text($('.cartnum').text())
			}
			
		}

	}
	else{
		for(var i=0;i<coll.length;i++){
			coll[i].checked=false;
		}
		$('#totalPrice').text(0)
		$('.checknum').text(0)
	}
	
})

// 删除
$('.del').click(function(){
	var id = $(this).attr('id')
	var del = $(this)
	$.ajax({
		url:'/myweb/delcart',
		type:'get',
		data:{'gid':id},
		dataType:'json',
		success:function(data){
			del.parent().parent().parent().remove()
			var num = Number($('.cartnum').text()) - 1
			$('.cartnum').text(num)
			// 判断是否选中
			if (del.parent().parent().siblings('.check').find('.checked').is(':checked')){
				// 获取删除商品小计
				var price = del.parent().parent().prev('td').find('span').text()
				// 刷新选中商品总价
				$('#totalPrice').text(Number($('#totalPrice').text())-Number(price))
				$('.checknum').text(Number($('.checknum').text())-1)
			}
		},
	})
})

// 去结算
$('.toorders').click(function(){
	var checkshops = []
	if ($("#totalPrice").text() == 0){
		alert('未选中商品!')
	}
	else{
		var coll = $('input').filter('.checked');
		for(var i=0;i<coll.length;i++){
			// 判断复选框是否选中
			if ($(coll[i]).is(':checked')){
				checkshops.push($(coll[i]).attr('goodsid'))
			}
		}
		$.ajax({
			url:'/myweb/orders',
			type:'get',
			data:{'checkshops':1},
			success:function(data){
				window.location.href='/myweb/order?shopid='+checkshops
			}
		})
	}
})