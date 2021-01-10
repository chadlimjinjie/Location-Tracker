const nameInput = document.getElementById("name");
const submitButton = document.getElementById("submit-button");

submitButton.addEventListener("click", function(e) {
  e.preventDefault();
  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(postLocation);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
  nameInput.setAttribute("disabled", "");
  submitButton.setAttribute("disabled", "");
});

function postLocation(position) {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;
  console.log(nameInput.value);
  name = nameInput.value;
  const data = {
    latitude,
    longitude
  };
  fetch("https://location-tracker.chadlim1.repl.co/PostLocation/" + name, {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data),
  })
};
