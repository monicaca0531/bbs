
$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var telephoneE = $("input[name='telephone']");
        var passwordE = $("input[name='password']");
        var rememberE = $("input[name='remember-me']");

        var telephone = telephoneE.val();
        var password = passwordE.val();
        var remember = rememberE.checked?1:0;

        bbsajax.post({
            'url':'/signin/',
            'data':{
                'telephone':telephone,
                'password':password,
                'remember':remember
            },
            'success':function (result) {
                console.log(result);
                if(result['code'] == 200){
                    var return_to = $('#return-to-span').text();
                    if(return_to){
                        window.location = return_to;
                    }else{
                        window.location = '/';
                    }
                }else{
                    bbsalert.alertInfo(result['message']);
                }
            },
            'fail':function () {
                bbsalert.alertNetworkError();
            }
        });
    });
})