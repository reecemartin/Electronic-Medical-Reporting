import React, { Component } from "react";
import FormQuestion from "./FormQuestion";
import FormSection from "./FormSection";
import Typography from "@material-ui/core/Typography";
import withStyles from "@material-ui/core/styles/withStyles";
import { Redirect, Link } from "react-router-dom";
import Button from "@material-ui/core/Button";

const styles = () => {
  return {
    form: {
      padding: "10px"
    },
    freeQuestions: {
      padding: "10px"
    }
  };
};

class FormView extends Component {
  constructor(props) {
    super(props);
    console.log(props.match.params.id);
    this.state = { form: null, loading: true, notFound: false };
    if (props.match.params.id != null) this.getForm(props.match.params.id);
  }

  async getForm(id) {
    if (this.state) this.setState({ loading: true });
    const form = await this.props.getForm(id);
    console.log(form);
    if (!form || form === {}) this.setState({ notFound: true });
    if (this.state) this.setState({ form: form });
    if (this.state) this.setState({ loading: false });
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
        <div className={classes.form}>
          {this.state.notFound ? <Redirect to="/404" /> : <></>}

          {/* form information */}
          <Typography variant="h4">
            {this.state.form.form.form_title}
          </Typography>

          <Link
            to={"/form/" + this.state.form.form.form_id + "/fill"}
            style={{ textDecoration: "none" }}
          >
            <Button variant="contained">Fill</Button>
          </Link>

          {/* <Typography variant="subtitle1">{props.form.form.package_id}</Typography> */}

          {/* sections */}
          {this.state.form.sections.map(section => (
            <FormSection section={section} key={section.section_id} />
          ))}

          {/* free questions */}
          <div className={classes.freeQuestions}>
            {this.state.form.free_questions.map(question => (
              <FormQuestion
                {...question}
                key={question.question_id}
                isFillable={false}
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
}

export default withStyles(styles)(FormView);
