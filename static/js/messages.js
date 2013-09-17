window.formd = (function(formd){

    "use strict";

    var messages = function() {
        $(document).ready(function(){
            var message_list = $('#messages');
            if($('li', message_list).length > 0) {
                window.setTimeout(function(){message_list.slideUp()}, 3000);
            }
        });
    }

    formd.messages = messages;

    return formd;

})(window.formd || {});