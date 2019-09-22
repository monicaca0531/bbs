
$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();

        var oldpdwE = $("input[name='oldpwd']");
        var newpwdE = $("input[name='newpwd']");
        var newpwd2E = $("input[name='newpwd2']");

        var oldpwd = oldpdwE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        bbsajax.post({
            'url':'/cms/resetpwd/',
            'data':{
                'oldpwd':oldpwd,
                'newpwd':newpwd,
                'newpwd2':newpwd2
            },
            'success':function (result) {
                if(result['code'] == 200){
                    bbsalert.alertSuccess('密码修改成功');
                }else{
                    var message = result['message'];
                    bbsalert.alertError(message);
                };
                oldpdwE.val("");
                newpwdE.val("");
                newpwd2E.val("");
                },
            'fail':function (error) {
                bbsalert.alertNetworkError();
            }
        });
    })
});

