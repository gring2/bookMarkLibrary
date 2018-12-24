const webpack = require('webpack');
const path = require('path');
module.exports = {
  mode: 'development',
  entry: {
    app: path.join(__dirname, 'bookMarkLibrary/static/js/app.js')
  },
  output: {
    path: path.join(__dirname, 'bookMarkLibrary/static/dist/js'),
    filename: 'dist.js',
    publicPath: '',
  },
  module: {

  },
  plugins: [],
  optimization: {},
  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.json', '.jsx', '.css'],
  },
};