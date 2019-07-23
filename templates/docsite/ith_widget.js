function ituWidget() {
    function sendAction(actionName, data="") {
      let domainName = window.location.hostname;
      let path = window.location.pathname;
      let protocol = window.location.protocol;
      let payload = {
          path:  path,
          action: actionName,
          data: data
      };


      let url = protocol + '://{{ hostname }}/sites/' + domainName + '/action/new';
      console.log("Send request to " + url);

      $.ajax({
          url: url,
          method: 'POST',
          dataType: 'json',
          data: JSON.stringify(payload),
      });

    };

    sendAction('VIEW');
    $('#itu-widget').empty()
        .append('<p>Is this document helpful? <a id="is-helpful" href="">Yes</a> |<a id="is-not-helpful" href="">Not</a></p>');

    $('#is-helpful').click(function (event) {
        event.preventDefault();
        sendAction('HELPFUL');
        $('#itu-widget').empty()
            .append('<p>Thank you for the feedback. We’re really glad we could help!</p>')
            .append('<p>Powered by <a href="http://{{ hostname }}">IsThisHelpful</a> service.</p>')
    });

    $('#is-not-helpful').click(function (event) {
        event.preventDefault();
        $('#itu-widget').empty()
            .append('<p>Thank you for the feedback. How could we improve this document?</p>')
            .append('<div><textarea name="content"  cols="70" rows="5" class="textarea" id="not-helpful-comment"/></div>')
            .append('<input id="not-helpful-submit" type="submit" value="Submit"/>');

        $('#not-helpful-submit').click(function (event) {
            event.preventDefault();
            sendAction('NOT_HELPFUL', $('#not-helpful-comment').val());
            $('#itu-widget').empty()
                .append('<p>Thank you for the feedback. Your comments will help us improve our documents in the future.</p>')
                .append('<p>Powered by <a href="http://{{ hostname }}">IsThisHelpful</a> service.</p>')

        })
    });
}

