import ActionType from '../action/type';
import Cookies from 'js-cookie';

let question = Cookies.get("question") ? Cookies.get("question") : "show me the distribution"

const initialState = {
    question,
    cachedQA: null,
    isUpdateLayout: false,
    editedTitle: ''
}

export default (state = initialState, action) => {
    const newState = Object.assign({}, state);
    switch (action.type) {
        case ActionType.UPDATE_QUESTION:
            newState.question = action.question
            newState.cachedQA = null //reset cachedQA 
            newState.editedTitle = null //reset user edit title 
            Cookies.set("question", action.question)
            return newState;
        case ActionType.SAVE_CACHED_QA:
            newState.cachedQA = action.cachedQA
            newState.cachedQA = newState.cachedQA.map((QA, id) => {
                return {
                    ...QA,
                    id //update id
                }
            })
            newState.isUpdateLayout = true
            return newState;
        case ActionType.EDIT_TITLE:
            newState.editedTitle = action.title
            return newState;
        default:
            break;
    }
    return newState;
}