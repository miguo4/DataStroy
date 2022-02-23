//let calliopeService = 'calliope-service.idvxlab.com:8004';
let calliopeService = 'talk-api.idvxlab.com:8006';

let uploadPrefix = process.env.NODE_ENV === 'production' ? `https://${calliopeService}` : 'http://localhost:6028';//todo 
//let uploadPrefix = `https://${calliopeService}`
let generationUrlPrefix = process.env.NODE_ENV === 'production' ? `https://${calliopeService}` : 'http://localhost:6030';
//let generationUrlPrefix = `https://${calliopeService}`


const config = {
    url: {
        //upload
        uploadPrefix: uploadPrefix,
        uploadData: `${uploadPrefix}/upload`,
        share: `${uploadPrefix}/share`,
        fetch: `${uploadPrefix}/data/share`,
        //story generation
        factScoring: `${generationUrlPrefix}/fact`,
        generate: `${generationUrlPrefix}/generate`,
        candidateQuestions: `https://${calliopeService}/column2questions`,
    }
}
export default config