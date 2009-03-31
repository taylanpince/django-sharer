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
    form : null,
    url : "",
    title : "",
    
    offset_left : 0,
    offset_top : 0,
    
    wrapper_template : '<div class="share-networks"></div>',
    form_template : '<div class="share-form"></div>',
    link_template : '<a href="javascript:void(0);" class="share-link">%(copy)</a>',
    error_template : '<p class="%(type)">%(message)</p>',
    cancel_template : '<input type="button" value="%(copy)" />',
    
    link_copy : 'Share',
    cancel_copy : 'Cancel',
    email_success_copy : 'Your email has been sent. Thank you!',
    email_failure_copy : 'There was an error with your request. Please try again.',
    
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
                top : (pos.top + this.offset_top) + "px",
                left : (pos.left + this.offset_left) + "px"
            }).slideDown("fast");
        }
    },
    
    close_widget : function(evt) {
        if (this.active && $(evt.target).parents().index(this.widget) == -1 && evt.target != this.link.get(0)) {
            this.active = false;
            
            $(this.widget).slideUp("fast");
        }
    },
    
    show_networks_panel : function() {
        $(this.widget).removeClass("share-widget-form").find("div.share-form").hide();
        $(this.widget).find("div.share-networks").show();
    },
    
    load_email_form : function(evt) {
        $(this.widget).find("div.share-networks").hide();
        $(this.widget).append(this.form_template).addClass("share-widget-form");
        
        if (this.form) {
            $(this.widget).find("div.share-form").show();
        } else {
            $(this.widget).find("div.share-form").load(
                $(evt.target).attr("href"),
                this.process_email_form.bind(this)
            );
        }
        
        return false;
    },
    
    process_email_form : function() {
        this.form = $(this.widget).find("form").submit(this.submit_email_form.bind(this));
        
        $(this.render_template(this.cancel_template, {
            copy : this.cancel_copy
        })).appendTo(this.form.find("li.submit")).click(this.show_networks_panel.bind(this));
    },
    
    submit_email_form : function(evt) {
        $(this.widget).find("p.error, p.success").fadeOut("slow");
	    this.form.find("input[type=submit], input[type=image]").attr("disabled", true);
	    
        $.ajax({
            url : this.form.attr("action"),
            type : "POST",
            processData : false,
            data : this.form.serialize(),
            dataType : "json",
            contentType : "application/json",
            success : this.parse_email_form.bind(this),
            error : this.fail_email_form.bind(this)
        });
        
        return false;
    },
    
    parse_email_form : function(data) {
        if (data.errors) {
	        for (error in data.errors) {
	            if (error == "__all__") {
	                for (e in data.errors[error]) {
        	            this.form.prepend(this.render_template(this.error_template, {
        	                "message" : data.errors[error][e],
        	                "type" : "error"
        	            }));
	                }
	            } else {
    	            this.form.find("[name*=" + error + "]").parent().prepend(this.render_template(this.error_template, {
    	                "message" : data.errors[error],
    	                "type" : "error"
    	            }));
	            }
	        }
	    } else {
	        $(this.widget).find("div.share-networks").prepend(this.render_template(this.error_template, {
                "message" : this.email_success_copy,
                "type" : "success"
            }));
	        
	        this.show_networks_panel();
	    }
	    
	    this.form.find("input[type=submit], input[type=image]").attr("disabled", false);
    },
    
    fail_email_form : function() {
        this.form.prepend(this.render_template(this.error_template, {
            "message" : this.email_failure_copy,
            "type" : "error"
        }));
    },
    
    init : function(selector, options) {
        this.widget = $(selector).removeClass("share-box").addClass("share-widget").get(0);
        
        if (options) {
            for (opt in options) {
                this[opt] = options[opt];
            }
        }
        
        $(this.widget).wrapInner(this.wrapper_template);
        
        this.link = $(this.render_template(this.link_template, {
            copy : this.link_copy
        })).insertBefore(this.widget).click(this.toggle_widget.bind(this));
        
        $(this.widget).find("a.share-email").click(this.load_email_form.bind(this));
        
        $("html").click(this.close_widget.bind(this));
    }
    
});
