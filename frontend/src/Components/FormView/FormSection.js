import React from "react";
import FormQuestion from "./FormQuestion";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import "./FormSection.css";

const FormSection = props => {
  // const { classes } = props;
  return (
    <Paper className="form-section" style={{ backgroundColor: "#f2f2f2" }}>
      <div className="section-header">
        <Typography className="section-title" variant="h5" gutterBottom>
          {props.section.title}
        </Typography>
        {/* <Typography variant="subtitle1">{props.section.section_id}</Typography> */}

        {/* subsections */}
        {props.section.subsections.map(subsection => (
          <FormSection section={subsection} key={subsection.section_id} />
        ))}

        {/* questions */}
        {props.section.questions.map(question => (
          <FormQuestion
            {...question}
            key={question.question_id}
            isFillable={false}
          />
        ))}
      </div>
    </Paper>
  );
};

export default FormSection;
