import ConvertType from './ConvertType'
import AliCloud from '@/constant/imageUrl'

let ConvertForms = [
    {
        name: ConvertType.TALK,
        iconUrl: `${AliCloud}/convertType/factsheet.png`,
        generateIconUrl: `${AliCloud}/convertType/factsheet_black.png`
    },
    // {
    //     name: ConvertType.H5,
    //     iconUrl: '${AliCloud}/convertType/H5.png',
    //     generateIconUrl: '${AliCloud}/convertType/H5_black.png'
    // }
]
export default ConvertForms;