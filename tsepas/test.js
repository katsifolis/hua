'use strict';

var book = {
	author: "Tolkien",
	title: "Lord of the rings",
	genre: "fantasy",
	price: 20

}

function Book(author, title, genre, price) {
	this.author = author;
	this.title = title;
	this.genre = genre;
	this.price = price;

}
var httpRequest;

document.getElementById('ajaxCall').addEventListener('click', makeRequest);

//document.getElementById('ajaxCall').onclick = function() {
//};

function makeRequest() {

	var tAuthor = document.getElementById('author').value;
	var tTitle = document.getElementById('title').value;
	var tGenre = document.getElementById('genre').value;
	var tPrice = document.getElementById('price').value;
	
	var b = new Book(tAuthor, tTitle, tGenre, tPrice);
	console.log(JSON.stringify(b));

	httpRequest = new XMLHttpRequest();

	if(!httpRequest) {
		alert('Failed');
	}

	httpRequest.onreadystatechange = alertContents;
	httpRequest.open('GET', 'index.html', true);
	httpRequest.send();

	function alertContents() {
		if (httpRequest.readyState === XMLHttpRequest.Done) {
			if (httpRequest.status === 200) {
				var response = httpRequest.responseText;
				alert(response);
				} else {
					alert('There was a problem');
				}
		}

	}
}

let user = {
	name: "John",
	lastName: "Doe",
	sayHi() {
		console.log('Hey');
		let sayBye = () => console.log('Bye');
	}
};

function User(name, lastName) {
	this.name = name;
	this.lastName = lastName;
}

