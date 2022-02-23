import { fact2visAllRules } from './fact2visAllRule';

const getSuitableBreakdownList = (factType, chartType, schema) => {
    //acording to factType ---> filter
    let suitableBreakdownList = fact2visAllRules.filter(x => x.fact === factType);

    //if has choosed chartType ---> filter
    if (chartType) {
        suitableBreakdownList = suitableBreakdownList.filter(x => x.chart === chartType);
    }
    if (suitableBreakdownList.length === 0) return [];
    let breakdownSets = new Set();
    suitableBreakdownList.forEach(x => {
        x.breakdownType.forEach(type => {
            breakdownSets.add(type)
        })
    })
    let breakdownList = Array.from(breakdownSets);
    //console.log("suitableBreakdownList", breakdownList)
    let suitableSchema = schema.filter(s => {
        return breakdownList.indexOf(s.type) !== -1
    })
    // suitableSchema = suitableSchema.map(shema => {
    //     return shema.field
    // })
    //console.log("suitableSchema", suitableSchema)
    return suitableSchema;
};
export default getSuitableBreakdownList;