import React, { Component } from "react";
import PropTypes from "prop-types";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import withStyles from "@material-ui/core/styles/withStyles";
import "./ResponseQuestion.css";

const ResponseQuestion = props => {
  console.log(props);

  const hasDependent =
    props.dependents &&
    props.dependents !== {} &&
    props.answer in props.dependents;

  if (props.question_type === "MC") {
    const options = props.options.split("|");
    return (
      <Card className="responseQuestion">
        <CardContent>
          <Typography variant="h6" className="questionTitle">
            <strong>{props.title}</strong>
          </Typography>
          <ul>
            {options.map((option, i) => {
              return option.toString().toLowerCase() ===
                props.answer.toString().toLowerCase() ? (
                <li key={i}>
                  <Typography className="options">
                    <u>{option}</u>
                  </Typography>
                </li>
              ) : (
                <li key={i}>
                  <Typography className="options">{option}</Typography>
                </li>
              );
            })}
          </ul>

          {hasDependent ? (
            // render dependent
            <ResponseQuestion
              {...props.dependents[props.answer]}
              answer={
                props.sectionAnswers[props.dependents[props.answer].question_id]
                  .answer_content
              }
            />
          ) : (
            <></>
          )}
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="responseQuestion">
      <CardContent>
        <Typography variant="h6" gutterBottom className="questionTitle">
          <strong>{props.title}</strong>
        </Typography>
        <Typography variant="body1">{props.answer}</Typography>
      </CardContent>
    </Card>
  );
};

ResponseQuestion.propTypes = {
  question_type: PropTypes.oneOf(["MC", "ST"]), // Type of question
  question_id: PropTypes.string.isRequired, // ID of question
  title: PropTypes.string.isRequired, // Title of question
  answer: PropTypes.string.isRequired, // Response
  options: PropTypes.string, // Options delimited by comma (,) if type is MC
  sectionAnswers: PropTypes.object, // Answers for the whole section, for use of dependent questions
  dependents: PropTypes.object // Dependent questions on this question
};

export default ResponseQuestion;
