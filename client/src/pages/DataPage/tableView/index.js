import { connect } from 'react-redux';
import { data, schema } from '@/selector/story';
import * as userAction from '@/action/userAction';
import TableView from './TableView';

const mapStateToProps = (state) => ({
    data: data(state),
    schema: schema(state),
})

const mapDispatchToProps = dispatch => {
    return {
        updateColumnName: (columName) => dispatch(userAction.updateColumnName(columName))
    }

}

export default connect(mapStateToProps, mapDispatchToProps)(TableView);
