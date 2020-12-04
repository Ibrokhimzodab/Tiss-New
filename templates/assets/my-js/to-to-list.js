window.addEventListener('DOMContentLoaded', () => {

	const block = document.querySelectorAll('#colored');
	// const unselected = document.querySelectorAll('.team-face');
	// let selected = null;

	for (let i = 0; i < block.length; i++) {
		block[i].style.color = block[i].getAttribute("color");
		block[i].style.border = block[i].getAttribute("color") + " 1px solid";
	}

	// for (let i = 0; i < img_block.length; i++) {
	// 	document.addEventListener("click", function() {
	// 		console.log(img_block[i].style.border);
	// 		if (img_block[i].style.border === "3px solid white") {
	// 			img_block[i].style.border = "3px solid green";
	// 		} else {
	// 			img_block[i].style.border = "3px solid white";
	// 		}
	// 	})
	// }

	// let vs = document.querySelector('.team-face');

	// check.oninput = function () {
	// if (vs.checked) {
	// 	vs.classList.remove("item-vs");
	// 	vs.classList.add("item-ms");
	// } else {
	// 	vs.classList.remove("item-ms");
	// 	vs.classList.add("item-vs");
	// }
	// };

	// for (let i = 0; i<unselected.length; i++) {
	// 	document.addEventListener("click", function() {
	// 		if (unselected[i].classList.contains('team-face')) {
	// 			unselected[i].classList.remove('team-face');
	// 			unselected[i].classList.add('team-face-active');
	// 			if (selected[i] !== null || selected[i].classList.contains('team-face-active')) {
	// 				selected.classList.remove('team-face-active');
	// 				selected[i].classList.add('team-face');
	// 			} 
	// 			selected = unselected[i];
	// 		}
	// 		else if (unselected[i].classList.contains('team-face-active')) {
	// 			selected.classList.remove('team-face-active');
	// 			unselected[i].classList.add('team-face');
	// 			selected = null;
	// 		}
	// 	})
	// }

	// document.querySelector('.team-face').onclick = function (e) {
	// 	var nav = document.querySelector('#mainnav');
	// 	nav.classList.toggle('show');
	// 	e.preventDefault();
	//   }

});
