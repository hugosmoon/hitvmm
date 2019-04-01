$(".loginbtn").click(function () {
        $.cookie('stuid', '', {expires: -1, path: '/'});
        $.cookie('stuname', '', {expires: -1, path: '/'});
        $.cookie('stunum', '', {expires: -1, path: '/'});
        $(location).attr('href', '/login/');
    });