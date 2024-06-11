// like
$(document).ready(function () {
    $(".likebtn").click(function (e) {
        e.preventDefault();
        var post_id = $(this).data("post-id");
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        console.log(post_id);
        $.ajax({
            type: "POST",
            url: "/user/post_likes/" + post_id + "/",
            data: {
                csrfmiddlewaretoken: csrf,
            },
            success: function (data) {
                if (data.no_of_likes == 0) {
                    $('.post-id-' + post_id).text("No Likes");
                }
                else if (data.no_of_likes == 1) {
                    $('.post-id-' + post_id).text(data.no_of_likes + " Like");
                }
                else {
                    $('.post-id-' + post_id).text(data.no_of_likes + " Likes");
                }
            }
        });
    });
});

// follow

$(document).ready(function () {
    $('.followbtn').click(function (e) {
        e.preventDefault();
        var username = $(this).data("username");
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        console.log(username)
        $.ajax({
            type: "POST",
            url: "/user/followers/" + username + "/",
            data: {
                csrfmiddlewaretoken: csrf,
            },
            success: function (data) {
                if (data.follow == false) {
                    $('.followbtn').text("UNFOLLOW")
                    $('.followers').text("FOLLOWERS " + data.followers)
                }
                else {
                    $('.followbtn').text("FOLLOW")
                    $('.followers').text("FOLLOWERS " + data.followers)
                }
            }
        })
    })
})

// chat


$(document).ready(function () {
    // select the chat form and listen for submission event
    $('#sendbtn').click(function (event) {
        // prevent default form submission
        event.preventDefault();
        var otheruser = $('#other-user').data("username");

        console.log(otheruser);
        // get the message input field value
        var message = $('#message').val();


        // create a CSRF token using jQuery cookie plugin
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

        // send the message to the server using AJAX
        $.ajax({
            url: "/userchat/" + otheruser + "/",
            type: 'POST',
            data: {
                'message': message,
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function (response) {
                // clear the message input field
                $('#message').val('');
                console.log("responce", response);

                // append the new message to the chat container
                var chatMessage = $('<div class="chat-message sent"><p></p><span class="chat-time"></span></div>');
                chatMessage.find('p').text(response.message);
                console.log('time', response.timestamp)
                chatMessage.find('.chat-time').text(response.timestamp);
                $('.chat-messages').append(chatMessage);
                var chatContainer = $('.chat-messages');
                chatContainer.scrollTop(chatContainer.prop("scrollHeight"));

            },
            error: function (response) {
                console.log('error', response);
            }
        });
    });
});



//refresh
$(document).ready(function () {
    var otheruser = $('#other-user').data("username");

    // define a function to refresh the chat screen
    function refreshChat() {
        $.ajax({
            url: "/userchat/" + otheruser + "/",
            type: 'GET',
            success: function (response) {
                // replace the current chat container with the updated one
                $('.chat-messages').append($(response).find('.chat-messages'));

                // scroll to the bottom of the chat container
                $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
            },
            error: function (response) {
                console.log('error', response);
            }
        });
    }

    // check if the URL contains /userchat/ followed by a username
    if (window.location.pathname.match(/^\/userchat\/\w+\//)) {
        // call the refreshChat function every 5 seconds
        setInterval(refreshChat, 5000);
    }
});
