function age() {
    var now = new Date();
    var birthday = new Date(2004, 1, 19);
    var elapsed = now - birthday;
    var ageInYears = Math.floor(elapsed / (1000 * 60 * 60 * 24 * 365.25));
    return ageInYears + " years old";
}
document.getElementById("age").innerHTML = age();