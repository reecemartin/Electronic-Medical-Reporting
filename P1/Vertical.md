_(The vertical slice of our app that we decided to implement is the login process. )_

_Backend:_

In the back end, we implemented the main api which serves the client service and communicates with the other 2 sub services with 2 simple endpoints. One GET endpoint which returns all the users saved in the system. The second endpoint was a POST endpoint which takes in a username and password and passes it along to django’s built in authentication feature. Then based on the result of the django authentication we return a bool and a username representing whether or not the authentication was successful as JSON in the response body.

In addition to these endpoints we also implemented unit tests which tests the logic built into our two endpoints. These are implemented using django’s built in testing feature.

_Frontend:_

In the front end, we implemented a login page with an email and password entry box.
The whole application sits within a main component named App, which stores application-wide state and interacts with the backend API. App contains an async function named signIn() that takes in an email and password, then uses the fetch API to send them to the back end with JSON, and waits for a response to see if the login is successful. If the login was successful, then the state of App is updated to be logged in, and the current user name is stored, and the function returns true. If the login was unsuccessful, the function returns false.

The login page is implemented in a component named Login, which deals with the rendering of the page as well as the interaction with users. The currently entered email and password are stored in Login’s state, and LoginPage also implements an onSubmit handler for the submit button. As the user types into the email TextField, Login validates the user's input, and if the input is not a valid email, the TextField will have a red outline indicating error. When the submit button is pressed, onSubmit sends the entered username/email and password back to App using the signIn() function that was passed to Login with props. If the login was successful, the user is redirected to the next home page of the application. If the login was unsuccessful, or the user tries to log in with an invalid email, an error message pops up informing user of the error. 

In addition to the pages, we implemented some tests for our login page using Jest and Enzyme (as described in test.md). The tests test for the error state of TextField if an invalid input is entered, and the error message if an invalid input is submitted. 

**Instructions for vertical slice:**

_Backend:_
To run our main api, execute the following commands:

- $ git clone https://github.com/csc302-fall-2019/proj-coolcats.git
- $ cd proj-coolcats/backend
- $ python3 manage.py migrate
- $ python3 manage.py runserver

You should now be able to access our API’s endpoints via the client service.

_Frontend:_
To run our client, first ensure you have node & npm installed, then execute the following commands:

- $ git clone https://github.com/csc302-fall-2019/proj-coolcats.git
- $ cd proj-coolcats/frontend
- $ npm install
- $ npm start

You should now be able to access the client at http://localhost:3000.

To run tests on the client, execute the following command in /frontend:

- $ npm run test

The jest test runner should now be running, and automatically execute all test suites. 
