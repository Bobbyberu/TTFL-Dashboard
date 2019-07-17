import React, { Component } from "react";
import BoxscoreService from "../../services/BoxscoreService";

import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import { withStyles } from "@material-ui/core/styles";

import Emoji from "../../common-components/Emoji";
import Navbar from "../../common-components/Navbar";
import ScoreTable from "../../common-components/score-table/ScoreTable";

const styles = {
  title: {
    color: "#BC0001"
  },
  table: {
    margin: 10,
    paddingLeft: 20,
    paddingRight: 20
  },
  tableTitle: {
    paddingTop: 10,
    paddingBottom: 20
  },
  extraLink: {
    padding: 15,
    textAlign: "right"
  }
};

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      top_players_season: [],
      top_players_night: []
    };
  }

  componentDidMount() {
    this.getTopTTFL();
    this.getNightTopTTFL();
  }

  async getTopTTFL() {
    try {
      let response = await BoxscoreService.getTopTTFL();
      if (response.status === 200) {
        this.setState({
          top_players_season: response.data
        });
      }
    } catch (error) {
      this.setState({
        top_players_season: null
      });
    }
  }

  async getNightTopTTFL() {
    try {
      let response = await BoxscoreService.getNightTopTTFL(2019, 2, 3);
      if (response.status === 200) {
        this.setState({
          top_players_night: response.data
        });
      }
    } catch (error) {
      this.setState({
        top_players_night: null
      });
    }
  }

  render() {
    const { classes } = this.props;
    return (
      <div>
        <Navbar />
        <h1 className={classes.title}>#TTFL Dashboard</h1>
        <Grid container>
          <Grid item xs={6}>
            <Paper className={classes.table}>
              <Typography
                variant="h4"
                id="tableTitle"
                className={classes.tableTitle}
              >
                <Emoji emoji="🔥" label="fire" /> Scores de la nuit
              </Typography>
              <ScoreTable data={this.state.top_players_night} average={false} />
              <p className={classes.extraLink}>
                <a href="/nightscores">>> Tous les scores de la nuit</a>
              </p>
            </Paper>
          </Grid>
          <Grid item xs={6}>
            <Paper className={classes.table}>
              <Typography
                variant="h4"
                id="tableTitle"
                className={classes.tableTitle}
              >
                <Emoji emoji="⭐" label="star" /> Meilleurs joueurs de la saison
              </Typography>
              <ScoreTable data={this.state.top_players_season} average={true} />
              <p className={classes.extraLink}>
                <a href="/averages">>> Toutes les moyennes des joueurs</a>
              </p>
            </Paper>
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default withStyles(styles)(Home);
