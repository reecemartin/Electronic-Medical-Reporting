import React, { Component } from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import { Link } from "react-router-dom";
import SuccessBar from "../StatusBar/SuccessBar";

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
    // width: '100%',
    marginTop: theme.spacing(3),
    overflowX: "auto",
    padding: "10px"
  },
  table: {
    minWidth: 700
  },
  successBar: {
    paddingBottom: "10px"
  }
});

class ResponseBrowse extends Component {
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        {this.props.showSuccess ? (
          <SuccessBar
            className={classes.successBar}
            message="Successfully submitted response!"
          />
        ) : (
          <></>
        )}

        <Table
          className={classes.table}
          stickyHeader
          aria-label="customized table"
        >
          <TableHead>
            <TableRow>
              <StyledTableCell>Form ID</StyledTableCell>
              <StyledTableCell>Patient ID</StyledTableCell>
              <StyledTableCell>Filler ID</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {this.props.responses.map(row => (
              <StyledTableRow key={row.patient_id + row.form_id}>
                <StyledTableCell component="th" scope="row">
                  <Link
                    to={
                      "/response/" +
                      row.form_id +
                      "/" +
                      row.patient_id +
                      "/" +
                      row.filler_id
                    }
                  >
                    {row.form_id}
                  </Link>
                </StyledTableCell>
                <StyledTableCell>{row.patient_id}</StyledTableCell>
                <StyledTableCell>{row.filler_id}</StyledTableCell>
              </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    );
  }
}

ResponseBrowse.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(ResponseBrowse);
