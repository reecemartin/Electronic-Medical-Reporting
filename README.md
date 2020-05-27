# Electronic-Medical-Reporting:
This project comes from a University Class at the University of Toronto (CSC302: Engineering Large Software Systems). The team consisted of [Christopher Chiu](https://github.com/chr-chiu), [Kory McLean](https://github.com/Kory-McLean), [Ellen Chen](https://github.com/BlackSpade741), [Reece Martin](https://github.com/reecemartin) and Jayde Yue. Chris and Kory primarily worked on the frontend while Ellen, Reece, and Jayde did work for the backend. Code Review and some Fixes were done by everyone.

## What it does:
This project is developed to help doctors keep patient medical records using a standardized forms in XML file format defined by a third party. Our application ingests this XML, parses it, stores it, dynamically renders it, and allows for form filling the the associated actions with saved responses.

## How it was built:
The application was built as a Web-App with a Frontend composed of ReactJS with UI Components from Material UI and Routing with React Router. The Backend was created with Django and stores files in an SQLite Database.

## My Contribution:
My contributions to the project were primarily in the Frontend where I helped create the login page, and form upload functionality. I also played a significant role in the dynamic rendering or the forms.

## Notable Elements: 

### Recursive Rendering of Components
Due to the recursive organization of forms with questions and sections we were able to recursively render components in React which was something team members have long wanted to try but, never gotten around to. Recursive component rendering was a total success however we did face issues when using HOC or Higher Order Components recursively - particularly withStyles. We hope to investigate this further in the future.

### Dependent Questions
In the forms some questions have dependents, this means that some answers "trigger" follow-up questions. We chose to render the form such that these questions only appeared when the necessary "trigger" event happened. This required conditional rendering based on response data.

### Displaying the Correct Form Filling Control based on Context
When responding to the forms, some questions are binary choices (patient y has or does not have condition x), while other questions demand a response from a number of possible options. Due to this we had to render different input components from Material UI based on Question. For "multiple choice" questions with only one option we render a checkbox whereas for true multiple choice questions we render radio buttons.

## Images

### Fill Form
This is what users see when filling a form uploaded into the system.
![Fill Form](https://github.com/reecemartin/Electronic-Medical-Reporting/blob/master/Screenshots/Fill-Form.png?raw=true)

### Dependent Question Fill Form
This is what users see when a question response within a form triggers a dependent question.
![Dependent Question Fill Form](https://github.com/reecemartin/Electronic-Medical-Reporting/blob/master/Screenshots/Fill-Form-Dependent-Question.png?raw=true)

### Response Browse
This is the Response Browse page which allows for the viewing of "Responses" or filled forms.
![Response Browse](https://github.com/reecemartin/Electronic-Medical-Reporting/blob/master/Screenshots/Response-Browse.png)

### View Form
This is what users see when viewing a form uploaded into the system.
![View Form](https://github.com/reecemartin/Electronic-Medical-Reporting/blob/master/Screenshots/View-Forms.png)

### View Response
This is what users see when viewing a response uploaded into the system.
![View Response](https://github.com/reecemartin/Electronic-Medical-Reporting/blob/master/Screenshots/View-Response.png?raw=true)

### View Response Dependent Question
This is what users see when a response uploaded into the system includes dependent questions.
![View Response Dependent Question](https://github.com/reecemartin/Electronic-Medical-Reporting/blob/master/Screenshots/View-Response-Dependent-Question.png?raw=true)

