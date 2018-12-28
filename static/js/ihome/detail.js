function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}



$(document).ready(function(){
    var url = location.search
    $.ajax({
        url: '/house/detail_image/'+parseInt(url.split('=')[1]),
        type: 'GET',
        dataType: 'json',
        success: function(data){
                var image_url= ''
                for ( i=0;i< data.data.images.length;i++){

                    image_url+='<li class="swiper-slide"><img src='+data.data.images[i]+'></li>'
                }
                $('.swiper-wrapper').html(image_url)

                $(document).ready(function(){
                    var mySwiper = new Swiper ('.swiper-container', {
                        loop: true,
                        autoplay: 2000,
                        autoplayDisableOnInteraction: false,
                        pagination: '.swiper-pagination',
                        paginationType: 'fraction'
                    })
                    $(".book-house").show();
                })
        },
        error: function(data){
            alert('失败')
        }
    })
})


$(document).ready(function(){
    var url = location.search
    $.ajax({
        url: '/house/detail_info/'+parseInt(url.split('=')[1]),
        type: 'GET',
        dataType: 'json',
        success: function(data){

            $('.house-price span').text(data.data.price)
            $('.house-title').text(data.data.title)
            $('.landlord-pic img').attr('src',data.data.user_avatar)
            $('#user_name').text(data.data.user_name)
            $('.text-center li').text(data.data.address)
            $('#room_count').text('出租'+data.data.room_count+'间')
            $('#acreage').text('房屋面积:'+data.data.acreage+'平米')
            $('#unit').text('房屋户型:'+data.data.unit)
            $('#capacity').text('宜住'+data.data.capacity+'人')
            $('#beds').text(data.data.beds)
            $('#deposit').text(data.data.deposit)
            $('#min_days').text(data.data.min_days)
            if (data.data.max_days ==0){
                $('#max_days').text('无限制')
            }else{$('#max_days').text(data.data.max_days)}
            var  html_char=''
            for ( i=0;i< data.data.facilities.length;i++){
                html_char += '<li><span class="'+data.data.facilities[i].css+'"></span>'+data.data.facilities[i].name+'</li>'
            }
            $('.house-facility-list').html(html_char)
            $('.book-house').attr('href','/order/booking/?house_id='+data.data.id)
            if (data.booking ==1){
                $('.book-house').hide()
            }else{$('.book-house').show()}
        },
        error:function(data){
            alert('不可以')
        }
    })
})