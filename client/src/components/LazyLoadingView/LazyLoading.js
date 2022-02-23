import React, { Component } from "react";


export default class LazyLoading extends Component {
    render() {
        const { isLoading, error } = this.props
        // Handle the loading state
        if (isLoading) {
            return <div style={{ backgroundColor: "#f0f2f5" }}></div>;
        }
        // Handle the error state
        else if (error) {
            return <div>Sorry, there was a problem loading the page.</div>;
        }
        else {
            return null;
        }
    }
};

