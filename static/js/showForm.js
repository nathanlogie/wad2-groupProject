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

function setBorrowMenu(menu){
    const user_bookings = document.getElementById("user-bookings");
    const all_bookings = document.getElementById("all-bookings");
    const user_bookings_title = document.getElementById("user-bookings-title");
    const all_bookings_title = document.getElementById("all-bookings-title");
    if (menu == "user"){
        user_bookings.style.display = "block"
        all_bookings.style.display = "none"
        user_bookings_title.style.textDecoration = "underline"
        all_bookings_title.style.textDecoration = "none"
    }else if (menu == "all"){
        all_bookings.style.display = "block"
        user_bookings.style.display = "none"
        all_bookings_title.style.textDecoration = "underline"
        user_bookings_title.style.textDecoration = "none"
    }
}