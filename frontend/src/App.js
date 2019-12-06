import React, { Component } from "react";
import Header from "./Components/Header/Header";
import Login from "./Components/Login/Login";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import "./App.css";
import FormBrowse from "./Components/FormBrowse/FormBrowse";
import ResponseBrowse from "./Components/ResponseBrowse/ResponseBrowse";
import FormView from "./Components/FormView/FormView";
import sampleResponse from "./sampleForms/sampleResponse";
import sampleForm from "./sampleForms/sampleForm";
import NotFound from "./Components/404/NotFound";
import ResponseView from "./Components/ResponseView/ResponseView";
import FillResponseView from "./Components/FillResponse/FillResponseView";

const testing = false;

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loggedIn: false,
      currentUser: "",

      formsList: [],
      responseList: [],
      currentForm: null
    };

    this.loadForms().then(forms => {
      console.log(forms);
      this.setState({ formsList: forms });
      console.log(this.state);
    });

    this.loadResponses().then(responses => {
      console.log(responses);
      this.setState({ responseList: responses });
    });

    this.signIn = this.signIn.bind(this);
    this.getForm = this.getForm.bind(this);
    this.uploadForm = this.uploadForm.bind(this);
    this.getResponse = this.getResponse.bind(this);
    this.saveResponse = this.saveResponse.bind(this);
  }

  async loadForms() {
    const r = await fetch("/api/get_all_forms/");
    return await r.json();
  }

  async loadResponses() {
    const r = await fetch("/api/get_all_form_responses/");
    console.log(r);
    return await r.json();
  }

  async getForm(id) {
    if (testing) return sampleForm;
    console.log("getform, id=" + id);
    const r = await fetch("/api/get_form_by_id/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json;charset=utf-8"
      },
      body: JSON.stringify({
        form_id: id
      })
    });

    const form = await r.json();
    console.log(form);
    return form;
  }

  async getResponse(formId, patientId, fillerId) {
    console.log(
      "getResponse, formId=" +
        formId +
        ", patientId=" +
        patientId +
        "fillerId=" +
        fillerId
    );

    if (testing) return sampleResponse;

    const r = await fetch("/api/get_form_response/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json;charset=utf-8"
      },
      body: JSON.stringify({
        form_id: formId,
        patient_id: patientId,
        filler_id: fillerId
      })
    });

    const response = await r.json();
    console.log(response);
    return response;
  }

  async uploadForm(form) {
    console.log("[App] uploadForm");
    console.log(form);

    try {
      // get string from form
      const formStr = await form.text();
      console.log(formStr);

      const response = await fetch("/api/add_form/", {
        headers: {
          "Content-Type": "application/json;charset=utf-8"
        },
        method: "POST",
        body: JSON.stringify({ form: formStr })
      });
      const result = await response.json();
      console.log("Success:", JSON.stringify(result));
      // repopulate forms list after upload
      this.loadForms().then(forms => {
        console.log(forms);
        this.setState({ formsList: forms });
        console.log(this.state);
      });
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async saveResponse(response) {
    // assume response has same structure as needed besides filler id
    if (this.state.currentUser === "") return false;
    if (response.response === undefined) return false;

    console.log("[App] uploadResponse");
    console.log(response);

    // send the response to the backend
    let res = await fetch("/api/submit_form_response/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json;charset=utf-8"
      },
      body: JSON.stringify(response)
    });
    console.log(res);
    if (res.status !== 200) return false;

    // repopulate responses list after upload
    const responseList = await this.loadResponses();
    console.log(responseList);
    this.setState({ responseList: responseList });
    console.log(this.state);

    return true;
  }

  async signIn(username, password, remember) {
    console.log("App.signIn()");

    let response = await fetch("/api/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json;charset=utf-8"
      },
      body: JSON.stringify({
        username: username,
        password: password,
        remember: remember
      })
    });
    console.log(response);

    if (response.ok) {
      response.json().then(body => {
        console.log(body.username);

        if (body.username) {
          console.log("Log in successful");
          this.setState({
            loggedIn: true,
            currentUser: body.username
          });
          console.log(this.state);
          return true;
        } else {
          console.log("Log in unsuccessful");
        }
      });
    }
    return false;
  }

  render() {
    return (
      <Router className="app">
        {/* Route for header, should not appear on home page */}
        <Route
          path={[
            "/forms/browse",
            "/responses/browse",
            "/form/:id",
            "/response/:formId/:patientId/:fillerId"
          ]}
        >
          <Header></Header>
        </Route>

        {testing ? (
          <Route
            exact
            path="/form/:id/fill"
            render={props => (
              <FillResponseView {...props} getForm={this.getForm} />
            )}
          />
        ) : (
          <></>
        )}

        {/* Route for pages */}

        <Switch>
          <Route path="/404" component={NotFound} />

          {/* If  user not logged in, redirect back to home page */}
          {this.state.loggedIn && !testing ? (
            <>
              <Route
                exact
                path="/forms/browse"
                render={props => (
                  <FormBrowse
                    {...props}
                    forms={this.state.formsList}
                    username={this.state.currentUser}
                    uploadForm={this.uploadForm}
                  />
                )}
              />
              <Route exact path="/forms">
                <Redirect to="/forms/browse" />
              </Route>
              <Route exact path="/responses/browse">
                <ResponseBrowse responses={this.state.responseList} />
              </Route>
              <Route exact path="/responses/browse/success">
                <ResponseBrowse
                  responses={this.state.responseList}
                  showSuccess
                />
              </Route>
              <Route exact path="/responses">
                <Redirect to="/responses/browse" />
              </Route>
              <Route
                exact
                path="/form/:id"
                render={props => <FormView {...props} getForm={this.getForm} />}
              ></Route>
              <Route
                exact
                path="/response/:formId/:patientId/:fillerId"
                render={props => (
                  <ResponseView
                    {...props}
                    getResponse={this.getResponse}
                    getForm={this.getForm}
                  />
                )}
              ></Route>
              <Route
                exact
                path="/form/:id/fill"
                render={props => (
                  <FillResponseView
                    {...props}
                    getForm={this.getForm}
                    saveResponse={this.saveResponse}
                    fillerId={this.state.currentUser}
                  />
                )}
              />
            </>
          ) : (
            <>
              <Route exact path="/">
                {this.state.loggedIn ? (
                  <Redirect to="/forms" />
                ) : (
                  <Login signIn={this.signIn} loggedIn={this.state.loggedIn} />
                )}
              </Route>
            </>
          )}
        </Switch>

        {/* If logged in, redirect to forms */}
        {this.state.loggedIn && !testing ? <Redirect to="/forms" /> : <></>}
      </Router>
    );
  }
}

export default App;
