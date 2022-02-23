import ActionType from './type';

export const addFact = (facts) => ({
    type: ActionType.ADD_FACT,
    facts: facts
})

export const updateFact = (index, fact) => ({
    type: ActionType.UPDATE_FACT,
    index,
    fact,
})

export const insertFact = (index, insert) => ({
    type: ActionType.INSERT_FACT,
    index,
    insert,
})

export const deleteFact = (index) => ({
    type: ActionType.DELETE_FACT,
    index,
})

export const deleteUnusedFact = (index) => ({
    type:ActionType.DELETE_UNUSEDFACT,
    index,
})

export const orderFacts = (sourceIndex, destinationIndex) => ({
    type: ActionType.ORDER_FACTS,
    sourceIndex,
    destinationIndex,
})

export const setHoverIndex = (index) => ({
    type: ActionType.SET_HOVER_INDEX,
    index
})