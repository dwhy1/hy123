$(function(){

        // 获取页面上的值
        console.log($("p.subtotal > span").text());

        $('.del-cart').click(function () {
          // 获取需要的数据：商品编号
          console.log('获取商品编号');
          var $goods_id = $(this).attr('goods_id');
          console.log($goods_id);
          $(this).parent().parent().remove();

        // 发送ajax请求，删除商品
        // $.ajax({
        //     url: '/shopcart/'+ $goods_id +'/shop_cart_del/',
        //     type: 'GET',
        //     success:function (response) {
        //         console.log(response);
        //         alert('商品删除成功！')
        //     },
        //
        //     error:function () {
        //         console.log('请求失败')
        //     }
        // })
      });

        // 商品数量变化
        $('.reduce').click(function () {
              // 获取需要的数据：商品编号
              console.log('商品数量变化');
              // var $goods_id = $(this).next().val();
              var count = $(this).next().val();
              if (count <= 1){
                  $(this).next().val(1)
              }else{
                  var num = count-1;
                  $(this).next().val(num)
              }
          });

        $('.add').click(function () {
              // 获取需要的数据：商品编号
              var count = $(this).prev().val();
              var num = parseInt(count)+1;
              $(this).prev().val(num);
              // console.log(count);

          });

        //商品总价
        $(function () {
            $('.add').on('click', function(){
                var i = $(this).prev().val();
                var $goods_id = $(this).attr('up_goods_id');
                console.log($goods_id);
                var shop_total = i * $(this).parent().siblings(".good_price").attr("data-m");
                $(this).parent().siblings(".subtotal").text("总价："+shop_total);
                aj($goods_id,i)

            });
                $('.reduce').on('click', function(){
                var i = $(this).next().val();
                var $goods_id = $(this).attr('down_goods_id');
                var shop_total = i * $(this).parent().siblings(".good_price").attr("data-m");
                $(this).parent().siblings(".subtotal").text("总价："+shop_total);
                aj($goods_id,i)
            });

            });

        // ajax更新
            function aj(goods_id,i){
                $.ajax({
                url: '/shopcart/'+goods_id+'/'+i+'/shopcart_update/',
                type: 'GET',
                // data: {"csrfmiddlewaretoken": "{{csrf_token}}"},
                success:function (response) {
                    console.log(response)
                },
                error:function (response) {
                    console.log("失败")
                }
            })
            }


         // 选择商品
         $('#check_all').click(function () {
            state=$(this).prop('checked');
            $(':checkbox:not(#check_all)').prop('checked', state);
            });
            //选择
            $(':checkbox:not(#check_all)').click(function () {
                if ($(this).prop('checked')){
                    if ($(':checked').length+1==$(':checkbox').length){
                        $('#check_all').prop('checked', true);
                    }
                } else {
                    $('#check_all').prop('checked', false);
                }
            });




   });