Is This Helpful?
================

Is This Helpful (ITH) is a simple web service to get feedback about your online documentation.

Usage
-----

Register the domain name of your documentation site on `ThisIsUseful <https://is-this-helpful.herokuapp.com>`_ and add the following code to your HTML template:

::

  <head>
    .....
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script src="https://is-this-helpful.herokuapp.com/ith_widget.js"></script>
    ....
  </head>
  <body>
    ....
    <div id="ith-widget"></div>
    <script>
      ithWidget();
    </script>
    ....
  </body>

Project Status
--------------

Very very alpha.
