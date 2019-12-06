import React from "react";
import PropTypes from "prop-types";
import CheckCircleIcon from "@material-ui/icons/CheckCircle";
import SnackbarContent from "@material-ui/core/SnackbarContent";

function SuccessBarContentWrapper(props) {
  const { className, message, onClose, variant, ...other } = props;
  const Icon = CheckCircleIcon;

  return (
    <SnackbarContent
      style={{ backgroundColor: "#3F51B5", marginBottom: "10px" }}
      aria-describedby="success-message"
      message={
        <span
          id="success-bar"
          style={{ display: "flex", alignItems: "center", margin: "5px" }}
        >
          <Icon style={{ fontSize: 20, opacity: 0.9, marginRight: "10px" }} />
          {message}
        </span>
      }
      {...other}
    />
  );
}

SuccessBarContentWrapper.propTypes = {
  message: PropTypes.string.isRequired
};

export default SuccessBarContentWrapper;
