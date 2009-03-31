/*
*	Sharer
*	A reusable JS class for providing AJAX functionality to Sharer
*	
*	Requires jQuery library (http://www.jquery.com) with 
*   jQuery.Class plug-in (http://github.com/taylanpince/jquery-class)
*	
*	Taylan Pince (taylanpince at gmail dot com) - March 30, 2009
*/

$.namespace("core.Sharer");

core.Sharer = $.Class.extend({
    
    active : false,
    widget : null,
    link : null,
    url : "",
    title : "",
    
    link_template : '<a href="javascript:void(0);">%(copy)</a>',
    
    link_copy : 'Share',
    
    render_template : function(template, values) {
        for (val in values) {
            var re = new RegExp("%\\(" + val + "\\)", "g");
        
            template = template.replace(re, values[val]);
        }
    
        return template;
    },
    
    toggle_widget : function(evt) {
        if (this.active) {
            this.active = false;
            
            $(this.widget).slideUp("fast");
        } else {
            this.active = true;
        
            var pos = this.link.offset();
        
            $(this.widget).css({
                top : (pos.top + 20) + "px",
                left : pos.left + "px"
            }).slideDown("fast");
        }
    },
    
    close_widget : function(evt) {
        if (this.active && $(evt.target).parents().index(this.widget) == -1 && evt.target != this.link.get(0)) {
            this.active = false;
            
            $(this.widget).slideUp("fast");
        }
    },
    
    init : function(selector, options) {
        this.widget = $(selector).removeClass("share-box").addClass("share-widget").get(0);
        
        if (options) {
            for (opt in options) {
                this[opt] = options[opt];
            }
        }
        
        this.link = $(this.render_template(this.link_template, {
            copy : this.link_copy
        })).insertBefore(this.widget).click(this.toggle_widget.bind(this));
        
        $("html").click(this.close_widget.bind(this));
    }
    
});
