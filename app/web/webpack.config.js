var path = require('path')
const webpack = require('webpack');

const config = {
    entry:  __dirname + '/frontend/app.js',

    output: {
        path: __dirname + '/public/js',
        filename: 'bundle.js',
    },

    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
			{
				test: /\.js$/,
				loader: 'babel-loader'
			},
			{
				test: /\.css$/,
				use: [ 'style-loader', 'css-loader' ]
			},
			{
				test: /\.(png|woff|woff2|eot|ttf|svg)$/,
				loader: 'url-loader?limit=100000'
			}
		]
    },

    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            '@': path.resolve(__dirname, 'frontend')
        }
    },

    plugins: [
        new webpack.LoaderOptionsPlugin({
            options:
            {
                context: process.cwd()
            }
        })
    ]
};

module.exports = config;
