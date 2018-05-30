// Simple http server

var express = require('express');
var app = express();
var mysql = require('mysql');

app.use(express.static('./'));
//app.use(bodyParser.json());
//app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded


app.post('/books/', function(req, res){
	res.send(req.body);
	res.send(req.headers);
});



app.listen(8081, () => console.log('Listening on port 8081'));



