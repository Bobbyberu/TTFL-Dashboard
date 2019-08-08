import React, { Component } from "react";
import { withStyles } from "@material-ui/core/styles";
import BoxscoreService from "../../services/BoxscoreService";

import MaterialTable from "material-table";
import Paper from "@material-ui/core/Paper";

import Navbar from "../../common-components/Navbar";
import ScoreTable from "../../common-components/score-table/ScoreTable";

const styles = {
  table: {
    margin: 10,
    marginLeft: 60,
    marginRight: 60,
    marginTop: 30
  },
  MuiTableCellBody: {
    fontSize: 50
  }
};

class NightScores extends Component {
  constructor(props) {
    super(props);

    this.state = {
      players_score: []
    };
  }

  componentDidMount() {
    this.getAllTTFLScores();
  }

  async getAllTTFLScores() {
    let players_score = [];
    try {
      let response = await BoxscoreService.getNightAllTTFL(2019, 2, 3);

      if (response.status === 200) {
        let perfs = response.data.data;
        for (let player in perfs) {
          players_score.push({
            player: perfs[player].first_name + " " + perfs[player].last_name,
            score: perfs[player].ttfl_score
          });
        }
        this.setState({
          players_score: players_score
        });
      }
    } catch (error) {
      console.error(error);
    }
  }

  render() {
    const { classes } = this.props;
    let headers = [
      { title: "Joueur", field: "player", cellStyle: { fontSize: "20px" } },
      { title: "Score", field: "score", cellStyle: { fontSize: "20px" } }
    ];
    return (
      <div>
        <Navbar />
        <h1>Scores de la nuit</h1>
        <Paper className={classes.table}>
          <MaterialTable
            title="Scores de la nuit"
            columns={headers}
            data={this.state.players_score}
            options={{ pageSize: 10 }}
            style={{ fontSize: 50 }}
            localization={{
              toolbar: {
                searchPlaceholder: "Rechercher"
              },
              pagination: {
                labelRowsSelect: "Joueurs",
                labelDisplayedRows: " {from}-{to} sur {count}"
              }
            }}
          />
        </Paper>
      </div>
    );
  }
}

export default withStyles(styles)(NightScores);
