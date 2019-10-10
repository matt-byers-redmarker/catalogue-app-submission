function onSignIn(googleUser) {
    // Hide login button / show logout button
    // document.querySelector('#login-button').classList.add('is-hidden');
    // document.querySelector('#logout-button').classList.remove('is-hidden')

    // Useful data for your client-side scripts:
    var profile = googleUser.getBasicProfile();
    $('.g-signin2').addClass('is-hidden')
    $('#logout-button').removeClass('is-hidden')
    console.log("ID: " + profile.getId()); // Don't send this directly to your server!
    console.log('Full Name: ' + profile.getName());
    console.log('Given Name: ' + profile.getGivenName());
    console.log('Family Name: ' + profile.getFamilyName());
    console.log("Image URL: " + profile.getImageUrl());
    $("#pic").attr("src",profile.getImageUrl());
    console.log("Email: " + profile.getEmail());
    $("#email").text(profile.getEmail());


    // The ID token you need to pass to your backend:
    var id_token = googleUser.getAuthResponse().id_token;
    console.log("ID Token: " + id_token);
    $('#result').html('ID Token:</br>'+ id_token + '')
}

function signOut() {
	$('.g-signin2').removeClass('is-hidden')
    $('#logout-button').addClass('is-hidden')
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function() {
        console.log('User signed out.');
    });
}

gapi.load('auth2', function() {
    auth2 = gapi.auth2.init({
        client_id: '531238088619-l8qdbu2tms74f1kkaoam691u7te4dcdh.apps.googleusercontent.com',
        scope: 'email profile openid'
    });
});
