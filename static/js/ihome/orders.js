//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-comment").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
    });
});

$(document).ready(function(){
    $.ajax({
        url:'/order/my_orders/',
        type: 'GET',
        dataType:'json',
        success: function(data){
            $.each(data.data,function(index,elem){
                $('.orders-list').append(
                    $('<li>').attr('id',elem.order_id).append(
                        $('<div>').attr('class','order-title').append(
                            $('<h3>').text('订单编号：'+elem.order_id),
                            $('<div>').attr('class','fr order-operate').append(
                                    $('<button>').attr({'type':'button','class':'btn btn-success order-comment',
                                    'data-toggle':'modal','data-target':'#comment-modal','id':elem.order_id,'onclick':'comment(this)' }).text('发表评价')
                            )
                        ),
                        $('<div>').attr('class','order-content').append(
                            $('<img>').attr('src',elem.image),
                            $('<div>').attr('class','order-text').append(
                                $('<h3>').text('订单'),
                                $('<ul>').append(
                                    $('<li>').text('创建时间：'+elem.create_date),
                                    $('<li>').text('入住日期：'+elem.begin_date),
                                    $('<li>').text('离开日期：'+elem.end_date),
                                    $('<li>').text('合计金额：'+elem.amount+'元(共'+elem.days+'晚)'),
                                    $('<li>').text('订单状态：').append($('<span>').text(elem.status)),
                                    $('<li>').text('我的评价：'+elem.comment),
                                    $('<li>').text('拒单原因：'+'不适合')
                                )
                            )
                        )
                    )
                )
                if (elem.status in ['WAIT_ACCEPT','WAIT_PAYMENT','CANCELED','REJECTED']){
                    $('#'+elem.order_id).hide()
                }
            })
        },
        error: function(data){
            alert('请求失败')
        }
    })
})


function comment(e){
    var id = $(e).attr('id')
    $('.btn-primary').attr('order_id',id)
}


function submit(e){
    var order_id = $(e).attr('order_id')
    var comment = $('#comment').val()
    $.ajax({
        url: '/order/comment/',
        data:{'order_id':order_id,'comment':comment},
        type: 'POST',
        dataType:'json',
        success: function(data){
            if (data.code == 200){
               location.href = ''
            }
        },
        error: function(data){
            alert('请求失败')
        }
    })
}