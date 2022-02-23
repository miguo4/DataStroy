import { connect } from 'react-redux';
import { fileName, schema } from '@/selector/story';
import { columName } from '@/selector/user';
import QuestionList from './QuestionList';
import * as questionAction from '@/action/questionAction';

const mapStateToProps = (state) => ({
    schema: schema(state),
    fileName: fileName(state),
    columName: columName(state)
})

const mapDispatchToProps = dispatch => {
    return {
        updateQuestion: (question) => dispatch(questionAction.updateQuestion(question)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(QuestionList);
