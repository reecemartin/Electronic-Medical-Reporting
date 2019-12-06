**Front end (ReactJS):**

The front end of our app will be built using JavaScript and React, for their flexibility, modularity, and reusability. We will be using Material UI, a component package that provides pre-built UI components that can easily be inserted into our application for quick and beautiful UI layout. 

The main business logic of the client side app will be contained in App.js, which handles interaction with the back end server, storage of state information, as well as routing for the different pages. The state stored will include the current logged in user, cached forms and form responses, and any other information useful in the app. To communicate with the backend, we will be using the built-in Ajax & fetch API. 

Each page of the application will have its own component that deals with its rendering and individual state-keeping for state that is only used on that page/in that component. These pages will use props to communicate with App, where App passes callback functions for the page component to call when an interaction needs to be done.

**Back end (Django):**

The back end of our app will be divided up into different services communicating all utilizable through our main api service. We will be implementing a service for each of the following main functionalities:

- Communicating to our front end service via a main service API
- Form Administration such as XML Parsing and form object creation and handling
- Form Response handling such as saving, searching, deleting and fetching

The backend will be implemented using django’s rest framework due to many useful self contained features such as unit testing and admin dashboard to monitor and manage the database.

By splitting our backend implementation into these multiple services allows our system to have seperate concise test suits for each service along with higher separation of responsibilities. It also allows us to modularize our backend to allow for easier sharing of duties among the group. By having separate services for each of our main functionalities we are able to have group members work on separate areas without a high chance of collision or conflicts which will aid us in our workflow throughout the project.
