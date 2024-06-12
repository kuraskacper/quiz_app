function toggleNav() {
  var x = document.getElementById("topnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

function closeMessage(element) {
  var div = element.parentElement;
  div.style.display = "none";
}

