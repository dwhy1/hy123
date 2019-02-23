


$(function (){
    //加的效果
    $(".nub-jia").click(function(){
        var n=$(this).prev().val();
        var num=parseInt(n)+1;
        if(num==0){ return;}
        $(this).prev().val(num);
    });
    //减的效果
    $(".nub-jian").click(function(){
        var n=$(this).next().val();
        var num=parseInt(n)-1;
        if(num==0){ return}
        $(this).next().val(num);
    });
});


$(function () {
    // console.log($(".play-d").attr("date-m"))

   $(".nub-jia").on("click",function () {
       var i=$(this).prev().val();
       var g_id=$(this).prev().attr('goods_id')
       // console.log(g_id)
       $(this).parent().siblings(".shop-sum").children().html("￥"+i*$(".play-d").attr('date'-g_id));
       // sums=$(this).parent().siblings(".shop-sum").children().text()
       // console.log(sums)
       console.log($(".play-d").attr('date'-g_id))
       $(".sum").html("￥"+i*$(".play-d").attr('date'-g_id));
       //console.log(i)
   })
    $(".nub-jian").on("click",function () {
        var i=$(this).next().val();
        if(i<=1){
            i=1;
        }
        $(this).parent().siblings(".shop-sum").children().html("￥"+i*$(".play-d").attr("date-m"));
        // sums=$(this).parent().siblings(".shop-sum").children().text()
        // console.log(sums)
        $(".sum").html("￥"+i*$(".play-d").attr("date-m"));
        //console.log(i)
    })
})