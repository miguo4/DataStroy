//import { createSelector } from 'reselect';
import Cookies from 'js-cookie';
export const schema = state => state.story.schema;
export const operateState = state => state.user.operateState;
export const isLogin = state => state.user.isLogin;
export const convertType = state => state.user.convertType;
export const currentLocale = state => state.user.currentLocale;
export const isClosePannel = state => state.user.isClosePannel;
export const columName = state => state.user.columName;



export const getUserInfo = state => {
    return Cookies.get("userInfo") && JSON.parse(Cookies.get("userInfo")) ? JSON.parse(Cookies.get("userInfo")) : {
        username: "",
        uid: -1
    }
}


