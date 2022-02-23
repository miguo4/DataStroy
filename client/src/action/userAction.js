import ActionType from './type';


export const updateUserInfo = (userInfo) => ({
    type: ActionType.UPDATE_USER_INFO,
    userInfo
})

export const updateOperation = (operateState) => ({
    type: ActionType.UPDATE_USER_OPERATION,
    operateState
})

export const updateQustion = (question) => ({
    type: ActionType.UPDATE_USER_OPERATION,
    question
})
export const updateColumnName = (columName) => ({
    type: ActionType.UPDATE_COLUMN_NAME,
    columName
})
export const updateCovertType = (convertType) => ({
    type: ActionType.UPDATE_CONVERT_TYPE,
    convertType
})

export const updateLocale = (currentLocale) => ({
    type: ActionType.UPDATE_LOCALE,
    currentLocale
})

export const closePannel = (isClose) => ({
    type: ActionType.CLOSE_PANNEL,
    isClose
})

export const editTitle = (title) => ({
    type: ActionType.EDIT_TITLE,
    title
})
