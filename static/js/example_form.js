window.formd = (function(formd) {

    "use strict";

    var template = '<form id="myForm" action="<%= url %>" method="POST">\n\t<input name="token" type="hidden" value="<%= code %>" /><% _.each(placeholders, function(placeholder){ %>\n\t<input name="<%= placeholder %>" type="text" /><% }); %>\n\t<input type="submit" value="Submit form" />\n</form>'

    var example_form = function(data){
        $(document).ready(function(){
            var $example = $('#example_form');
            data.placeholders = [];
            $example.text(_.template(template, data));
        });
    };

    formd.example_form = example_form;

    return formd;
})(window.formd || {});