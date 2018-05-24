// Simple http server

var express = require('express');
var app = express();
var mysql = require('mysql');

app.use(express.static('./'));

app.post('/books/', function(req, res){
	res.send('books');
	
});


app.listen(8081, () => console.log('Listening on port 8081'));



