window.formd = (function(formd) {

    "use strict";

    var template = '<form id="myForm" action="<%= url %>" method="POST">\n\t<input name="token" type="hidden" value="<%= code %>" /><% _.each(placeholders, function(placeholder){ %>\n\t<label for="#id_<%= placeholder %>"><%= placeholder %></label>\n\t<input name="<%= placeholder %>" id="id_<%= placeholder %>" type="text" /><% }); %>\n\t<input type="submit" value="Submit form" />\n</form>'

    var example_form = function(data){
        $(document).ready(function(){
            var $example = $('#example_form');
            var render = (function render() {
                var placeholders = $('#id_template').val().match(/{{\s*[\w\.]+\s*}}/g)
                if(placeholders) {
                    placeholders = placeholders.map(function(x) { return x.match(/[\w\.]+/)[0]; });
                }
                data.placeholders = _.uniq(placeholders);
                $example.text(_.template(template, data));
                return render;
            }());
            $('#id_template').on('keyup', render);
        });
    };

    formd.example_form = example_form;

    return formd;
})(window.formd || {});