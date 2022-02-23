import ActionType from './type';

export const selectFact = (index) => ({
    type: ActionType.SELECT_FACT,
    index
})

export const changeMethod = (method) => ({
    type: ActionType.CHANGE_METHOD,
    method,
})

export const setStoryParameter = (maxStoryLength, information, chartDiversity, timeLimit) => ({
    type: ActionType.SET_STORY_PARAMETER,
    maxStoryLength,
    information,
    chartDiversity,
    timeLimit,
})

export const setRewardWeight = (logicality, diversity, integrity) => ({
    type: ActionType.SET_REWARD_WEIGHT,
    logicality,
    diversity,
    integrity,
})

export const setAggregationLevel = (level) => ({
    type: ActionType.SET_AGGREGATION_LEVEL,
    level,
})

export const generateStory = (facts, relations, coverage) => ({
    type: ActionType.GENERATE_STORY,
    facts,
    relations,
    coverage,
})
export const updateProgress = (totalLength, currentLength) => (
    {
        type: ActionType.UPDATE_PROGRESS,
        totalLength,
        currentLength
    }
)
export const exportPdf = (isExportPdf) => (
    {
        type: ActionType.EXPORT_PDF,
        isExportPdf
    }
)
export const changeTitle = (title) => ({
    type: ActionType.CHANGE_TITLE,
    title,
})
export const updateCommentStoryInfo = (facts, relations, data, schema, title, fileName, storyParameter, aggregationLevel, resultCoverage) => ({
    type: ActionType.UPDATE_COMMENT_STORY_INFO,
    facts,
    relations,
    data,
    schema,
    title,
    storyParameter,
    aggregationLevel,
    resultCoverage,
    fileName
})
export const updateUUID = (uuid) => ({
    type: ActionType.UPDATE_UUID,
    uuid,
})
