import { connect } from 'react-redux';
import { operateState } from '@/selector/user';
import * as userAction from '@/action/userAction';

import PannelView from './PannelView';

const mapStateToProps = (state) => ({
    operateState: operateState(state)
})

const mapDispatchToProps = dispatch => {
    return {
        updateOperation: (operateState) => dispatch(userAction.updateOperation(operateState)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(PannelView);
