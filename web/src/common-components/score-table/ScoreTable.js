import React from "react";
import { withStyles } from "@material-ui/core/styles";
import Emoji from "../Emoji";
import grey from "@material-ui/core/colors/grey";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";

const styles = {
  cell: {
    fontSize: 20
  }
};

// alternate rows background color to improve table readability
const StyledTableRow = withStyles(theme => ({
  root: {
    "&:nth-of-type(odd)": {
      backgroundColor: grey[100]
    }
  }
}))(TableRow);

// will format raw ttfl score to make it 2 decimal long if score is a calculated average
// and add "pts" label
const formatScore = function(score, average) {
  if (average) {
    let formattedScore = parseFloat(score).toFixed(2);
    return formattedScore + " pts";
  } else {
    return score + " pts";
  }
};

class ScoreTable extends React.Component {
  buildTableHead(headers) {
    let heads = [];
    for (let i in headers) {
      heads.push(
        <TableCell align={headers[i].align}>{headers[i].label}</TableCell>
      );
    }
    return heads;
  }

  render() {
    const { classes } = this.props;

    let players = [];
    if (this.props.data) {
      let data = this.props.data.data;
      let i = 0;
      if (data && data.length > 0) {
        while (i < data.length) {
          let fullname = data[i].first_name + " " + data[i].last_name;
          players.push(
            <StyledTableRow key={data[i].player_id}>
              <TableCell className={classes.cell}>{fullname}</TableCell>
              <TableCell align="right" className={classes.cell}>
                {formatScore(data[i].ttfl_score, this.props.average)}
              </TableCell>
            </StyledTableRow>
          );
          if (this.props.short && i == 10) {
            break;
          } else {
            i++;
          }
        }
      }

      let head;
      if (this.props.headers && this.props.headers.length > 0) {
        head = (
          <TableHead>
            <TableRow>{this.buildTableHead(this.props.headers)}</TableRow>
          </TableHead>
        );
      }

      return (
        <Table>
          {head}
          <TableBody>{players}</TableBody>
        </Table>
      );
    } else {
      return (
        <p className="error-message">
          Nous n'avons pas pu récupérer les données correspondantes &nbsp;
          <Emoji emoji="😔" label="sadface" />
        </p>
      );
    }
  }
}

export default withStyles(styles)(ScoreTable);
