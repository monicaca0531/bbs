
$(function () {
   $(".highlight-btn") .click(function (event) {
       event.preventDefault();
       var self = $(this);
       var tr = self.parent().parent();
       var highlight = parseInt(tr.attr("data-highlight"));
       console.log(highlight);
       var post_id = tr.attr("data-id");
       var url = ""
       if(highlight){
           url = '/cms/dhposts/';
       }else{
           url = '/cms/hposts/';
       }
       console.log(url);
       bbsajax.post({
          'url':url,
          'data':{
              'post_id':post_id
          } ,
           'success':function (result) {
               if(result['code'] == 200){
                   bbsalert.alertSuccessToast('操作成功');
                   setTimeout(function () {
                       window.location.reload();
                   },500);
               }else{
                   bbsalert.alertInfo(result['message']);
               }
           }
       });
   });
});


$(function () {
   $(".delete-btn").click(function (event) {
       event.preventDefault();
       var self = $(this);
       var tr = self.parent().parent();
       var post_id = tr.attr('data-id');

       bbsajax.post({
           'url':'/cms/dposts/',
           'data':{
               'post_id':post_id
           },
           'success':function (result) {
               if(result['code'] == 200){
                   bbsalert.alertSuccessToast('删除成功');
                   setTimeout(function () {
                       window.location.reload();
                   },500);
               }else{
                   bbsalert.alertInfo(result['message']);
               }
           },
           'fail':function () {
               bbsalert.alertNetworkError();
           }
       });
   });
});