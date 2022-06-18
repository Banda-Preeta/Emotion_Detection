const path = window.location.href;
const predictions = document.getElementById("predictions").children;
const img = document.getElementById("image");
const route = window.location.href;
const results = '/static/result/result.json';

const EMOTIONS = [
  "angry",
  "confident",
  "confused",
  "contempt",
  "crying",
  "disgust",
  "fear",
  "happy",
  "neutral",
  "sad",
  "shy",
  "sleepy",
  "surprised",
];
async function GetData() {
  fetch(results)
    .then(async (response) => {
      await HandleResponse(response);
    })
    .catch((data) => console.error(data));
}

async function HandleResponse(response) {
  const data = await response.json();
  if (data["detected"] === true) {
    img.style.borderColor = "green";
    displayData(data["pred"]);
  } else {
    img.style.borderColor = "red";
  }
}
async function displayData(pred) {
  for (let i = 0; i < predictions.length; i++) {
    const percentage = Math.floor(pred[EMOTIONS[i]] * 100);
    predictions[i].children[1].innerText = percentage.toString() + "%";
    predictions[i].children[2].children[0].style.width =
      (percentage * 0.75).toString() + "%";
    predictions[i].children[2].children[0].style.backgroundColor =
      getcolor(percentage);
  }
}

async function getcolor(value) {
  if (value > 75) {return "red";}
     else if (value > 50) {return "orange";  } 
  else if (value > 25) {return "yellow";  }
   else {return "black";  }
}
setInterval(GetData,3000);
