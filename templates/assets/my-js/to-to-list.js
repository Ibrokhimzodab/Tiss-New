window.addEventListener('DOMContentLoaded', () => {

	const block = document.querySelectorAll('#colored');

	for (let i = 0; i < block.length; i++) {
		block[i].style.color = block[i].getAttribute("color");
		block[i].style.border = block[i].getAttribute("color") + " 1px solid";
	}

});
