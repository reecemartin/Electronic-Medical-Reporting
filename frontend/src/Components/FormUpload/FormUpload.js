import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";

class FormUpload extends Component {
  constructor(props) {
    super(props);
    this.state = {
      fileForUpload: null,
      test: 1
    };
    this.onUploadHandler = this.onUploadHandler.bind(this);
    this.onUploadButtonClicked = this.onUploadButtonClicked.bind(this);
  }

  onUploadHandler(event) {
    console.log(event.target.files[0]);
    this.setState({
      fileForUpload: event.target.files[0]
    });
  }
  onUploadButtonClicked(event) {
    event.preventDefault();
    console.log("[FormUpload] onUploadButtonClicked");
    if (this.state.fileForUpload == null) return;
    this.props.uploadForm(this.state.fileForUpload);
  }

  render() {
    return (
      <div style={{ margin: "10px" }}>
        <Button variant="outlined" component="label">
          Upload File
          <input
            type="file"
            accept=".xml"
            name="file"
            style={{ display: "none" }}
            onChange={this.onUploadHandler}
          />
        </Button>
        <Typography style={{ display: "inline-block", margin: "0 10px" }}>
          {this.state.fileForUpload == null
            ? "No File Chosen"
            : this.state.fileForUpload.name}
        </Typography>
        <Button variant="contained" onClick={this.onUploadButtonClicked}>
          Upload
        </Button>
      </div>
    );
  }
}

export default FormUpload;
