import { combineReducers } from 'redux';
import story from './story';
import user from './user';
import question from './question';

export default combineReducers({
    story,
    user,
    question
});