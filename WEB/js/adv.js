const advBanner = document.querySelectorAll(".banner-image");
const advSelector = document.querySelectorAll(".adv-page-selector");
const logo = document.querySelector("#header-logo");

let idx = 0;
let i = 0;
let advSwitch = true;
function advertisement() {
    if(advSwitch) {
        changeAdv(i);
        changeAdvSelector(i);
        i++;
    
        if(i > 3) {
            i = 0;
        }
    } else {
        
    }
}

function changeAdv(idx) {
    advBanner.forEach(adv => adv.style.zIndex = 0);
    advBanner[idx].style.zIndex = 1;
}

function changeAdvSelector(idx) {
    advSelector.forEach(s => s.style.backgroundColor = "white");
    advSelector[idx].style.backgroundColor = "black";
}

for(let i=0; i<advSelector.length; i++) {
    advSelector[i].addEventListener("click", advSelect);
}

function advSelect(event) {
    advIndex = parseInt(event.srcElement.id.substr(-1));
    clearInterval(advInterval);
    i = advIndex - 1;
    advertisement()
    advInterval = setInterval(advertisement, 2000);
}

advertisement()
let advInterval = setInterval(advertisement, 2000);