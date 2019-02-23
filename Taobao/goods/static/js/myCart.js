// JavaScript Document
 
/*改变所购商品的数量*/
function changeNum(numId,flag){/*numId表示对应商品数量的文本框ID，flag表示是增加还是减少商品数量*/
    var tom=document.getElementById(numId);
     if(flag=='add'){
         tom.value++;
    }
    if(flag=='minus'){
    if (tom.value > 1) {
        tom.value=tom.value-1;
    }
}
    getSubTotal(tom.parentNode.parentNode.id);
    productCount();
}
    function getSubTotal(tr) {
        var tds=document.getElementById(tr);
        var price = parseFloat(tds.cells[4].innerHTML);//获取价格
        var count = parseInt(tds.cells[5].getElementsByTagName('input')[0].value);//获取数量
        var SubTotal = parseFloat(price * count);
        tds.cells[6].innerHTML = SubTotal.toFixed(2);//四舍五入
    }
/*自动计算商品的总金额、总共节省的金额和积分*/
function productCount(){
    var checkAllInputs = document.getElementById('allCheckBox');
    var tableTr=document.getElementById("shopping").getElementsByTagName("tr");
    var total=0;      //所有商品的总计
    var integral=0;   //所有商品的积分
    console.log(tableTr);
    if(tableTr.length==3){
        checkAllInputs.checked=false;
    }
    var checkInputs = document.getElementsByName("cartCheckBox");
    for(var i=0;i< checkInputs.length;i++){
        var point=0;      //每一行商品的单品积分
        var price=0;     //每一行商品的单价
        var nums=0;    //每一行商品的数量
 
        if(checkInputs[i].checked) { //判断复选框是否被选中
                  var c=checkInputs[i].parentNode.parentNode;
                        point=c.childNodes[7].innerHTML;  //选中行商品的单品积分
                        price=c.childNodes[9].innerHTML;  //选中行商品的单价
                        nums=c.childNodes[11].childNodes[2].value; //选中行商品的数量
                        console.log(nums);
                        integral+=point*nums;  //所有商品的积分的和 = 每一行商品的单价积分 x 数量   相加
                        total+=price*nums;//所有商品的总计的和 = 每一个商品的单价 x 数量   相加
                        c.childNodes[13].innerHTML=price*nums;  //商品小计 =商品的单价 x 数量
            } else {
            total+=0;//思考这里为什么是“+=”
            integral+=0;
        }
    }
    document.getElementById("total").innerHTML=total;
    document.getElementById("integral").innerHTML=integral;
}
 
  window.onload=productCount; //onload函数，让页面加载后自动计算商品总额
 
/*复选框全选或全不选效果*/
function selectAll(){
    var checkInputs = document.getElementsByName("cartCheckBox");
    var checkAllInputs = document.getElementById('allCheckBox');
            for(var i=0;i< checkInputs.length;i++){
                checkInputs[i].checked=checkAllInputs.checked;
            }
     }
 
/*根据单个复选框的选择情况确定全选复选框是否被选中*/
function selectSingle(){
    var checkInputs = document.getElementsByName("cartCheckBox");
    var checkAllInputs = document.getElementById('allCheckBox');
    var count=0;
    for(var i=0;i< checkInputs.length;i++){
        if(checkInputs[i].checked) {
            count++;
        }
            if (count === checkInputs.length ) {//判断是否全选
                checkAllInputs.checked = true;
                selectAll();
            } else {
            checkAllInputs.checked=false;
        }
        }
    productCount();
}
 
/*删除单行商品*/
function deleteRow(rowId){
    var t = document.getElementById(rowId);
    t.previousSibling.previousSibling.remove();
    t.remove();
    productCount();
 }
 
/*删除选中行的商品*/
function deleteSelectRow() {
    var inp=document.getElementsByName("cartCheckBox");  //获取每个多选框
    for (var i=inp.length-1;i>=0;i--){//若顺序则无法删除所有
        if(inp[i].checked){
            inp[i].parentNode.parentNode.previousSibling.previousSibling.remove();
            inp[i].parentNode.parentNode.remove();
            inp.checked = false;//思考这里为什么不用数组下标
            productCount();
        }
    }
}
