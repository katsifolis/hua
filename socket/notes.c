void producer {
	int item; /* data item */
	while (TRUE) {
		produce_item(&item);
		if (count == N) /* buffer full? */
		sleep(); /* wait */
		enter_item(item);
		count = count + 1; /* increase buffer full count */
		if (count == 1) /* empty ->not empty transition? */
		wakeup(consumer);
	}
}

void consumer {
	int item; /* data item */
	while (TRUE) {
		if (count == 0) /* buffer empty? */
		sleep(); /* wait */
		remove_item(&item);
		count = count - 1; /* reduce buffer full count */
		if (count == N - 1) /* not empty -> empty transition? */
		wakeup(producer);
		consume_item(item);
	}
}

void producer_sem {
	int item; /* data item */
	while (TRUE);
		produce_item(&item);
		down(&empty); /* wait for an empty */
		down(&mutex); /* wait for buffer use */
		enter_item(item);
		up(&mutex); /* release buffer */
		up(&full); /* increase full count */
	}
}

void consumer_sem {
	int item; /* data item */
	while (TRUE);
		down(&full); /* wait for a full */
		down(&mutex); /* wait for buffer use */
		remove_item(item);
		up(&mutex); /* release buffer */
		up(&empty); /* increase empty count */
		consume_item(&item);
	}
}

