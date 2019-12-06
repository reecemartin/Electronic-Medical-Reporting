import React, { Component } from "react";
import clsx from "clsx";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Link from "@material-ui/core/Link";
import Paper from "@material-ui/core/Paper";
import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import Typography from "@material-ui/core/Typography";
import withStyles from "@material-ui/core/styles/withStyles";

import ErrorBarContentWrapper from "../StatusBar/ErrorBar";

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {"Copyright © "}
      <Link color="inherit" href="https://material-ui.com/">
        LabCats
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}

const useStyles = theme => ({
  root: {
    height: "100vh",
    overflowY: "hidden"
  },
  image: {
    backgroundImage: "url(https://source.unsplash.com/random)",
    backgroundRepeat: "no-repeat",
    backgroundSize: "cover",
    backgroundPosition: "center"
  },
  paper: {
    margin: theme.spacing(8, 4),
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1)
  },
  submit: {
    margin: theme.spacing(3, 0, 2)
  }
});

class Login extends Component {
  constructor(props) {
    super();
    this.props = props;
    this.signIn = this.signIn.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.state = {
      email: "",
      password: "",
      remember: false,
      loggedIn: false,
      validated: true,
      errorFormatOpen: false,
      errorLoginOpen: false
    };
  }

  closeErrorMessages() {
    this.setState({
      errorFormatOpen: false,
      errorLoginOpen: false
    });
  }

  handleChange(key_, value) {
    // console.log("[Login] handleChange");
    this.closeErrorMessages();
    this.setState({ [key_]: value });
    if (key_ === "email") {
      // check if the email contains an '@' symbol
      const atLoc = value.indexOf("@");
      if (value && value.indexOf("@") === -1) {
        // console.log("no @ symbol")
        this.setState({ validated: false });
      } else if (
        value &&
        (value.indexOf(".", atLoc) === -1 ||
          value.indexOf(".", atLoc) >= value.length - 2)
      ) {
        // console.log("domain name incorrect")
        this.setState({ validated: false });
      } else {
        this.setState({ validated: true });
      }
    }
  }

  render() {
    const { classes } = this.props;
    return (
      <Grid container component="main" className={classes.root}>
        <CssBaseline />
        <Grid item xs={false} sm={4} md={7} className={classes.image} />
        <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
          <div className={classes.paper}>
            <Avatar className={classes.avatar}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign in to LabCats
            </Typography>
            <form className={classes.form} noValidate>
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                // autoComplete="email"
                error={!this.state.validated}
                autoFocus
                onChange={e => this.handleChange("email", e.target.value)}
              />
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                // autoComplete="current-password"
                onChange={e => this.handleChange("password", e.target.value)}
              />
              <FormControlLabel
                control={<Checkbox value="remember" color="primary" />}
                label="Remember me"
                onChange={e => this.handleChange("remember", e.target.value)}
              />

              <Button
                // type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className={classes.submit}
                onClick={this.signIn}
                id="signIn"
              >
                Sign In
              </Button>

              {/* Error messages */}
              {this.state.errorFormatOpen ? (
                <ErrorBarContentWrapper
                  variant="error"
                  className={classes.margin}
                  id="#errorFormat"
                  message="Please enter your email address correctly!"
                />
              ) : (
                <></>
              )}
              {this.state.errorLoginOpen ? (
                <ErrorBarContentWrapper
                  variant="error"
                  className={classes.margin}
                  id="#errorFormat"
                  message="Incorrect email address or password!"
                />
              ) : (
                <></>
              )}

              <Box mt={5}>
                <Copyright />
              </Box>
            </form>
          </div>
        </Grid>
      </Grid>
    );
  }

  async signIn(e) {
    e.preventDefault();
    if (this.state.validated && this.state.email !== "") {
      const signInResult = await this.props.signIn(
        this.state.email,
        this.state.password,
        this.state.remember
      );
      if (!signInResult) {
        console.log("[Login] login unsuccessful");
        this.setState({ errorLoginOpen: true });
      }
    } else {
      this.setState({ errorFormatOpen: true });
    }
  }
}

export default withStyles(useStyles)(Login);
