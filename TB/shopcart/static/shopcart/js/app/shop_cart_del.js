$(function(){
        $('#add-cart').click(function () {
          // 获取需要的数据：商品编号、购买数量
          var $goods_id = $(this).attr('goods_id');
          var $count = $(this).prev().val();
          console.log($goods_id, $count);

        // 发送ajax请求，添加到购物车
        $.ajax({
            url: '/shopcart/'+$goods_id+'/'+$count+'/shop_cart_add/',
            type: 'GET',
            success:function (response) {
                console.log(response);
                alert('商品添加成功！')
                $('#war').css({
                    "display": "block",
                });
            },

            error:function () {
                console.log('请求失败')
            }
        })
      })
   });