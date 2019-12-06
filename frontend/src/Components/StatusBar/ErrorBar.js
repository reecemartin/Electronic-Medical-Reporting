import React from "react";
import ErrorIcon from "@material-ui/icons/Error";
import SnackbarContent from "@material-ui/core/SnackbarContent";

function ErrorBarContentWrapper(props) {
  const { className, message, onClose, variant, ...other } = props;
  const Icon = ErrorIcon;

  return (
    <SnackbarContent
      style={{ backgroundColor: "#d32f2f" }}
      aria-describedby="error-message"
      message={
        <span
          id="error-bar"
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

export default ErrorBarContentWrapper;
