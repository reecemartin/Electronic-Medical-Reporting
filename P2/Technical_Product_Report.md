**Technical Product Report**

**What did you actually build during this phase?**

For phase 2 we focused on being able to view forms and form responses. In order to achieve this we implemented front end views along with a main api and services. We were able to implement the following functionalities:
- View forms
    - View a specific form by its form id
    - View all forms as a list and be able to click into a specific form to view it
 
- View form responses
    - View a specific form response (Created by clinician)
    - View all form responses (created by clinician) and be able to click into a specific response to view it
- Upload Forms
    - Upload an XML file which specifies a form

We originally proposed to have parsing and viewing of forms done by this phase, which we were successful in implementing. However,  we originally proposed viewing, editing and filling of form responses but we were limited to only successfully implementing the viewing of form responses. This limitation is a result of external factors outside the scope of this course (other work from other courses) along with an underestimation of the available time our team will have to implement our proposed functionalities. 

**High-level design of your software.**

**_Front End:_**

The design of the Frontend follows the React Guidelines and is fully component based. The multiple pages are supported using React Router which the Frontend team has existing experience with. React Router based in App.js manages the routing on the main component of each page, it also defines routes for the pages other components and is highly modular to enable work in Phase 3. App.js is the single entry point for data from the Backend APIs, data used in individual components is therefore fed to them when rendered by App.js. This architecture greatly simplifies updates and changes across our API and frontend. 


**_Back End:_**

The design of our backend api and services generally follow our proposals from Phase 1, with some revision. Our backend is split into three main components:

- _The Main API:_
This component is the main contact point for our front end. This component is responsible for taking a request from the front end and by utilizing our two services fulfil the response. It also has the responsibility of creating an appropriate json object to represent a form response object. Apart from creating appropriate json object to represent objects, this service is mostly used as a pass through service. The aim of this was to have a single point of contact for our front end team members to lower the chance of confusion.

- _The Form Admin Service:_
This component is responsible for the administration of forms. Administration of forms include the creation, delete and retrieval of forms. Form creation is done by parsing xml files in order to create an appropriate form object. Form deletion and the retrieval of forms is done utilizing the Django framework based on data passed into the request. This is the service which is used by the main api for requests that relate to forms.

- _The Form Response Service:_
This component is responsible for the our form responses. It has the responsibilities of creating form response from a submission, deletion of form responses and the retrieval of form responses. Form response creation is done by parsing the passed in requests’ json body to create appropriate form response objects. Form response deletion and the retrieval of form responses is done utilizing the Django framework based on data passed into the request.

Each of these three components was implemented using test driven development (to be discussed later) therefore each of these services have a test suite which relates to the respective service.
 
**Technical highlights:**

- _Test driven development_
    - Though when implementing our project we aimed and succeeded in using test driven development, we had differences in the way test driven development is followed/done. Some members wrote whole tests first then coded implementation, while other built up the tests line by line with incremental code implementation. Though it was not a severe issue it was interesting to see that something as popular as test driven development had many ways of its actually implementation.

- _Cross communication between form admin and form response services_
    - When implementing the creation of form responses, we wanted to return a json object which represents the form response. This required us to be able to get the structure of the corresponding form in order to build an appropriate json object by querying the form database table for the corresponding form. However, as the form object models are stored in the form table and ‘belonged’ to the form admin service we were not able to get the appropriate corresponding form. We say belong as we were not able to get access to the form table from the form response service as the model which defines the form objects were specified in the form admin service. This is due to constraints placed on us by the Django framework. As we wanted to keep responsibilities separate we did not want the form response service to access the form admin service’s stored data objects. This was an unexpected severe issue. In order to resolve this we moved the creation of json objects to represent form responses into the main api, as it would be able to use the form admin service to get the corresponding form and use the form response service to get the form response objects.
			
- _Provided XML files_
    - When implementing the parsing of xml files into form objects in the form admin service we noticed that all the provided XML files were somewhat in the same structure but many contained different complexities in their structure. Examples of these different complexities are forms with sections which have subsections and forms with dependent questions. There were also ‘flat’ (no subsections) forms provided. As we were provided with many different XML files which can vary in their structure, when implementing parsing we did it in three levels of complexities: Simple or ‘flat’ forms, forms with sections which contain subsections and forms which have questions with dependent questions. In order to avoid having to parse for every possible case of XML structure, we assumed that any form’s structure can be made up of the three previously mentioned complexities. This leveling of complexities can be seen through our test suite for the form admin service as we have tests for each of the complexity levels.
    
- _Travis CI_ 
    - Our use of Travis CI allowed us to get the full utility of our test suites as it allowed us to have a sanity check when pushing and merging into master. We did experience some teething issues when setting up Travis CI on our repository but these mainly had to do with ensuring our temporary db which is created when running our tests by Django contained the correct schema by creating and applying migrations.
 
**Teamwork and process**

- _**Successes**_
    - _Team Communication_ - Though we initially desired to use either Discord or Slack, we found it more convenient to use our Facebook group chat as it was more convenient and with the ability to have access to Facebook on our phones allowed for faster communication.
 
    - _Team Meetings_ - As planned we aimed to meet at least once a week with our main meeting day being Monday during lecture time. However, we found that it was more likely for all team members to be on campus around the Friday tutorial time. This lead to us changing our main meeting day to Friday. See the meetings attendance artifacts. 
 
    - _Division into Front End and Back End teams_ - This decision was very successful, as it allowed for our members to focus on particular parts of our overall project without having to jump between the front end and back end. This also provided more flexibility as if a particular team member for a subteam was unreachable we had other members who would be able to assist.
 
    - _Pull Requests_ - Our intended and followed git workflow involved having separate non-master branches and using pull requests to merge them into master. This was successful as it allowed for members of the sub teams to review changes before they went into master, as well as squashing the multiple commits for the implementation of functionalities into a single commit into master, making the process of rolling back to a commit easier if necessary. See the pull request artifacts to view all of our pull requests
 
- _**Improvements**_

    - _Division into Front End and Back End teams_ - One improvement we can make is to ensure that both teams respectively have at least some context of what the other team has implemented. This would allow us to have better synergy between the teams. Although we communicated well, we had a couple of issues where functionalities seemed to be broken when it was just the case that we were misusing the implementation of the functionality. We could improve on this by having doc strings for the respective implementations and better commit messages and pull request comments.
 
    - _Verbal vs Written communication_ - Though we met in person and verbally communicated during these meetings, the majority of our communication took place on our Facebook chat. The benefits of written communication in our chat is that we were able to refer back to things mentioned in the past as we had a source of history of conversation. However, when we met in person the same could not be said. We were not able to have a source of history of conversation for our meetings which meant things could be forgotten. This can lead to confusion and may even result in forgetting to implement functionalities that we said we were gonna do in the meeting. To improve on this we could have a brief meeting summary in the meeting attendance sheet in which we can write what we discussed in the meeting, providing a source of history of conversation. This would give us the benefits of written communication for our verbal communications.
 
 - **Artifacts**
 
    - _Pull Requests_ - https://github.com/csc302-fall-2019/proj-coolcats/pulls?q=is%3Apr+is%3Aclosed
    
    - _Team Meetings_ - https://docs.google.com/spreadsheets/d/1SHsxBn_DrtOCVjFlYrCz0SOZ7vItqV1VKr7SBkUp498/edit?usp=sharing 
    
**Triage**

For phase 3 we aim to have the following complete:

- User filling of forms to create form responses
- Editing of pre-existing form responses
- Creation of url links to access form responses (external links)

If successful, this would allow us to be able to create, view, edit and delete both forms and form responses along with being able to create external links to directly view a saved form response.

_Front End Details:_

For Phase 3, the goal for front end is to complete the functionality of selecting a form, filling it, and saving the response to the back end, as currently the front end has the capability to view forms and view already filled responses, but no way to bridge between the two. We also want to clean up routing, implement better authentication for our routes, and up our test coverage.

_Back End Details:_

- Create endpoint to allow the editing of pre-existing form responses
- Create an endpoint to create and retrieve an external url link to view a form response
