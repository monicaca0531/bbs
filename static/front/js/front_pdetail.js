
$(function () {
    var ue = UE.getEditor("apost-ue",{
        "serverUrl":"/ueditor/upload/",
        "toolbars":[
            [
                'undo',//撤销
                'redo',//重做
                'bold',//加粗
                'forecolor',//字体颜色
                'italic',//斜体
                'underline',//下划线
                'strikethrough',//删除线
                'blockquote',//引用
                'emotion',//表情
                'simpleupload',//单图上传
            ]
        ]
    });
    window.ue = ue;
});

$(function () {
   $("#comment-btn").click(function (event) {
       event.preventDefault();
       var self = $(this);
       var loginTag = $("#login-tag").attr("data-is-login");
       if(!loginTag){
           window.location = '/signin/';
       }else{
           var content = window.ue.getContent();
           var post_id = self.attr("data-post-id");
           bbsajax.post({
               'url':'/acomment/',
               'data':{
                   'content':content,
                   'post_id':post_id
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