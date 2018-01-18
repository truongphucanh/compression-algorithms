var express	=	require("express");
var bodyParser =	require("body-parser");
var path = require('path');
var app	=	express();
const config = require('./config.json');
var file = require('./routes/file.js');

app.use(bodyParser.urlencoded({
  extended: true,
  limit: '100mb'
}));

app.use(bodyParser.json());
//app.use(express.json({limit: '50mb'}));

app.use('/v1/file', file);

app.use(express.static(path.resolve('./public')));
app.use('/bower_components', express.static(path.join(__dirname + '/bower_components/')));

app.get('/',function(req,res){
  res.sendFile(__dirname + "/public/index.html");
});

app.listen(config.apiPort, function () {
  console.log("API is working on localhost:" + config.apiPort);
})

