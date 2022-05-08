const socket = io();
console.log('here')
socket.emit('join', { device_type: 'phone' });
socket.on('notif', (frame) => {
    const actual_frame = frame.substring(2, frame.length-1);
    console.log(actual_frame)
    $('#video-frame').attr('src', 'data:image/jpg;base64,' + actual_frame);
});