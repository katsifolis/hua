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

function makeRequest() {
	/* Creating a new book to insert to the db */
	var tAuthor = document.getElementById('author').value;
	var tTitle = document.getElementById('title').value;
	var tGenre = document.getElementById('genre').value;
	var tPrice = document.getElementById('price').value;
	
	var b = new Book(tAuthor, tTitle, tGenre, tPrice);
	console.log(b);

	httpRequest = new XMLHttpRequest();

	if(!httpRequest) {
		alert('Failed');
	}
	var a = 2;

	httpRequest.onreadystatechange = alertContents;
	httpRequest.open('POST', '/books/');
	httpRequest.setRequestHeader('Content-Type', 'x-www-form-urlencoded');
	httpRequest.send('Just text'+a);

	function alertContents() {
		if (httpRequest.readyState === XMLHttpRequest.DONE) {
			if (httpRequest.status === 200) {
				console.log(httpRequest.response);
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

