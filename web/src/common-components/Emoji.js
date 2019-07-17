import React from "react";

export default class Emoji extends React.Component {
  render() {
    return (
      <span role="img" aria-label={this.props.label}>
        {this.props.emoji}
      </span>
    );
  }
}
