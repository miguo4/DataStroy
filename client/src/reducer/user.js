import ActionType from '../action/type';
import Cookies from 'js-cookie';
import OperationType from '@/constant/OperationType'
import ConvertType from '@/constant/ConvertType'

let userInfo = Cookies.get("userInfo") && JSON.parse(Cookies.get("userInfo")) ? JSON.parse(Cookies.get("userInfo")) : {
    username: "",
    uid: -1
}


const initialState = {
    isLogin: userInfo.uid !== -1,
    userInfo: userInfo,
    operateState: OperationType.BEFORE_UPLOAD,// BEFORE_UPLOAD  UPLOADIND UPLOADED FILE_LARGE  GENERATING GENERATED PUBLISHED,
    convertType: ConvertType.FACTSHEET,
    currentLocale: '',
    isClosePannel: false,
    columName: '',
}

export default (state = initialState, action) => {
    const newState = Object.assign({}, state);
    switch (action.type) {
        case ActionType.UPDATE_USER_INFO:
            newState.userInfo = action.userInfo;
            if (action.userInfo.uid === -1) {
                newState.isLogin = false
            } else {
                newState.isLogin = true
            }
            return newState;

        case ActionType.UPDATE_USER_OPERATION:
            newState.operateState = action.operateState
            return newState;
        case ActionType.UPDATE_CONVERT_TYPE:
            newState.convertType = action.convertType
            return newState;
        case ActionType.UPDATE_LOCALE:
            newState.currentLocale = action.currentLocale
            return newState;
        case ActionType.CLOSE_PANNEL:
            newState.isClosePannel = action.isClose
            return newState;
        case ActionType.UPDATE_COLUMN_NAME:
            newState.columName = action.columName
            return newState;
        default:
            break;
    }
    return newState;
}