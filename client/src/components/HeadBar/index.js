import { connect } from 'react-redux';
import HeadBarView from './HeadBarView';
import { isLogin, getUserInfo } from "@/selector/user";
import * as userAction from '../../action/userAction';

const mapStateToProps = (state) => ({
    //user
    isLogin: isLogin(state),
    userInfo: getUserInfo(state)
})

const mapDispatchToProps = dispatch => {
    return {
        updateUserInfo: (userInfo) => dispatch(userAction.updateUserInfo(userInfo)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(HeadBarView);
