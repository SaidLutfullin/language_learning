$(document).ready(function($) {
    const front = document.getElementById('front');
    const back = document.getElementById('back');
    const btn1 = document.getElementById('flip-btn1');
    const btn2 = document.getElementById('flip-btn2');
    function handleFlip() {
        front.classList.toggle('flippedF')
        back.classList.toggle('flippedB')
    }
    btn1.addEventListener('click', handleFlip)
    btn2.addEventListener('click', handleFlip)
});