function showHiddenForm() {
    console.log("Hi!");
    var form = document.getElementById("account-image-form");
    var button = document.getElementById("action-button");
    console.log(form.style);
    if (form.style.display != "block") {
        form.style.display = "block";
        button.innerHTML = "Hide Profile Picture Manager"
    }
    else {
        form.style.display = "none";
         button.innerHTML = "Show Profile Picture Manager";
    }
}