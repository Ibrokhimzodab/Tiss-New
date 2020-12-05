document.addEventListener('DOMContentLoaded', () => {

	const block = document.querySelectorAll('#colored');
	const btn = document.querySelectorAll('.team-face');

	for (let i = 0; i < block.length; i++) {
		block[i].style.color = block[i].getAttribute("color");
		block[i].style.border = block[i].getAttribute("color") + " 1px solid";
	}

	for (let i = 0; i <= btn.length; i++) {
		const user = document.getElementById(`user-${i}`);
		user.onclick = () => {
			user.classList.toggle('team-face-active');
		}
	}
	
});
