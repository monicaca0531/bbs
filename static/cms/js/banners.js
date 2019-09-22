
$(function () {
    $("#banner-save-btn").click(function (event) {
        var self = $(this);
        event.preventDefault();
        var bannerModal = $("#bannerModal");
        var nameInput = bannerModal.find("input[name='name']");
        var imgUrlInput = bannerModal.find("input[name='img_url']");
        var linkToInput = bannerModal.find("input[name='link_to']");
        var priorityInput = bannerModal.find("input[name='priority']");

        var name = nameInput.val();
        var img_url = imgUrlInput.val();
        var link_to = linkToInput.val();
        var priority = priorityInput.val();
        var banner_id = self.attr("data-id");
        var submitType = self.attr("data-type");

        if(!name || !img_url || !link_to || !priority){
            bbsalert.alertInfoToast('请输入完整的轮播图信息');
            return;
        }

        var url = ''
        if(submitType == 'update'){
            url = '/cms/ubanner/';
        }else{
            url = '/cms/abanner/';
        }

        bbsajax.post({
            'url':url,
            'data':{
                'name':name,
                'img_url':img_url,
                'link_to':link_to,
                'priority':priority,
                'banner_id':banner_id
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
    });
});

$(function () {
    $(".edit-banner-btn").click(function (event) {
        var self = $(this);
        event.preventDefault();
        var bannerModal = $("#bannerModal");
        bannerModal.modal('show');

        var nameInput = bannerModal.find("input[name='name']");
        var imgUrlInput = bannerModal.find("input[name='img_url']");
        var linkToInput = bannerModal.find("input[name='link_to']");
        var priorityInput = bannerModal.find("input[name='priority']");
        var saveBtn = bannerModal.find("#banner-save-btn");

        var tr = self.parent().parent()
        var banner_id = tr.attr('data-id');
        var data_name = tr.attr('data-name');
        var data_img_url = tr.attr('data-img-url');
        var data_link_to = tr.attr('data-link-to');
        var data_priority = tr.attr('data-priority');

        nameInput.val(data_name);
        imgUrlInput.val(data_img_url);
        linkToInput.val(data_link_to);
        priorityInput.val(data_priority);
        saveBtn.attr("data-type",'update');
        saveBtn.attr("data-id",banner_id);
    });
});


$(function () {
    $(".delete-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent()
        var banner_id = tr.attr('data-id');
        bbsalert.alertConfirm({
            'msg':'确定是否删除该轮播图？',
            'confirmCallback':function () {
                bbsajax.post({
                    'url':'/cms/dbanner/',
                    'data':{
                        'banner_id':banner_id
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


// $(function () {
//     bbsqiniu.setUp({
//         'domain': 'http://underfire.s3-cn-south-1.qiniucs.com/',
//         'browse_btn': 'upload-btn',
//         'uptoken_url': '/c/uptoken/',
//         'success': function (up,file,info) {
//             var imageInput = $("input[name='image_url']");
//             imageInput.val(file.name);
//         }
//     });
// });

function Qiniu(){

};

Qiniu.prototype.run = function(){
    this.listenQiniuUploadFileEvent();
};

Qiniu.prototype.listenQiniuUploadFileEvent = function(){
    var self = this;
    var uploadBtn = $("#upload-btn");
    uploadBtn.change(function () {
        var file = this.files[0];
        bbsajax.get({
            'url':'/c/uptoken/',
            'success':function (result) {
                var token = result['uptoken'];
                var key = (new Date()).getTime() + '.' + file.name.split('.')[1];
                var putExtra = {
                    fname: key,
                    params: {},
                    mimeType: ['image/png', 'image/jpeg', 'image/gif', 'video/x-ms-wmv']
                };
                var config = {
                    useCdnDomain:true,
                    retryCount:6,
                    region: qiniu.region.z2,
                };
                var observable = qiniu.upload(file,key,token,putExtra,config);
                observable.subscribe({
                    'next':self.handleFileUploadProgress,
                    'error':self.handleFileUploadError,
                    'complete':self.handleFileUploadComplete
                });

            }
        });
    });
};


Qiniu.prototype.handleFileUploadProgress = function(response){
    var total = response.total;
    // var percent = total.percent;
    // var percentText = percent.toFixed(0) + '%';
    // var progressGroup = News.progressGroup;
    // progressGroup.show();
    // var progressBar = $(".progress-bar");
    // progressBar.css({"width":percentText});
    // progressBar.text(percentText);
    console.log("total:",total);
    console.log('上传过程');
};

Qiniu.prototype.handleFileUploadError = function(error){
    // window.messageBox.showError(error.message);
    // var progressGroup = News.progressGroup;
    // progressGroup.hide();
    console.log("error:",error);
};

Qiniu.prototype.handleFileUploadComplete = function(response){
    console.log(response);
    // var progressGroup = News.progressGroup;
    // progressGroup.hide();


    var domain = 'http://underfire.s3-cn-south-1.qiniucs.com/';
    var name = response.key;
    var url = domain + name;
    var imgUrlInput = $("input[name='img_url']");
    imgUrlInput.val(url);
    // var progressBar = $(".progress-bar");
    // progressBar.css({"width":0});
};

$(function () {
    var qiniuupload = new Qiniu();
    qiniuupload.run();
})