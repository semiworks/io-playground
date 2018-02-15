var path = require('path')
const webpack = require('webpack');

const config = {
    entry:  __dirname + '/js/app.js',

    output: {
        path: __dirname + '/public/js',
        filename: 'bundle.js',
    },

    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            }
        ]
    },

    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            '@': path.resolve(__dirname, 'js')
        }
    }
};

module.exports = config;
