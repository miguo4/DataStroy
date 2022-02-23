import { createSelector } from 'reselect';
import { storyAggregation } from '../tool/factAggregation';

// data
export const fileName = state => state.story.fileName;
export const title = state => state.story.title;
export const data = state => state.story.data;
export const schema = state => state.story.schema;
// story
const originFacts = state => state.story.facts;
export const relations = state => state.story.relations;
export const method = state => state.story.method;
export const maxStoryLength = state => state.story.maxStoryLength;
export const chartDiversity = state => state.story.chartDiversity;
export const information = state => state.story.information;
export const timeLimit = state => state.story.timeLimit;
export const resultCoverage = state => state.story.resultCoverage;
export const aggregationLevel = state => state.story.aggregationLevel;
export const rewardWeight = state => state.story.rewardWeight;
export const historyStory = state => state.story.historyStory;
export const generateProgress = state => state.story.generateProgress;


export const facts = createSelector(
    originFacts,
    aggregationLevel,
    function (originFacts, aggregationLevel) {
        return storyAggregation(originFacts, aggregationLevel)
    }
)


export const storyParameter = createSelector(
    maxStoryLength,
    information,
    chartDiversity,
    timeLimit,
    function (maxStoryLength, information, chartDiversity, timeLimit) {
        return {
            maxStoryLength: maxStoryLength,
            information: information,
            chartDiversity: chartDiversity,
            timeLimit: timeLimit,
        }
    }
)

