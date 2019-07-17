import React from "react";

import { withStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableRow from "@material-ui/core/TableRow";

import Emoji from "../Emoji";

const styles = {
  cell: {
    fontSize: 20
  }
};

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
  render() {
    const { classes } = this.props;

    let players = [];
    if (this.props.data) {
      let data = this.props.data.data;
      if (data && data.length > 0) {
        for (let i = 0; i < 5; i++) {
          let fullname = data[i].first_name + " " + data[i].last_name;
          players.push(
            <TableRow key={data[i].player_id}>
              <TableCell className={classes.cell}>{fullname}</TableCell>
              <TableCell align="right" className={classes.cell}>
                {formatScore(data[i].ttfl_score, this.props.average)}
              </TableCell>
            </TableRow>
          );
        }
      }
      return (
        <Table>
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
