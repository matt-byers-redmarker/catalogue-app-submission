gapi.load('auth2', function() {
    auth2 = gapi.auth2.init({
        client_id: '531238088619-l8qdbu2tms74f1kkaoam691u7te4dcdh.apps.googleusercontent.com',
        scope: 'email profile openid'
    });
});
