// USER REGISTRATION FUNCTION
function registerUser() {
    const name = document.getElementById("register_name").value;
    const email = document.getElementById("register_email").value;
    const password = document.getElementById("register_password").value;

    fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("register_message").innerText = data.message || data.error;
        if (data.message === "User registered successfully!") {
            window.location.href = "/login-page";  // Redirect after successful registration
        }
    })
    .catch(error => console.error("Error:", error));
}


// USER LOGIN FUNCTION
function loginUser() {
    const email = document.getElementById("login_email").value;
    const password = document.getElementById("login_password").value;

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("login_message").innerText = data.message || data.error;
        if (data.message === "Login successful") {
            localStorage.setItem("user_email", email);
            window.location.href = "/dashboard-page";
        }
    })
    .catch(error => console.error("Error:", error));
}

// SLOT RESERVATION FUNCTION
function reserveSlot() {
    const station_id = document.getElementById("station_id").value;
    const slot_number = document.getElementById("slot_number").value;
    const date = document.getElementById("date").value;
    const time = document.getElementById("time").value;
    const email = localStorage.getItem("user_email"); // Retrieve user email

    if (!email) {
        alert("Please log in first!");
        window.location.href = "/login-page";
        return;
    }

    fetch("/reserve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, station_id, slot_number, date, time })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById("reservation_message").innerText = data.message;
            document.getElementById("reservation_message").style.color = "green";
        } else {
            document.getElementById("reservation_message").innerText = data.error;
            document.getElementById("reservation_message").style.color = "red";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Reservation failed. Please check console for errors.");
    });
}



// PREDICT MILEAGE FUNCTION (Debugging Enabled)
function predictMileage() {
    const odometer = document.getElementById("odometer").value;
    const battery_health = document.getElementById("battery_health").value;

    console.log("Sending Mileage Prediction Request:", { odometer, battery_health });

    fetch("/predict/mileage", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ odometer, battery_health })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response:", data);
        if (data.predicted_mileage) {
            document.getElementById("mileage_result").innerText = `Predicted Mileage: ${data.predicted_mileage}`;
        } else {
            document.getElementById("mileage_result").innerText = "Error: " + data.error;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Prediction failed. Check the console for details.");
    });
}


// PREDICT MILEAGE FUNCTION
function predictMileage() {
    const odometer = document.getElementById("odometer").value;
    const battery_health = document.getElementById("battery_health").value;

    fetch("/predict/mileage", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ odometer, battery_health })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("mileage_result").innerText = data.predicted_mileage
            ? `Predicted Mileage: ${data.predicted_mileage}`
            : "Error: " + data.error;
    })
    .catch(error => console.error("Error:", error));
}

// PREDICT BATTERY HEALTH FUNCTION
function predictBatteryHealth() {
    const charging_cycles = document.getElementById("charging_cycles").value;
    const age = document.getElementById("battery_age").value;

    fetch("/predict/battery", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ charging_cycles, age })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("battery_result").innerText = data.predicted_battery_health
            ? `Predicted Battery Health: ${data.predicted_battery_health}`
            : "Error: " + data.error;
    })
    .catch(error => console.error("Error:", error));
}

// LOGOUT FUNCTION
function logoutUser() {
    localStorage.removeItem("user_email");
    window.location.href = "/login-page";
}
