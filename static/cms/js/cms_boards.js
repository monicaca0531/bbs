
$(function () {
   $("#add-board-btn").click(function (event) {
       event.preventDefault();
       bbsalert.alertOneInput({
           'text':'创建板块',
           'inputPlaceholder':'请输入板块名称',
           'confirmCallback':function (inputValue) {
               bbsajax.post({
                   'url':'/cms/aboard/',
                   'data':{
                       'name':inputValue
                   },
                   'success':function (result) {
                       console.log(result);
                       if(result['code'] == 200){
                           window.location.reload();
                       }else{
                           bbsalert.alertInfo(result['message']);
                       }
                   },
                   'fail':function () {
                       bbsalert.alertNetworkError();
                   }
               });
           }
       });
   });
});

$(function () {
    $(".edit-board-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var board_id = tr.attr('data-id');
        bbsalert.alertOneInput({
            'title':'请修改模板名称',
            'placeholder':name,
            'confirmCallback':function (inputValue) {
                bbsajax.post({
                    'url':'/cms/uboard/',
                    'data':{
                        'board_id':board_id,
                        'name':inputValue
                    },
                    'success':function (result) {
                        console.log(result);
                        if(result['code'] == 200){
                            window.location.reload();
                        }else{
                            bbsalert.alertInfo(result['message']);
                        }
                    },
                    'fail':function () {
                        bbsalert.alertNetworkError();
                    }
                });
            }
        });
    });
});

$(function () {
    $(".delete-board-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr('data-id');
        bbsalert.alertConfirm({
            'title':'确定是否删除该模板',
            'confirmCallback':function () {
                bbsajax.post({
                    'url':'/cms/dboard/',
                    'data':{
                        'board_id':board_id
                    },
                    'success':function (result) {
                        if(result['code'] == 200){
                            window.location.reload();
                        }else{
                            bbsalert.alertInfo(result['message']);
                        }
                    },
                    'fail':function () {
                        bbsalert.alertNetworkError();
                    }
                });
            }
        });
    });
});