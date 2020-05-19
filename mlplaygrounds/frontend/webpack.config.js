const path = require('path')

const NORMALIZE_PATH = path.resolve(
  __dirname,
  "./node_modules/normalize.css/normalize.css"
);

const BLUEPRINT_CORE_PATH = path.resolve(
  __dirname,
  "./node_modules/@blueprintjs/core/lib/css/blueprint.css"
);

const BLUEPRINT_ICONS_PATH = path.resolve(
  __dirname,
  "./node_modules/@blueprintjs/icons/lib/css/blueprint-icons.css"
);

module.exports = {
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.css$/i,
        exclude: /node_modules/,
        use: ['style-loader', 'css-loader'],
      }
    ]
  }
};