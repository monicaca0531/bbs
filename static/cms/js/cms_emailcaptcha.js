
$(function () {
    $('#sendCaptcha').click(function (event) {
        event.preventDefault();
        var emailE = $("input[name='newemail']");

        var email = emailE.val();
        if(!email){
            bbsalert.alertErrorToast('请输入邮箱！');
        }else{
            bbsajax.get({
                'url':'/cms/email_captcha/',
                'data':{
                    'email':email
                },
                'success':function (result) {
                    if(result['code'] == 200){
                        bbsalert.alertSuccessToast('成功发送验证码');
                    }else{
                        bbsalert.alertInfo(result['message']);
                    }
                }
            })
        }
    });
});

$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var newemailE = $("input[name='newemail']");
        var captchaE = $("input[name='captcha']");

        var newemail = newemailE.val();
        var captcha = captchaE.val();

        bbsajax.post({
            'url':'/cms/resetemail/',
            'data':{
                'newemail':newemail,
                'captcha':captcha
            },
            'success':function (result) {
                if(result['code'] == 200){
                    bbsalert.alertSuccessToast('成功修改邮箱');
                    newemailE.val('');
                    captchaE.val('');
                }else{
                    bbsalert.alertInfo(result['message']);
                }
            }
        });
    });
});