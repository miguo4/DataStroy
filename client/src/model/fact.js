// import {genFactSentence,genSubtitle} from '../sentencer';

export default class Fact {
    constructor(type, measure = [], subspace = [], groupby = [], focus = [], parameter = [], chart = "", score = 0, information = 0, significance = 0) {
        this.type = type;
        this.measure = measure;
        this.subspace = subspace;
        this.groupby = groupby;
        this.focus = focus;
        this.parameter = parameter;
        this.score = score;
        this.information = information;
        this.significance = significance;
        this.chart = chart;
        // this.generatedScript = genFactSentence(this);
        // this.generatedSubtitle = genSubtitle(this)
        // Compound Fact
        this.aggregated = false;
        this.aggregatedFact = null;
        this.compoundType = '';
        this.compoundChart = 'juxtaposition';
    }
    script = () => this.generatedScript;
}