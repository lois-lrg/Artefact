function sendCommand(direction) {
    fetch('/move', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ direction: direction })
    });
}

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowUp') sendCommand('forward');
    else if (event.key === 'ArrowDown') sendCommand('backward');
    else if (event.key === 'ArrowLeft') sendCommand('left');
    else if (event.key === 'ArrowRight') sendCommand('right');
    else if (event.key === ' ') sendCommand('stop');
});