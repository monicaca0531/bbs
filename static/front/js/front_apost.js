
$(function () {
    var ue = UE.getEditor("ueditor",{
        "serverUrl":'/ueditor/upload/'
    });

    $("#submit-post-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);

        var titleInput = $("input[name='title']");
        var boardSelect = $("select[name='board_id']");

        var title = titleInput.val();
        var board_id = boardSelect.val();
        var content = ue.getContent();

        bbsajax.post({
            'url':'/apost/',
            'data':{
                'title':title,
                'board_id':board_id,
                'content':content,
            },
            'success':function (result) {
                if(result['code'] == 200){
                    bbsalert.alertConfirm({
                        'title':'发表帖子成功',
                        'confirmText':'再发表一篇？',
                        'cancelText':'返回首页',
                        'confirmCallback':function () {
                            window.location.reload();
                        },
                        'cancelCallback':function () {
                            window.location = '/';
                        }
                    });
                }else{
                    bbsalert.alertInfo(result['message']);
                }
            }
        });
    });
});