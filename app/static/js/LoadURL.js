function LoadURL() {
    var nitrogen = document.getElementById("validationNitrogen").value;
    var phosphorus = document.getElementById("validationPhosphorus").value;
    var potassium = document.getElementById("validationPotassium").value;
    var pH = document.getElementById("validationPH").value;
    var rainfall = document.getElementById("validationRainfall").value;
    var state = document.getElementById("validationState").value;
    var city = document.getElementById("validationCity").value;
    var server = window.location.origin;
    var path = "/crop-prediction/" + nitrogen + "/" + phosphorus + "/" + potassium + "/" + pH + "/" + rainfall + "/" + state + "/" + city;
    var url = server + path;
    window.location.href = url;
}