**Backend:** 

For the testing of backend main api and sub services we will be utilizing django’s built in testing functionality. We will be implementing our backend using test driven development in order to have our test suite grows as we implement functionality and to ensure high test coverage. The majority of our tests will be tests which call an endpoint with input and then analyse the output for expected results.

Functionalities which involve logic will be those who are mainly tested, as we do not want to unnecessarily test django’s framework, but we want to test how we are utilizing it. We will also set up Travis CI on our repository increased confidence and integrity when we are merging changes. 

**Frontend:** 

The frontend client app will be tested using Jest and Enzyme using snapshot and DOM tests that capture the expected behaviour of the frontend client app and the rendered components in the DOM tree in a file, and whenever the tests are run, are compared to the actual output of the client app. Jest is used as a test runner, which is already built into our frontend app bundled by create-react-app. Enzyme is a DOM-manipulation package that allows us to see and manipulate individual components inside the DOM so we can test them. 

The components of the frontend that will be particularly tested will be the form rendering components (testing whether the form and all the questions in it render correctly), as well as the routing of each page and authentication to make sure only users with the correct access can access some particular pages. 
