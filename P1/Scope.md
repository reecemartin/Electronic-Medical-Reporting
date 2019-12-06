**Learning Goals:**
- React JS
- Redux
- Importation and digestion of XML files
- Dynamic creation of HTML forms from structured files  (XML).
- Saving and retrieving structured files/data from a database
- Database Queries
- User authentication
- Test Driven Development
- Updating of structured files/data  in database

**Subset of Use Cases:**

_SDCTools Service_
- Get SDCForm for a DiagnosticProcedureID. Return the model object that represents a SDCForm in the client.
- Validate data entered in to a question. (called by clients to validate data entered into a field of a form)
    - Integer 
    - Decimal
    - String
- Create new SDCFormIterator, positioned at first node in form
- Get SDCFormNode at current position of SDCFormIterator
- Query if SDCFormIterator has a next node
- Position SDCFormIterator to next node
- Get questions of current node
- Get enabled state of node
- Get control node of a node
- Enter working answer for a node and propagate dependencies. (returns at least indication that dependencies have changed enabled state)
- Get list of dependent nodes of a given node (none if not control node)

_Actor Form Manager (administrator of forms)_
- Add SDC form to system. (Upload or otherwise import the XML file describing a form such that it is subsequently available to form fillers.)
- Delete form

_Actor Form Filler (Radiologist)_
- Assume only about a dozen radiology and pathology diagnostic procedures exist for this project.
- Fetch the form
- Search for form by diagnostic procedure eg: Cat Scan (CT) of the lung.
- Start new structured clinical note for patient, procedure.
- Render the form (HTML or React|Angular webapp etc. )
- User fills out form creating “form response”
- Save form response to (our prototype) enhanced EMR as structured clinical note, or “form response.
- Edit form response.
- Delete form response.
- Obtain external reference (URL?, #) to saved form response.

_Actor Form Receiver_
- View external reference to saved structured clinical note

From our learning goals listed above we have triaged the use cases to select a subset which will enable us to reach our goals. As we are not interested in email creation, we have left out the use cases which include its implementation. As our learning goals are shared between frontend and backend development our subset of use cases reflects this. For backend development we will focus on creating the apis using test driven development while using django’s database infrastructure to keep data persistent.
