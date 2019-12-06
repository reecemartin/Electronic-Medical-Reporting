import React from "react";
import ResponseQuestion from "./ResponseQuestion";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import "./ResponseSection.css";

const ResponseSection = props => {
  const questions = props.formSection.questions;
  console.log(questions);
  console.log(props.responseSection.questions);

  return (
    <Paper className="response-section">
      <div className="section-header">
        <Typography className="section-title" variant="h5" gutterBottom>
          {props.formSection.title}
        </Typography>

        {/* Subsections */}
        {props.formSection.subsections.map((subsection, i) => (
          <ResponseSection
            formSection={subsection}
            responseSection={props.responseSection.subsections[i]}
            key={subsection.section_id}
          />
        ))}

        {/* Questions */}
        {questions.map((question, i) => (
          <ResponseQuestion
            {...question}
            answer={
              props.responseSection.questions[question.question_id]
                .answer_content
            }
            key={question.question_id}
            sectionAnswers={props.responseSection.questions}
          />
        ))}
      </div>
    </Paper>
  );
};

export default ResponseSection;
