const { createProxyMiddleware } = require('http-proxy-middleware');
//1.0.0版本前都是用proxy,1.0.0后使用porxy会报错,应使用createProxyMiddleware;
module.exports = function (app) {
    app.use(
        createProxyMiddleware(
            '/generate',
            {
                target: 'https://talk-api.idvxlab.com:8006',
                changeOrigin: true,
            }
        )
    );
};