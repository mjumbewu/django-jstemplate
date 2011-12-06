(function(Mustache) {
    var CachedTemplate = function(template) {
        var self = this;

        /*
          The text of the template.
        */
        self.template = template;

        /*
          Turns this template into HTML using the given view data.
        */
        self.render = function(view, partials, send_fun) {

            // Use either the parials specified, or the entire set of templates
            // stored in Mustache.TEMPLATES
            partials = partials || Mustache.TEMPLATES;

            return Mustache.to_html(self.template, view, partials, send_fun);
        };
    };

    /*
      Creates a new Template object.
    */
    Mustache.template = function(name) {
        var template = Mustache.TEMPLATES[name];
        return new CachedTemplate(template);
    };

})(Mustache);
