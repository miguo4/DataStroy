import ActionType from '../action/type';
import Cookies from 'js-cookie';
// import { genTitle } from "../sentencer/index";
//
let fileName = Cookies.get("fileName") ? Cookies.get("fileName") : 'CarSales.csv'
let schema = Cookies.get("schema") ? JSON.parse(Cookies.get("schema")) : []

const initialState = {
    fileName, //缓存
   // title: '',
    data: [],
    schema,
    method: 'sig',
    facts: [],
    relations: [],
    maxStoryLength: 6,
    timeLimit: 2000,// for each iteration
    information: 40, // default 50 bits for 6 facts
    resultCoverage: 1,
    chartDiversity: 0,
    aggregationLevel: 0,
    rewardWeight: {
        logicality: 0.33,
        diversity: 0.33,
        integrity: 0.33,
    },
    generateProgress: 0,
};

export default (state = initialState, action) => {
    const newState = Object.assign({}, state);
    switch (action.type) {
        case ActionType.GENERATE_STORY:
            newState.facts = action.facts;
            newState.relations = action.relations;
            newState.resultCoverage = action.coverage;
            return newState;
        case ActionType.UPDATE_PROGRESS:
            newState.generateProgress = Number(((action.totalLength - action.currentLength) / action.totalLength).toFixed(2) * 100);
            return newState;
        case ActionType.UPLOAD_DATA:
            newState.fileName = action.fileName;
            Cookies.set("fileName", action.fileName)
            newState.schema = action.schema;
            newState.data = action.data;
            Cookies.set("schema", JSON.stringify(action.schema))
            newState.facts = [];
            newState.relations = [];
            return newState
        default:
            break;
    }
    return newState;
}