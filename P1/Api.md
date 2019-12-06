_( The lists below are subject to change as we implement but they represent our initial thoughts on the endpoints needed)_

We've decided to create 3 service APIs. The reasons being is we wanted to have seperate services which dealt with creating and handling forms (the form administrator service), handling form responses (the form response service) and one which communicates between the other two and the client web app service (the main API). This would allow us to have seperation of responsibilities while ensuring modularity of our implementation. This would also allow us to have seperate test suites for each major functionality we intend to implement.

**Main API Endpoints:**

_POST_ /api/login: Receives the username and password in the request body as JSON, returns a JSON object containing a bool success that indicates success of login, and a string username representing the user that is logged in. 

_POST_ /api/addForm: Receives the to be added forms XML in the body and then uses the form administrator sub service to parse the XML and save the resulting form in the form db.

_DELETE_ /api/deleteForm: Receives the id of a form to delete from the form db in the request body as JSON. Utilizes the administrator sub service to delete the form from the db.

_GET_ /api/getFormByID: Receives the id of a form to return from the form db in the request body as JSON. Utilizes the administrator sub service to search for the form and to return it if found.

_GET_ /api/getFormResponseByID: Receives the id of a response to return from the response db in the request body as JSON. Utilizes the response sub service to search for the response and to return it if found.

_DELETE_ /api/deleteFormResponse: Receives the id of a form response to delete from the form response db in the request body as JSON. Utilizes the response sub service to delete the form response from the db.

_POST_ /api/saveFormResponse: Receives a form response as JSON in the request body and utilizes the response sub service to save the response whether it is a new response or an updated one. 

_GET_ /api/getExternalURL: Receives the id of a response to return from the response db in the request body as JSON. Utilizes the response sub service to search for the form and return it’s external reference url.

**Form Administration service Endpoints:**

_POST_ /formAdmin/addForm: Receives the to be added forms XML in the request body, then parses the XML and saves the resulting form object in the form db.

_DELETE_ /formAdmin/deleteForm: Receives the id of a form to delete from the form db in the request body as JSON.

_GET_ /formAdmin/getFormByID: Receives the id of a form to return from the form db in the request body as JSON. Searches for the form and returns it if found.

**Form Responses service Endpoints:**

_GET_ /formResponse/getFormResponseByID: Receives the id of a response to return from the response db in the request body as JSON. Searches for the response and returns it if found.

_DELETE_ /formResponse/deleteFormResponse: Receives the id of a form response to delete from the form response db in the request body as JSON.

_POST_ /formResponse/saveFormResponse: Receives a form response as JSON in the request body and then saves the response in the response db. 
