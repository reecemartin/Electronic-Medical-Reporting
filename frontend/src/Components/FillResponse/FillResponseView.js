import React, { Component } from "react";
import { withStyles } from "@material-ui/core/styles";
import FillResponseQuestion from "./FillResponseQuestion";
import FillResponseSection from "./FillResponseSection";
import Typography from "@material-ui/core/Typography";
import { Redirect } from "react-router-dom";
import Button from "@material-ui/core/Button";
import ErrorBar from "../StatusBar/ErrorBar";

const styles = {
  fillResponseView: {
    padding: "10px"
  },
  freeQuestions: {
    padding: "10px"
  },
  saveButton: {
    margin: "10px"
  }
};

class FillResponseView extends Component {
  constructor(props) {
    super(props);

    this.state = {
      form: null,
      loading: true,
      notFound: false,
      errorSaving: false,
      saved: false,
      saving: false
    };

    this.sectionAnswers = [];
    this.freeQuestionAnswers = {};
    this.responseInfo = {
      form_id: "",
      patient_id: "",
      filler_id: this.props.fillerId
    };

    if (props.match.params.id != null) {
      this.getForm(props.match.params.id);
    }

    this.handleSectionChanged = this.handleSectionChanged.bind(this);
    this.handleAnswerChanged = this.handleAnswerChanged.bind(this);
    this.handlePatientIdChanged = this.handlePatientIdChanged.bind(this);
    this.onSaveButtonClicked = this.onSaveButtonClicked.bind(this);
  }

  async onSaveButtonClicked(e) {
    e.preventDefault();
    this.setState({
      saving: true
    });

    // send data to backend
    const filledResponse = {
      sections: this.sectionAnswers,
      free_questions: this.freeQuestionAnswers,
      response: this.responseInfo
    };

    if (this.responseInfo.patient_id === "") {
      this.setState({
        errorSaving: true,
        saving: false
      });
      return;
    }

    const res = await this.props.saveResponse(filledResponse);

    this.setState({
      errorSaving: !res,
      saved: res,
      saving: false
    });
  }

  handlePatientIdChanged(patient_id) {
    this.setState({
      errorSaving: false
    });
    this.responseInfo.patient_id = patient_id.answer_content;
    // console.log(this.responseInfo);
  }

  handleSectionChanged(id, sectionAnswers) {
    this.setState({
      errorSaving: false
    });
    this.sectionAnswers[id] = sectionAnswers;
    // console.log(this.sectionAnswers);
  }

  handleAnswerChanged(answer) {
    this.setState({
      errorSaving: false
    });
    this.freeQuestionAnswers[answer.question_id] = answer;
    // console.log(this.freeQuestionAnswers);
  }

  async getForm(id) {
    this.setState({ loading: true });
    const form = await this.props.getForm(id);

    if (!form || form === {}) this.setState({ notFound: true });

    this.setState({ form: form, loading: false });
    this.responseInfo.form_id = id;
  }

  render() {
    const { classes } = this.props;

    if (this.state.loading) {
      return (
        <div>
          <Typography variant="h3">Loading...</Typography>
        </div>
      );
    } else {
      return (
        <div className={classes.fillResponseVie}>
          {this.state.notFound ? <Redirect to="/404" /> : <></>}

          {/* form information */}
          <Typography variant="h4">
            {this.state.form.form.form_title}
          </Typography>

          {/* patient id */}
          <FillResponseQuestion
            style={{ margin: "10px" }}
            question_id="patient-id"
            question_type="ST"
            title="Patient ID"
            onChange={this.handlePatientIdChanged}
          />

          {/* sections */}
          {this.state.form.sections.map((section, id) => (
            <FillResponseSection
              section={section}
              key={section.section_id}
              onChange={answers => this.handleSectionChanged(id, answers)}
            />
          ))}

          {/* free questions */}
          <div className={classes.freeQuestions}>
            {this.state.form.free_questions.map(question => (
              <FillResponseQuestion
                {...question}
                key={question.question_id}
                isFillable={false}
                onChange={this.handleAnswerChanged}
              />
            ))}
          </div>

          {/* save button */}
          <div className={classes.saveButton}>
            <Button
              variant="contained"
              color="primary"
              fullWidth
              onClick={this.onSaveButtonClicked}
              disabled={this.state.saving}
            >
              {this.state.saving ? "Saving..." : "Save"}
            </Button>
          </div>

          {/* error */}
          {this.state.errorSaving ? (
            <ErrorBar message="There was an error saving your response, please check your response and try again. " />
          ) : (
            <></>
          )}

          {/* footer */}
          <Typography variant="subtitle1">
            {this.state.form.form.form_footer}
          </Typography>

          {/* saved, redirect to view all responses */}
          {this.state.saved ? (
            <Redirect to="/responses/browse/success" />
          ) : (
            <></>
          )}
        </div>
      );
    }
  }
}

export default withStyles(styles)(FillResponseView);
