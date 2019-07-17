import React, { Component } from "react";
import { Link } from "react-router-dom";

import { withStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Divider from "@material-ui/core/Divider";
import Drawer from "@material-ui/core/Drawer";
import IconButton from "@material-ui/core/IconButton";
import List from "@material-ui/core/List/List";
import ListItem from "@material-ui/core/ListItem/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import Menu from "@material-ui/icons/Menu";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";

import Emoji from "./Emoji";

const styles = theme => ({
  navbar: {
    position: "inherit"
  },
  navbarTitle: {
    "&:hover": {
      color: "#d3d5d6",
      transition: ".5s"
    }
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20
  },
  list: {
    width: 300
  },
  link: {
    textDecoration: "none",
    "&:hover": {
      textDecoration: "none"
    }
  },
  drawerTitle: {
    marginLeft: 8,
    fontWeight: "bold"
  },
  sectionIcon: {
    color: "rgba(0,0,0,0.8)"
  }
});

class Navbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      drawerOpen: false
    };
  }

  toggleDrawer = () => {
    this.setState({
      drawerOpen: !this.state.drawerOpen
    });
  };

  getDrawerContent() {
    const { classes } = this.props;
    return (
      <div className={classes.list}>
        <h4 className={classes.drawerTitle}>Sections</h4>
        <List>
          <Link to="/nightscores" className={classes.link}>
            <ListItem button>
              <ListItemIcon className={classes.sectionIcon}>
                <Emoji emoji="🔥" label="fire" />
              </ListItemIcon>
              <ListItemText>Scores de la nuit</ListItemText>
            </ListItem>
          </Link>
          <Divider variant="middle" />
          <Link to="/games" className={classes.link}>
            <ListItem button>
              <ListItemIcon className={classes.sectionIcon}>
                <Emoji emoji="🏀" label="basketball" />
              </ListItemIcon>
              <ListItemText>Matchs</ListItemText>
            </ListItem>
          </Link>
          <Divider variant="middle" />
          <Link to="/players" className={classes.link}>
            <ListItem button>
              <ListItemIcon className={classes.sectionIcon}>
                <Emoji emoji="🧔" label="bearded man" />
              </ListItemIcon>
              <ListItemText>Joueurs</ListItemText>
            </ListItem>
          </Link>
          <Divider variant="middle" />
          <Link to="/teams" className={classes.link}>
            <ListItem button>
              <ListItemIcon className={classes.sectionIcon}>
                <Emoji emoji="🏠" label="house" />
              </ListItemIcon>
              <ListItemText>Équipes</ListItemText>
            </ListItem>
          </Link>
          <Divider variant="middle" />
          <Link to="/averages" className={classes.link}>
            <ListItem button>
              <ListItemIcon className={classes.sectionIcon}>
                <Emoji emoji="📊" label="bar chart" />
              </ListItemIcon>
              <ListItemText>Stats</ListItemText>
            </ListItem>
          </Link>
          <Divider variant="middle" />
        </List>
      </div>
    );
  }

  render() {
    const { classes } = this.props;

    return (
      <AppBar position="fixed" className={classes.navbar}>
        <Toolbar className={classes.toolbar}>
          <IconButton
            color="inherit"
            aria-label="Menu"
            onClick={this.toggleDrawer}
            className={classes.menuButton}
          >
            <Menu />
          </IconButton>
          <Link to="/" className={classes.link}>
            <Typography
              variant="h5"
              color="secondary"
              className={classes.navbarTitle}
            >
              TTFL Dashboard
            </Typography>
          </Link>
          <Drawer
            open={this.state.drawerOpen}
            onClose={this.toggleDrawer}
            anchor="left"
          >
            {this.getDrawerContent()}
          </Drawer>
        </Toolbar>
      </AppBar>
    );
  }
}

export default withStyles(styles)(Navbar);
