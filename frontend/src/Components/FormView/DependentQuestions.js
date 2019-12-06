import React, { Component } from "react";
import PropTypes from "prop-types";
import withStyles from "@material-ui/core/styles/withStyles";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import FormQuestion from "./FormQuestion";

const styles = {};

class DependentQuestions extends Component {
  render() {
      console.log(this.props.questions);
    return (
      <Paper style={{ backgroundColor: "#cccccc", padding:"10px", marginBottom:"10px" }}>
        <Typography variant="h6" gutterBottom>
          {'If "' + this.props.relatedOption + '":'}
        </Typography>

        <FormQuestion {...this.props.question}/>
      </Paper>
    );
  }
}

DependentQuestions.propTypes = {
  question: PropTypes.object,
  relatedOption: PropTypes.string
};

export default withStyles(styles)(DependentQuestions);
