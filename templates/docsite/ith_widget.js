function ituWidget() {
    function sendAction(actionName) {
      let domainName = window.location.hostname;
      let path = window.location.pathname;
      let payload = {
        path:  path,
        action: actionName,
      }

      $.ajax({
          url: 'http://{{ hostname }}/sites/' + domainName + '/action/new',
          method: 'POST',
          dataType: 'json',
          data: JSON.stringify(payload),
      }).done(function () {
          alert('Hi!')
      });

    };

    sendAction('VIEW');
}

