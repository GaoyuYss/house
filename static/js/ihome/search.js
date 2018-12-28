var cur_page = 1; // 当前页
var next_page = 1; // 下一页
var total_page = 1;  // 总页数
var house_data_querying = true;   // 是否正在向后台获取数据

function hrefBack() {
    history.go(-1);
}


// 解析url中的查询字符串
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}


$(document).ready(function(){
    var queryData = decodeQuery();
    var startDate = queryData["sd"];
    var endDate = queryData["ed"];
    var aid = queryData["aid"];
    var aname = queryData["aname"]
    $.ajax({
        url:'/house/house_first/',
        type: 'POST',
        dataType: 'json',
        data: {'startDate':startDate,'endDate':endDate,'aid':aid,'aname':aname},
        success: function(data){
            $.each(data.areas_data,function(index,elem){
                $('.filter-area').append(
                    $('<li>').attr('area-id',elem.id).text(elem.name)
                )
            });
            $.each(data.house_data,function(index,elem){
                $('.house-list').append(
                    $('<li>').attr('class','house-item').append(
                        $('<a>').attr('href','/house/detail/?id='+elem.id).append(
                            $('<img>').attr('src',elem.images[0])
                        ),
                        $('<div>').attr('class','house-desc').append(
                            $('<div>').attr('class','landlord-pic').append(
                                $('<img>').attr('src',elem.user_avatar)
                            ),
                            $('<div>').attr('class','house-price').html('￥<span>'+elem.price+'</span>/晚'),
                            $('<div>').attr('class','house-intro').append(
                                $('<span>').attr('class','house-title').text(elem.title),
                                $('<em>').text('出租'+elem.room_count+'间 - 1次入住 - '+elem.address)
                            )
                        )
                    )
                )
            })
        },
        error: function(data){
        }
    })
})

// 更新用户点选的筛选条件
function updateFilterDateDisplay() {
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var $filterDateTitle = $(".filter-title-bar>.filter-title").eq(0).children("span").eq(0);
    if (startDate) {
        var text = startDate.substr(5) + "/" + endDate.substr(5);
        $filterDateTitle.html(text);
    } else {
        $filterDateTitle.html("入住日期");
    }
}


// 更新房源列表信息
// action表示从后端请求的数据在前端的展示方式
// 默认采用追加方式
// action=renew 代表页面数据清空从新展示
function updateHouseData(action) {
    var areaId = $(".filter-area>li.active").attr("area-id");
    if (undefined == areaId) areaId = 1;
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var sortKey = $(".filter-sort>li.active").attr("sort-key");
    var params = {
        aid:areaId,
        sd:startDate,
        ed:endDate,
        sk:sortKey,
        p:next_page
    };
    // 删除之前的房屋元素
    $('.house-item').remove()
    //发起ajax请求，获取数据，并显示在模板中
    $.ajax({
        url:'/house/update_search/',
        data:params,
        type:'POST',
        dataType:'json',
        success :function(data){
             $.each(data.house_data,function(index,elem){
                $('.house-list').append(
                    $('<li>').attr('class','house-item').append(
                        $('<a>').attr('href','/house/detail/?id='+elem.id).append(
                            $('<img>').attr('src',elem.images[0])
                        ),
                        $('<div>').attr('class','house-desc').append(
                            $('<div>').attr('class','landlord-pic').append(
                                $('<img>').attr('src',elem.user_avatar)
                            ),
                            $('<div>').attr('class','house-price').html('￥<span>'+elem.price+'</span>/晚'),
                            $('<div>').attr('class','house-intro').append(
                                $('<span>').attr('class','house-title').text(elem.title),
                                $('<em>').text('出租'+elem.room_count+'间 - 1次入住 - '+elem.address)
                            )
                        )
                    )
                )
            })
        },
        error:function(data){
            alert('请求失败')
        }
    })
}

$(document).ready(function(){
    var queryData = decodeQuery();
    var startDate = queryData["sd"];
    var endDate = queryData["ed"];
    $("#start-date").val(startDate);
    $("#end-date").val(endDate);
    updateFilterDateDisplay();
    var areaName = queryData["aname"];
    if (!areaName) areaName = "位置区域";
    $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html(areaName);

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    var $filterItem = $(".filter-item-bar>.filter-item");
    $(".filter-title-bar").on("click", ".filter-title", function(e){
        var index = $(this).index();
        if (!$filterItem.eq(index).hasClass("active")) {
            $(this).children("span").children("i").removeClass("fa-angle-down").addClass("fa-angle-up");
            $(this).siblings(".filter-title").children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).addClass("active").siblings(".filter-item").removeClass("active");
            $(".display-mask").show();
        } else {
            $(this).children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).removeClass('active');
            $(".display-mask").hide();
            updateFilterDateDisplay();
        }
    });
    $(".display-mask").on("click", function(e) {
        $(this).hide();
        $filterItem.removeClass('active');
        updateFilterDateDisplay();
        cur_page = 1;
        next_page = 1;
        total_page = 1;
        updateHouseData("renew");

    });
    $(".filter-item-bar>.filter-area").on("click", "li", function(e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html($(this).html());
        } else {
            $(this).removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html("位置区域");
        }
    });
    $(".filter-item-bar>.filter-sort").on("click", "li", function(e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(2).children("span").eq(0).html($(this).html());
        }
    })
})

