import React from 'react';
import connect from 'react-redux/lib/components/connect';
import Link from '../../core/components/Link';

import * as accountActions from '../actions';


const propTypes = {
  user: React.PropTypes.object.isRequired,
  accountUpdateProfile: React.PropTypes.func.isRequired,
};

export class Profile extends React.Component {
  constructor(props) {
    super(props);

    this.state = this.getStateFromProps(props);

    this.componentWillReceiveProps = this.componentWillReceiveProps.bind(this);
    this.handleValueChange = this.handleValueChange.bind(this);
    this.handleFormSubmit = this.handleFormSubmit.bind(this);
    this.getStateFromProps = this.getStateFromProps.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    this.setState(this.getStateFromProps(nextProps));
  }

  getStateFromProps(props) {
    return {
      username: props.user.get('username'),
      email: props.user.get('email'),
      first_name: props.user.get('first_name'),
      last_name: props.user.get('last_name'),
    };
  }

  handleValueChange(e) {
    this.setState({ [e.target.name]: e.target.value });
  }

  handleFormSubmit(e) {
    e.preventDefault();
    this.props.accountUpdateProfile({
      username: this.refs.username.value,
      email: this.refs.email.value,
      first_name: this.refs.first_name.value,
      last_name: this.refs.last_name.value,
    });
  }

  render() {
    return (
      <div>
        <form className="profile-form" onSubmit={this.handleFormSubmit}>
          <label htmlFor="username">Username</label>
          <input
            name="username"
            ref="username"
            value={this.state.username}
            onChange={this.handleValueChange}
          />

          <label htmlFor="email">Email</label>
          <input
            name="email"
            ref="email"
            type="email"
            value={this.state.email}
            onChange={this.handleValueChange}
          />

          <label htmlFor="first_name">First name</label>
          <input
            name="first_name"
            ref="first_name"
            value={this.state.first_name}
            onChange={this.handleValueChange}
          />

          <label htmlFor="last_name">Last name</label>
          <input
            name="last_name"
            ref="last_name"
            value={this.state.last_name}
            onChange={this.handleValueChange}
          />

          <button type="submit">Update profile</button>
        </form>

        <div>
          <Link to={ "/account/password/" }>Change password</Link>
          <Link to={ "/account/password/reset/" }>Reset password</Link>
        </div>
      </div>
    );
  }
}

Profile.propTypes = propTypes;

function mapStateToProps(state) {
  return {
    user: state.user,
  };
}

export const ProfileContainer = connect(
  mapStateToProps,
  accountActions
)(Profile);