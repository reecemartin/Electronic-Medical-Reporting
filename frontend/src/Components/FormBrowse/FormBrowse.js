import React, { Component } from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import { Link } from "react-router-dom";
import FormUpload from "../FormUpload/FormUpload";
import Button from "@material-ui/core/Button";

const StyledTableCell = withStyles(theme => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white
  },
  body: {
    fontSize: 14
  }
}))(TableCell);

const StyledTableRow = withStyles(theme => ({
  root: {
    "&:nth-of-type(odd)": {
      backgroundColor: theme.palette.background.default
    }
  }
}))(TableRow);

const styles = theme => ({
  root: {
    marginTop: theme.spacing(3),
    padding: "10px"
  },
  table: {},
  formUpload: {
    padding: "10px"
  }
});

class FormBrowse extends Component {
  render() {
    const { classes } = this.props;
    return (
      <div>
        <FormUpload
          className={classes.formUpload}
          uploadForm={this.props.uploadForm}
        />

        <Table
          className={classes.table}
          stickyHeader
          aria-label="customized table"
        >
          <TableHead>
            <TableRow>
              <StyledTableCell>Form ID</StyledTableCell>
              <StyledTableCell>Package ID</StyledTableCell>
              <StyledTableCell>Form Title</StyledTableCell>
              <StyledTableCell>Actions</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {this.props.forms.map(row => (
              <StyledTableRow key={row.form_id}>
                <StyledTableCell component="th" scope="row">
                  {row.form_id}
                </StyledTableCell>
                <StyledTableCell>{row.package_id}</StyledTableCell>
                <StyledTableCell>
                  <Link to={"/form/" + row.form_id}>{row.form_title}</Link>
                </StyledTableCell>
                <StyledTableCell>
                  <Link
                    to={"/form/" + row.form_id + "/fill"}
                    style={{ textDecoration: "none" }}
                  >
                    <Button variant="contained">Fill</Button>
                  </Link>
                </StyledTableCell>
              </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    );
  }
}

FormBrowse.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(FormBrowse);
