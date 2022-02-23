import {
    fact2visRules
} from './fact2visRule';
import {
    fact2visAllRules
} from './fact2visAllRule';
import FieldType from '@/constant/FieldType';

/****
 * 过滤规则： 根据fact.type 和 breakDown.type 筛选支持的图表
 * 其中isEdit===false表示生成阶段，生成阶段优先在推荐规则中过滤，如果找不到，会在全部支持的规则中过滤
 *     isEdit===ture表示编辑阶段，在全部支持的规则中过滤
 */

const getSupportedChartTypes = (fact, schema, isEdit = false) => {  
    
    let breakDown = schema.filter(s => s["field"] === fact.groupby[0])[0];
    let supportedChartTypes;
    let rules = isEdit ? fact2visAllRules : fact2visRules;//fact2visRules是推荐规则 
    supportedChartTypes = rules.filter(x => x.fact === fact.type);
    if (breakDown) {
        supportedChartTypes = supportedChartTypes.filter(x => x.breakdownType.indexOf(breakDown.type) !== -1);
        if (breakDown.type === FieldType.CATEGORICAL && breakDown.values) {
            supportedChartTypes = supportedChartTypes.filter(x => {
                if (!x.rang) {
                    return true
                } else {
                    return breakDown.values.length >= x.rang[0] && breakDown.values.length <= x.rang[1]
                }
            });
        }
        /*******important**** 找不到推荐的图表，就用可以支持的图表显示*****/
        if (supportedChartTypes.length === 0 && !isEdit) {
            supportedChartTypes = getSupportedChartTypes(fact, schema, true)
        }
        /*******important the end *********/
    }
    //console.log("supportedChartTypes", supportedChartTypes)
    return supportedChartTypes;
};
export default getSupportedChartTypes;