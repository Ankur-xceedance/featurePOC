ko.validation.init({
    registerExtenders: true,
    messagesOnModified: true,
    insertMessages: true,
    parseInputAttributes: true,
    errorClass: 'error',
    messageTemplate: null
}, true);

function FeatureRequestViewModel(data){
	var THIS = this;
	THIS.Title= ko.observable(data.title);
	THIS.Desc= ko.observable(data.desc);
	THIS.Client= ko.observable(data.client);
	THIS.Priority= ko.observable(data.priority);
	THIS.TargetDate= ko.observable(data.target_date);
	THIS.ProductArea= ko.observable(data.product_area);
	THIS.Status= ko.observable(data.status);
}

function pocViewModel(){
	var self = this;
	this.validateNow = ko.observable(false);
	this.title = ko.observable().extend({  
            required: { message: '*Title is mandatory' }
        })
	this.clients = ko.observableArray()
	this.client_id = ko.observable().extend({  
            required: { message: '*Client is mandatory' }
        })
	this.priority = ko.observable().extend({  
            required: { message: '*Priority is mandatory' }
        })
	this.target_date = ko.observable().extend({
			required: { message: 'Target Date is mandatory' }, 
			validation: {
				validator: function (val) {
					val = val.replace(/-/g,'/')
					return new Date(val) > new Date();
				},
				message: "Target date should be greater than today's date",
			}
		});
	this.products = ko.observableArray();
	this.product_id = ko.observable().extend({  
            required: { message: '*Product is mandatory' }
        })
	this.desc = ko.observable().extend({  
            required: { message: '*Description is mandatory' }
        })
	this.error_add = ko.observable();
	this.error_list = ko.observable();
	this.feature_request = ko.observableArray([]);
	this.errors = ko.validation.group(this);
	
	var client_data;
	var product_data;
	var feature_add_details = {
		title: self.title,
		desc: self.desc,
		client_id: self.client_id,
		priority: self.priority,
		target_date: self.target_date,
		product_id : self.product_id
	};
	
	$.ajaxSetup({
		async: false,
		contentType: "application/json; charset=utf-8"
	});
	$.getJSON("requests", function(data) {
		self.feature_request($.map(data.feature_request, function (item) {
            return new FeatureRequestViewModel(item);
		}));
		client_data = data.clients;
		product_data = data.products;
	})
	this.clients = ko.observableArray(client_data);
	this.products = ko.observableArray(product_data);
	self.ClearValues = function()
	{
		self.title(null);
		self.desc(null);
		self.client_id(null);
		self.priority(null);
		self.target_date(null);
		self.product_id(null);
	}
	
	self.submit = function () {
		self.validateNow(true);
		var result;
		if (self.errors().length === 0) {
			var feature_json = ko.toJSON(feature_add_details);
			$.post("addrequest", feature_json, function(returnedData) {
				result = returnedData[0]
				var data = returnedData[0];
				array_data = [
								data.title,
								data.desc,
								data.client,
								data.priority,
								data.target_date,
								data.product_area,
								data.status
							]
				$('#requests').DataTable().row.add(array_data).draw(false);
				self.ClearValues();
				self.errors.showAllMessages(false);  
			})
		}else{
			self.errors.showAllMessages();
            return;
		}
	}
}

ko.applyBindings(new pocViewModel());