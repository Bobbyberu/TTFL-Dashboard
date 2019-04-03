import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import Averages from "./pages/averages/Averages";
import Games from "./pages/games/Games";
import Home from "./pages/home/Home";
import NightScores from "./pages/night-scores/NightScores";
import NotFound from "./pages/404/NotFound";
import Players from "./pages/players/Players";
import Teams from "./pages/teams/Teams";

function AppRouter() {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={() => <Home />} />
        <Route path="/averages" exact component={() => <Averages />} />
        <Route path="/games" exact component={() => <Games />} />
        <Route path="/nightscores" exact component={() => <NightScores />} />
        <Route path="/players" exact component={() => <Players />} />
        <Route path="/teams" exact component={() => <Teams />} />
        <Route component={NoMatch} />
      </Switch>
    </Router>
  );
}

function NoMatch({ location }) {
  return <NotFound path={location.pathname} />;
}

export default AppRouter;
