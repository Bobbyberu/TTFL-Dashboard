import React from "react";

export default class NotFound extends React.Component {
  render() {
    return this.props.message ? (
      <div className="not-found">{this.props.message}</div>
    ) : (
      <div className="not-found">Could not find {this.props.path}!</div>
    );
  }
}
