import { connect } from 'react-redux';
import { fileName, schema, relations, storyParameter, maxStoryLength, data, resultCoverage, aggregationLevel, facts, rewardWeight, title, generateProgress } from '@/selector/story';
import { cachedQA, isUpdateLayout, editedTitle } from '@/selector/question';
import * as dataAction from '@/action/dataAction';
import * as storyAction from '@/action/storyAction';
import * as userAction from '@/action/userAction';
import * as questionAction from '@/action/questionAction';

import Dashboard from './dashboard';

const mapStateToProps = (state) => ({
    schema: schema(state),
    // facts: facts(state),
    relations: relations(state),
    data: data(state),
    title: title(state),
    resultCoverage: resultCoverage(state),
    fileName: fileName(state),
    storyParameter: storyParameter(state),
    maxStoryLength: maxStoryLength(state),
    rewardWeight: rewardWeight(state),
    aggregationLevel: aggregationLevel(state),
    generateProgress: generateProgress(state),
    cachedQA: cachedQA(state),
    isUpdateLayout: isUpdateLayout(state),
    editedTitle: editedTitle(state)
})

const mapDispatchToProps = dispatch => {
    return {
        //data
        uploadData: (fileName, schema, data) => dispatch(dataAction.uploadData(fileName, schema, data)),
        //story
        generateStory: (facts, relations, coverage) => dispatch(storyAction.generateStory(facts, relations, coverage)),
        updateProgress: (totalLength, currentLength) => dispatch(storyAction.updateProgress(totalLength, currentLength)),
        //question
        updateQuestion: (question) => dispatch(questionAction.updateQuestion(question)),
        saveCachedDecomposedQA: (QA) => dispatch(questionAction.saveCachedDecomposedQA(QA)),
        //user
        updateCovertType: (covertType) => dispatch(userAction.updateCovertType(covertType)),
        updateOperation: (operateState) => dispatch(userAction.updateOperation(operateState)),
        editTitle: (title) => dispatch(userAction.editTitle(title)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Dashboard);
