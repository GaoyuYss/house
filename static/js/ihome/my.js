function logout() {
    $.get("/user/logout/", function(data){
        if (data.code ==200 ) {
            location.href = "/house/index/";
        }
    })
}

$(document).ready(function(){
    $.ajax({
        url: '/user/my_info/',
        type: 'GET',
        dataType: 'json',
        success:function(data){
            if (data.code=='200'){
                $('#user-name').text(data.name)
                $('#user-mobile').text(data.phone)
            }
        },
        error:function(data){
            alert('请求失败')
        }
    })

})

