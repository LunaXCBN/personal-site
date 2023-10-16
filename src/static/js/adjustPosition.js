window.addEventListener('resize', adjustPosition);

function adjustPosition() {
    var song = document.getElementById('song');
    var heightBefore = song.offsetHeight;
    song.style.marginBottom = '-1000px';
    var heightOneLine = song.offsetHeight;

    song.style.marginBottom = '';

    var lines = heightBefore / heightOneLine;
    song.style.top = (-7 * lines) + 'px';
}