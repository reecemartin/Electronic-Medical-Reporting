import React from "react";
import FillResponseQuestion from "./FillResponseQuestion";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import "./FillResponseSection.css";

class FillResponseSection extends React.Component {
  constructor(props) {
    super(props);

    this.answers = {};
    // console.log(this.answers);
    this.handleAnswerChanged = this.handleAnswerChanged.bind(this);
    this.subsections = props.section.subsections.map(_ => ({}));
  }

  handleAnswerChanged(answer) {
    console.log(answer);
    this.answers[answer.question_id] = answer;
    // console.log(this.answers);
    const newAnswers = {
      section_id: this.props.section.section_id,
      subsections: this.subsections,
      questions: this.answers
    };
    this.props.onChange(newAnswers);
  }

  handleSubsectionChanged(id, answers) {
    this.subsections[id] = answers;
    // console.log(this.subsections);
    const newAnswers = {
      section_id: this.props.section.section_id,
      subsections: this.subsections,
      questions: this.answers
    };
    this.props.onChange(newAnswers);
  }

  render() {
    const props = this.props;

    // const { classes } = props;
    return (
      <Paper className="form-section" style={{ backgroundColor: "#f2f2f2" }}>
        <div className="section-header">
          <Typography className="section-title" variant="h5" gutterBottom>
            {props.section.title}
          </Typography>
          {/* <Typography variant="subtitle1">{props.section.section_id}</Typography> */}

          {/* subsections */}
          {props.section.subsections.map((subsection, id) => (
            <FillResponseSection
              section={subsection}
              key={subsection.section_id}
              onChange={answers => this.handleSubsectionChanged(id, answers)}
            />
          ))}

          {/* questions */}
          {props.section.questions.map(question => (
            <FillResponseQuestion
              {...question}
              key={question.question_id}
              onChange={this.handleAnswerChanged}
            />
          ))}
        </div>
      </Paper>
    );
  }
}

export default FillResponseSection;
