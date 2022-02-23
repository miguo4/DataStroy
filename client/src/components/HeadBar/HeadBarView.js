import React, { Component } from 'react';
import { Avatar, Divider } from 'antd';
import LocaleConfigView from './LocaleConfig/LocaleConfigView'
import config from '../../axios/config';
import Cookies from 'js-cookie';
//import * as api from '@/axios/api';
import './HeadBarView.less';

export default class HeadBarView extends Component {

    getUser = () => {
        window.open(config.url.authenUrl, '_blank')
    }
    clickBtn = () => {
        const { isLogin } = this.props;
        //console.log("isLogin", isLogin)
        if (isLogin) {
            this.logout()
        } else {
            this.login()
        }
    }
    login = () => {
        this.props.updateUserInfo({
            username: "Test",
            uid: 1
        });

        Cookies.set("userInfo", {
            username: "Test",
            uid: 1
        })
    }
    logout = () => {
        this.props.updateUserInfo({
            username: "",
            uid: -1
        });
        Cookies.set("userInfo", {
            username: "",
            uid: -1
        })
    }
    back = () => {
        this.props.history.push("/")
    }
    render() {
        const { intl, initDone, isLogin, userInfo } = this.props;

        return (
            <div className="headerBarWrapper" >
                <div className="headerBarLeft">
                    <div onClick={this.back}></div>
                    <span>{initDone && intl.get("calliope-talk")}</span>
                </div>
                <div style={{ flex: 1, height: "50px" }}></div>
                <div className='headerBarRight'>
                    {
                        isLogin ?
                            <Avatar className='AvatarImg' style={{ display: "none" }}
                                onClick={this.getUser}
                                src={`${config.url.userImage}/${userInfo.avatar}`}
                            >{userInfo && userInfo.username.substr(0, 1)}</Avatar>
                            :
                            <div className='defaultimg' type=' ' style={{ display: "none" }}></div>
                    }
                    <Divider type="vertical" style={{ display: "none" }}></Divider>
                    <div className='LogInBt' style={{ display: "none" }} onClick={this.clickBtn} >{isLogin ? intl.get("logOut") : intl.get("logIn")}</div>
                    <div >
                        <LocaleConfigView {...this.props} />
                    </div>
                </div>
            </div >
        )
    }
}