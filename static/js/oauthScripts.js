gapi.load('auth2', function() {
    auth2 = gapi.auth2.init({
        client_id: '531238088619-l8qdbu2tms74f1kkaoam691u7te4dcdh.apps.googleusercontent.com',
        scope: 'email profile openid'
    });
});

XMLHttpRequest.addEventListener('readystatechange', evt => {
    if (this.readyState == 4 && this.status == 200) {
        setTimeout(function() {
            window.location.href = "/";
        }, 4000);
    }
}, false);