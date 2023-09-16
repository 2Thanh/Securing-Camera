function getClientX(event) {
    if (event.touches) {
        return event.touches[0].clientX;
    }
    return event.clientX;
}

function startDrag(e, isDragging, updateBarValue, bar, dragger, valueDisplay, barContainer) {
    isDragging.value = true;
    e.preventDefault();
    updateBarValue(getClientX(e), bar, dragger, valueDisplay, barContainer);
}

function drag(e, isDragging, updateBarValue, bar, dragger, valueDisplay, barContainer) {
    if (isDragging.value) {
        e.preventDefault();
        updateBarValue(getClientX(e), bar, dragger, valueDisplay, barContainer);
    }
}

function stopDrag(isDragging) {
    isDragging.value = false;
}

function updateBarValue(clientX, bar, dragger, valueDisplay, barContainer) {
    const containerLeft = barContainer.getBoundingClientRect().left;
    const mouseXRelative = clientX - containerLeft;
    const maxWidth = barContainer.clientWidth;
    const newWidth = Math.max(0, Math.min(maxWidth, mouseXRelative));
    const percentageWidth = newWidth / maxWidth;

    const minValue = 0;
    const maxValue = 180;
    const newValue = Math.round(minValue + percentageWidth * (maxValue - minValue));

    bar.style.width = percentageWidth * 100 + '%';
    dragger.style.left = percentageWidth * 100 + '%';

    valueDisplay.textContent = newValue;
    return newValue
}

// First Bar Elements
const dragger1 = document.getElementById('dragger1');
const valueDisplay1 = document.getElementById('valueDisplay1');
const bar1 = document.getElementById('bar1');
const barContainer1 = document.querySelectorAll('.bar-container')[0];
const isDragging1 = { value: false };

dragger1.addEventListener('mousedown', (e) => startDrag(e, isDragging1, updateBarValue, bar1, dragger1, valueDisplay1, barContainer1));
dragger1.addEventListener('touchstart', (e) => startDrag(e, isDragging1, updateBarValue, bar1, dragger1, valueDisplay1, barContainer1));

document.addEventListener('mousemove', (e) => drag(e, isDragging1, updateBarValue, bar1, dragger1, valueDisplay1, barContainer1));
document.addEventListener('touchmove', (e) => drag(e, isDragging1, updateBarValue, bar1, dragger1, valueDisplay1, barContainer1));

document.addEventListener('mouseup', () => stopDrag(isDragging1));
document.addEventListener('touchend', () => stopDrag(isDragging1));

// Second Bar Elements
const dragger2 = document.getElementById('dragger2');
const valueDisplay2 = document.getElementById('valueDisplay2');
const bar2 = document.getElementById('bar2');
const barContainer2 = document.querySelectorAll('.bar-container')[1];
const isDragging2 = { value: false };

dragger2.addEventListener('mousedown', (e) => startDrag(e, isDragging2, updateBarValue, bar2, dragger2, valueDisplay2, barContainer2));
dragger2.addEventListener('touchstart', (e) => startDrag(e, isDragging2, updateBarValue, bar2, dragger2, valueDisplay2, barContainer2));

document.addEventListener('mousemove', (e) => drag(e, isDragging2, updateBarValue, bar2, dragger2, valueDisplay2, barContainer2));
document.addEventListener('touchmove', (e) => drag(e, isDragging2, updateBarValue, bar2, dragger2, valueDisplay2, barContainer2));

document.addEventListener('mouseup', () => stopDrag(isDragging2));
document.addEventListener('touchend', () => stopDrag(isDragging2));
//newValue_vertical

document.getElementById("sendButton").addEventListener("click", function () {
    let dataToSend = {
        newValue1: parseInt(valueDisplay1.textContent), // Extract value from valueDisplay1
        newValue2: parseInt(valueDisplay2.textContent)  // Extract value from valueDisplay2
    };

    fetch("/send_data", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ data: dataToSend })
    })
    .then(response => response.text())
    .then(data => {
        console.log(data); // Print the response from the server
    })
    .catch(error => {
        console.error("Error:", error);
    });
});


document.getElementById("Capture").addEventListener("click", function () {
    let dataToSend = 1;

    fetch("/requests", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ data: dataToSend })
    })
        .then(response => response.text())
        .then(data => {
            console.log(data); // Print the response from the server
        })
        .catch(error => {
            console.error("Error:", error);
        });
});