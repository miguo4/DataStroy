import config from '@/axios/config';
import axios from 'axios';

export async function uploadData(formData) {
    return new Promise((reslove, reject) => {
        axios({
            method: "post",
            url: `${config.url.uploadData}`,
            config: {
                "headers": {
                    'Content-Type': 'multipart/form-data' //application/json; charset=utf-8
                },
            },
            data: formData
        }).then((response) => {
            if (response.status >= 400) {
                reject();
            } else if (response.status === 200 || response.status === 201 || response.status === 204) {
                reslove(response.data);
            } else {
                reject();
            }
        }).catch(error => {
            reject();
            //  message.error('error message');
        })
    })
}


export function generate(data) {
    return axios({
        method: "post",
        url: `${config.url.generate}`,
        config: {
            "headers": {
                'Content-Type': 'application/json; charset=utf-8'
            },
        },
        data: data
    })
}

export function getQuestions(data) {
    return axios({
        method: "post",
        url: `${config.url.candidateQuestions}`,
        config: {
            "headers": {
                'Content-Type': 'application/json; charset=utf-8'
            },
        },
        data: data
    })
}
export function factScoring(filename, fact, method) {
    return axios({
        "method": "POST",
        "url": config.url.factScoring,
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
        },
        "data": {
            "file_name": filename,
            "fact": fact,
            "method": method,
        }
    })
}

export async function shareStory(jsonstring) {
    return new Promise((reslove, reject) => {
        axios({
            method: "post",
            url: `${config.url.share}`,
            config: {
                "headers": {
                    'Content-Type': 'application/json; charset=utf-8'
                },
            },
            data: {
                "share_json": jsonstring
            }
        }).then((response) => {
            if (response.status >= 400) {
                reject();
            } else if (response.status === 200 || response.status === 201 || response.status === 204) {
                reslove(response.data);
            } else {
                reject();
            }
        }).catch(error => {
            reject();
            //  message.error('error message');
        })
    })
}

export async function fetchStory(id) {
    return axios({
        method: "get",
        "url": `${config.url.fetch}/${id}.json`,
        config: {
            "headers": {
                'Content-Type': 'application/json; charset=utf-8'
            },
        }
    })
}
/*****
 *????????????
 ssr(????????????)???koa(koa-views)????????????????????????????????????pdf?????????)
 node.js ??????pdf?????? puppeteer???????????????????????????PDF
 koa-send???????????????PDF??????????????????????????? 
 * 
 data????????????????????????????????????
 */
export function generatePDF(data) {
    return axios({
        method: 'post',
        url: `/generatePDF`,
        param: {},
        data: data
    })
}
