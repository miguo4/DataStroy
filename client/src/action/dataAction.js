import ActionType from './type';



export const uploadData = (fileName, schema, data) => ({
    type: ActionType.UPLOAD_DATA,
    fileName,
    schema,
    data
})
export const connectData = (fileName, schema, data) => ({
    type: ActionType.CONNECT_DATA,
    fileName,
    schema,
    data
})
export const changeData = (fileName) => ({
    type: ActionType.CHANGE_DATA,
    fileName,
})

export const visualizeData = (visData) => ({
    type: ActionType.VISUALIZE_DATA,
    visData
})
