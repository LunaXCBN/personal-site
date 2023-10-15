function age() {
    var now = new Date();
    var birthday = new Date(2004, 1, 19);
    var elapsed = now - birthday;
    var ageInYears = Math.floor(elapsed / (1000 * 60 * 60 * 24 * 365.25));
    return ageInYears + " years old";
}
document.getElementById("age").innerHTML = age();

async function getStatus(url = "", data = {}) {
    var opts = {
        headers: {
            "mode":"no-cors"
        }
    }
    fetch("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=E88C8F550DFA5B17B4156616A25C6893&format=json&steamids=76561198148554560")
        .then(response => response.json())
        .then(data => console.log(data))
        .then(error => console.error('Error:', error));
}