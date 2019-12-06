import React, { Component } from "react";
import PropTypes from "prop-types";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import TextField from "@material-ui/core/TextField";
import "./FillResponseQuestion.css";

class FillResponseQuestion extends Component {
  constructor(props) {
    super(props);
    if (this.props.question_type === "MC") {
      const options = this.props.options.split("|");
      if (options.length === 1) {
        // if checkbox question, current answer should be empty (nothing selected)
        this.state = {
          answer: ""
        };
      } else {
        // if MC question, current answer should be first option
        this.state = {
          answer: options[0]
        };
      }
    } else {
      this.state = {
        answer: ""
      };
    }

    // Update parent with current answer
    const newResponse = {
      answer_content: this.state.answer,
      state: true,
      question_id: this.props.question_id
    };
    this.props.onChange(newResponse);

    // bind class functions
    this.handleChange = this.handleChange.bind(this);
    this.handleChangeCheckbox = this.handleChangeCheckbox.bind(this);
  }

  // handle input events from radio buttons and text boxes
  handleChange(event) {
    this.setState({ answer: event.target.value }, () => {
      console.log(this.state.answer);
    });
    const newResponse = {
      answer_content: event.target.value,
      state: true,
      question_id: this.props.question_id
    };
    this.props.onChange(newResponse);
  }

  // handle input events from checkbox
  // if checked, then answer is option value
  // otherwise, answer is empty string
  handleChangeCheckbox(event) {
    const answer = event.target.checked ? event.target.value : "";

    this.setState({ answer: answer }, () => {
      // console.log(this.state.answer);
    });

    const newResponse = {
      answer_content: answer,
      state: true,
      question_id: this.props.question_id
    };
    this.props.onChange(newResponse);
  }

  render() {
    if (this.props.question_type === "MC") {
      const options = this.props.options.split("|");
      return (
        <Card className="fillResponseQuestion">
          <CardContent>
            <Typography variant="h6" className="questionTitle">
              <strong>{this.props.title}</strong>
            </Typography>
            {options.length === 1 ? (
              <FormControlLabel
                value={options[0]}
                control={<Checkbox />}
                label={options[0]}
                onChange={this.handleChangeCheckbox}
              />
            ) : (
              <RadioGroup
                aria-label="MCoptions"
                name="MCoptions"
                value={this.state.answer}
                onChange={this.handleChange}
              >
                {options.map((option, i) => (
                  <FormControlLabel
                    value={option}
                    control={<Radio />}
                    label={option}
                    key={i}
                  />
                ))}
              </RadioGroup>
            )}

            {// dependent question, can use the same onChange function from this question's parent
            this.state.answer in this.props.dependents ? (
              <FillResponseQuestion
                {...this.props.dependents[this.state.answer]}
                onChange={this.props.onChange}
              />
            ) : (
              <></>
            )}
          </CardContent>
        </Card>
      );
    }
    return (
      <Card className="formQuestion">
        <CardContent>
          <Typography variant="h6" className="questionTitle">
            <strong>{this.props.title}</strong>
          </Typography>
          <TextField
            id="outlined-textarea"
            label={this.props.title}
            placeholder="Enter Answer Here"
            multiline
            className="textField"
            margin="normal"
            variant="outlined"
            onChange={this.handleChange}
          />
        </CardContent>
      </Card>
    );
  }
}

FillResponseQuestion.propTypes = {
  question_type: PropTypes.oneOf(["MC", "ST"]), // Type of question
  question_id: PropTypes.string.isRequired, // ID of question
  title: PropTypes.string.isRequired, // Title of question
  options: PropTypes.string, // Options delimited by comma (,) if type is MC
  onChange: PropTypes.func, // A function to respond to change, if question is fillable
  dependents: PropTypes.object // Dependent questions on this question
};

export default FillResponseQuestion;
