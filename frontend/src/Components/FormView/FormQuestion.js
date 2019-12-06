import React, { Component } from "react";
import PropTypes from "prop-types";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import withStyles from "@material-ui/core/styles/withStyles";
import DependentQuestions from "./DependentQuestions";

const styles = {
  formQuestion: {
    padding: "10px",
    marginBottom: "10px"
  },
  questionTitle: {
    fontFamily: "Open Sans, sans-serif"
  },
  options: {
    fontFamily: "Open Sans, sans-serif"
  }
};

// A question in a form.
class FormQuestion extends Component {
  render() {
    const { classes } = this.props;

    if (this.props.question_type === "MC") {
      const options = this.props.options.split("|");
      return (
        <Card className={classes.formQuestion}>
          <CardContent>
            <Typography variant="h6" className={classes.questionTitle}>
              <strong>{this.props.title}</strong>
            </Typography>
            <ul>
              {options.map((option, i) => (
                <li key={i}>
                  <Typography className={classes.options}>{option}</Typography>
                </li>
              ))}
            </ul>

            {
              Object.keys(this.props.dependents).map(option => (
                <DependentQuestions relatedOption={option} question={this.props.dependents[option]} key={option}/>
              ))
            }
          </CardContent>
        </Card>
      );
    }
    return (
      <Card className={classes.formQuestion}>
        <CardContent>
          <Typography variant="h6" className={classes.questionTitle}><strong>{this.props.title}</strong></Typography>
        </CardContent>
      </Card>
    );
  }
}

FormQuestion.propTypes = {
  question_type: PropTypes.oneOf(["MC", "ST"]), // Type of question
  question_id: PropTypes.string.isRequired, // ID of question
  title: PropTypes.string.isRequired, // Title of question
  options: PropTypes.string, // Options delimited by comma (,) if type is MC
  onChange: PropTypes.func // A function to respond to change, if question is fillable
};

export default withStyles(styles)(FormQuestion);
