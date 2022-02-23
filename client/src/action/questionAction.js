import ActionType from './type';

export const updateQuestion = (question) => ({
    type: ActionType.UPDATE_QUESTION,
    question
})

export const saveCachedDecomposedQA = (QA) => ({
    type: ActionType.SAVE_CACHED_QA,
    cachedQA:QA
})