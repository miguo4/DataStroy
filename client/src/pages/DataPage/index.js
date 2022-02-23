import { connect } from 'react-redux';
import DataPage from './DataPage';
import * as dataAction from '@/action/dataAction';
import * as userAction from '@/action/userAction';
import { fileName, data } from '@/selector/story';
import * as questionAction from '@/action/questionAction';

const mapStateToProps = (state) => ({
    fileName: fileName(state),
    data: data(state)
})

const mapDispatchToProps = dispatch => {
    return {
        updateQuestion: (question) => dispatch(questionAction.updateQuestion(question)),
        //data
        uploadData: (fileName, schema, data) => dispatch(dataAction.uploadData(fileName, schema, data)),
        //user
        closePannel: (isClose) => dispatch(userAction.closePannel(isClose)),
        saveCachedDecomposedQA: (QA) => dispatch(questionAction.saveCachedDecomposedQA(QA))
    }

}

export default connect(mapStateToProps, mapDispatchToProps)(DataPage);
