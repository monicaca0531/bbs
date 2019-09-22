var bbsparam = {
    setParam: function (href,key,value) {
        //重新加载整个页面
        var isReplace = false;
        var urlArray = href.split('?');
        if(urlArray.length > 1){
            var querryArray = urlArray[1].split('&');
            for(var i=0; i < querryArray.length; i++){
                var paramsArray = querryArray[i].split('=');
                if(paramsArray[0] == key){
                    paramsArray[1] = value;
                    querryArray[i] = paramsArray.join('=');
                    isReplace = true;
                    break;
                }
            }
            var params = querryArray.join('&');
            urlArray[1] = params;
            href = urlArray.join('?');
        }else{
            var param = {};
            param[key] = value;
            href = href + '?' + $.param(param);
        }
        return href;
    }
};
