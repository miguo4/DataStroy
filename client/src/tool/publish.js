import LayoutType from '../constant/LayoutType';
import config from '@/axios/config';
let lang;
if (window.location.search) {
    lang = window.location.search.split('=')[1]
}
let URL = `${config.url.publicPrefix}?lang=${lang}#/publish/`

export const getPublishLink = (layout) => {
    let publishLink = ''
    switch (layout) {
        case LayoutType.STORYLINE_WEB:
            publishLink = URL + 'storyline/'
            break;

        case LayoutType.SLIDER_MOBILE:
            publishLink = URL + 'mobile/'
            break;

        case LayoutType.FACTSHEET:
            publishLink = URL + 'factsheet/'
            break;

        default:
            publishLink = URL + 'storyline/'
            break;
    }
    return publishLink
}

export const getEmbedLink = (layout) => {
    let embedLink = ''
    switch (layout) {
        case LayoutType.STORYLINE_WEB:
            embedLink = '<IFRAME name="storyline" width=1400 height=800 frameborder=0 src="' + URL + 'storyline/{{uuid}}"></IFRAME>'
            break;

        case LayoutType.SLIDER_MOBILE:
            embedLink = '<IFRAME name="mobile" width=300 height=530 frameborder=0 src="' + URL + 'mobile/{{uuid}}"></IFRAME>'
            break;

        case LayoutType.FACTSHEET:
            embedLink = '<IFRAME name="factsheet" width=1425 height=1166 frameborder=0 src="' + URL + 'factsheet/{{uuid}}"></IFRAME>'
            break;

        default:
            embedLink = '<IFRAME name="storyline" width=1400 height=800 frameborder=0 src="' + URL + 'storyline/{{uuid}}"></IFRAME>'
            break;
    }
    return embedLink
}
