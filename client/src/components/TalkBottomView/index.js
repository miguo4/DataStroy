import { connect } from 'react-redux';
import { isClosePannel } from '@/selector/user';
import * as userAction from '@/action/userAction';
import TalkBottom from './TalkBottom';

const mapStateToProps = (state) => ({
    isClosePannel: isClosePannel(state),
})

const mapDispatchToProps = dispatch => {
    return {
        //user
        closePannel: (isClose) => dispatch(userAction.closePannel(isClose))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(TalkBottom);
