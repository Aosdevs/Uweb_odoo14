odoo.define('spiffy_theme_backend.userMenuJs', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;
    var UserMenu = require("web.UserMenu");

    var NewUserMenu = UserMenu.include({
        start: function () {
            this._super.apply(this, arguments);
            //greeting
            var session = this.getSession();
            var current_time_hr = new Date().getHours().toLocaleString("en-US", { timeZone: session.user_context.tz });
            if ((parseInt(current_time_hr) >= 6) && (parseInt(current_time_hr) < 12)){
                var greeting = "Good Morning"
            } else if ((parseInt(current_time_hr) >= 12) && parseInt(current_time_hr) <= 18) {
                var greeting = "Good Afternoon"
            } else {
                var greeting = "Good Evening"
            }
            this.$el.find('.dropdown-toggle .greeting').text(greeting)
        },
    });
});