import React from 'react';
import { connect } from 'react-redux'
import * as userAction from './action/userAction'
import LazyLoading from '@/components/LazyLoadingView/index'
import intl from 'react-intl-universal'
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import './App.less'
import './common.less'

import {
  HashRouter as Router,
  Switch,
  Route,
  //useParams
} from "react-router-dom";
// common locale data
require('intl/locale-data/jsonp/en.js');
require('intl/locale-data/jsonp/zh.js');

// app locale data
const locales = {
  "en-US": require('./locales/en-US.json'),
  "zh-CN": require('./locales/zh-CN.json'),
};

const mapDispatchToProps = dispatch => {
  return {
    updateLocale: (currentLocale) => dispatch(userAction.updateLocale(currentLocale)),
  }
}
const mapStateToProps = (state) => ({
})

const ANIMATION_MAP = {
  PUSH: "fade",
  POP: "refade",
};
class App extends React.Component {

  state = {
    initDone: false,
    currentLocale: '',
    isShow: true
  }

  loadLocales(lang) {
    // init method will load CLDR locale data according to currentLocale
    // react-intl-universal is singleton, so you should init it only once in your app
    intl.init({
      currentLocale: lang,
      locales,
    })
      .then(() => {
        this.props.updateLocale(lang)
        // After loading CLDR locale data, start to render
        this.setState(
          { initDone: true, currentLocale: lang });
      });
  }

  initDefaultLang = () => {
    let userDefaultLang = navigator.language || navigator.userLanguage;//常规浏览器语言和IE浏览器
    let lang = userDefaultLang.substr(0, 2);//截取lang前2位字符
    if (lang === 'zh') {
      lang = "zh-CN"
    } else {
      lang = "en-US"
    }
    if (this.state.currentLocale !== lang) {
      this.loadLocales(lang)
    }
  }

  componentDidMount() {
    this.initDefaultLang()
  }



  render() {
    const { initDone, currentLocale } = this.state;

    const MyRoute = ({ MyComponent, ...rest }) => {
      return (
        <Route
          {...rest}
          render={routerProps => (
            <MyComponent
              intl={intl}
              initDone={initDone}
              currentLocale={currentLocale}
              onChangeLocaleListener={lang => this.loadLocales(lang)}
              {...routerProps} ></MyComponent>)
          } />
      )
    }
    const AnimationGo = (props) => {
      const { children } = props;
      return (
        <Route
          render={({ location, history }) => {
            return <TransitionGroup
              className="animation-page"
              childFactory={(child) =>
                React.cloneElement(child, {
                  classNames: "fade",
                })
              }
            >
              <CSSTransition timeout={500} key={location.pathname}>
                <Switch location={location}>{children}</Switch>
              </CSSTransition>
            </TransitionGroup>
          }}
        ></Route>
      );
    }

    return (
      <Router>
        <AnimationGo>
          <MyRoute exact path='/edit' MyComponent={LazyLoading('EditPage/index')} />
          <MyRoute path='/data' MyComponent={LazyLoading('DataPage/index')} />
          {/* <MyRoute exact path='/publish' MyComponent={LazyLoading('PublishPage/PublishPage')} /> */}
          <MyRoute exact path='/' MyComponent={LazyLoading('Homepage/index')} />
        </AnimationGo>
      </Router>
    )
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App)