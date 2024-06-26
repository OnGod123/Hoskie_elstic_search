$(document).ready(function() {
    $('#search').click(function() {
        var query = $('#query').val().trim();
        if (!query.match(/^[a-zA-Z0-9_@. ]+$/)) {
            $('#result').html('<p>Invalid search query.</p>');
            return;
        }
        $.ajax({
            url: '/search_user/',
            method: 'GET',
            data: { 'query': query },
            success: function(data) {
                if (data.error) {
                    $('#result').html('<p>' + data.error + '</p>');
                } else {
                    var resultHtml = '';
                    data.forEach(function(user) {
                        resultHtml += '<p>Username: ' + user.username + '</p>';
                        resultHtml += '<p>Name: ' + user.name + '</p>';
                        resultHtml += '<p>Email: ' + user.email + '</p>';
                        resultHtml += '<p>Relationship Status: ' + user.relationship_status + '</p>';
                        resultHtml += '<p>Sexual Orientation: ' + user.sexual_orientation + '</p>';
                        resultHtml += '<p>Race: ' + user.race + '</p>';
                        resultHtml += '<p>Phone Number: ' + user.phone_number + '</p>';
                        resultHtml += '<p>Social Media API: ' + user.social_media_api + '</p>';
                        resultHtml += '<p>Birth Date: ' + user.birth_date + '</p>';
                        if (user.profile_video) {
                            resultHtml += '<p>Profile Video: <a href="' + user.profile_video + '">View</a></p>';
                        }
                        if (user.location) {
                            resultHtml += '<p>Location: ' + user.location + '</p>';
                        }
                        if (user.tweet) {
                            resultHtml += '<p>Tweet: <img src="' + user.tweet + '" alt="Tweet Image"></p>';
                        }
                        if (user.video) {
                            resultHtml += '<p>Video: <a href="' + user.video + '">Watch</a></p>';
                        }
                        if (user.image) {
                            resultHtml += '<p>Image: <img src="' + user.image + '" alt="Profile Image"></p>';
                        }
                        resultHtml += '<hr>';
                    });
                    $('#result').html(resultHtml);
                }
            },
            error: function(xhr) {
                $('#result').html('<p>Error: ' + xhr.responseText + '</p>');
            }
        });
    });
});

