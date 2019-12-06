import React, { Component } from "react";
import Typography from "@material-ui/core/Typography";
import { Redirect } from "react-router-dom";
import withStyles from "@material-ui/core/styles/withStyles";

import ResponseSection from "./ResponseSection";
import ResponseQuestion from "./ResponseQuestion";

const styles = () => {
  return {
    response: {
      padding: "10px"
    },
    freeQuestions: {
      padding: "10px"
    }
  };
};

class ResponseView extends Component {
  constructor(props) {
    super(props);
    const formId = props.match.params.formId;
    const patientId = props.match.params.patientId;
    const fillerId = props.match.params.fillerId;

    console.log(
      "[ResponseView] constructor, formId=" +
        formId +
        ", patientId=" +
        patientId +
        ",fillerId=" +
        fillerId
    );

    this.state = { response: null, form: null, loading: true, notFound: false };

    if (formId != null && patientId != null && fillerId != null)
      this.getResponse(formId, patientId, fillerId);
  }

  async getResponse(formId, patientId, fillerId) {
    this.setState({ loading: true });
    const response = await this.props.getResponse(formId, patientId, fillerId);

    if (!response || response === {}) this.setState({ notFound: true });
    console.log(response);
    this.setState({ response: response });
    await this.getForm(formId);
    this.setState({ loading: false });
  }

  async getForm(id) {
    const form = await this.props.getForm(id);
    console.log(form);
    if (!form || form === {}) this.setState({ notFound: true });
    if (this.state) this.setState({ form: form });
  }

  render() {
    const { classes } = this.props;

    if (this.state.loading) {
      return (
        <div>
          <Typography variant="h3">Loading...</Typography>
        </div>
      );
    }

    return (
      <div className={classes.response}>
        {this.state.notFound ? <Redirect to="/404" /> : <></>}

        {/* form information */}
        <Typography variant="h4">{this.state.form.form.form_title}</Typography>
        <Typography variant="subtitle1">
          Patient ID: {this.state.response.response.patient_id}
        </Typography>
        <Typography variant="subtitle1">
          Filler ID: {this.state.response.response.filler_id}
        </Typography>

        {/* <Typography variant="subtitle1">{props.form.form.package_id}</Typography> */}

        {/* sections */}
        {this.state.form.sections.map((section, i) => (
          <ResponseSection
            formSection={section}
            responseSection={this.state.response.sections[i]}
            key={section.section_id}
          />
        ))}

        {/* free questions */}
        <div className={classes.freeQuestions}>
          {this.state.form.free_questions.map((question, i) => (
            <ResponseQuestion
              {...question}
              answer={
                this.state.response.free_questions[question.question_id]
                  .answer_content
              }
              key={question.question_id}
              sectionAnswers={this.state.response.free_questions}
            />
          ))}
        </div>

        {/* footer */}
        <Typography variant="subtitle1">
          {this.state.form.form.form_footer}
        </Typography>
      </div>
    );
  }
}

export default withStyles(styles)(ResponseView);
