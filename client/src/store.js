import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './reducer';

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;


const middlewares = [
    thunk
  ]
  
  if (process.env.NODE_ENV === 'development' && process.env.TARO_ENV !== 'quickapp') {
    middlewares.push(require('redux-logger').createLogger())
  }

function configureStore(initialState = {}) {
    return createStore(
        rootReducer,
        initialState,
        composeEnhancers(
            applyMiddleware(...middlewares)
        )
    );
}

const store = configureStore();

export default store;