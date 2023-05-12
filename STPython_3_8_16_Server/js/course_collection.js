function course_collection() {
    const socket = new WebSocket('ws://' + location.host + '/stCloudCourse/courseCollection/ws');

    socket.addEventListener('open', () => {
        console.log('WebSocket connection opened');
    });

    socket.addEventListener('message', (event) => {
        const msg = event.data;
        console.log('msg:', msg);

        const parsedData = JSON.parse(msg);
        console.log('parsedData:', parsedData);

        const courseName = parsedData.courseName;
        const providerName = parsedData.providerName;

        const courseElement = document.createElement('div');
        courseElement.innerHTML = `${courseName} 發送成功 - 提供者：${providerName}`;
        document.getElementById('SubmitConfirmation').appendChild(courseElement);
    });

    window.submitCourse4OneCourse = function() {
        const courseCategory = document.getElementById('CourseCategory').value;
        const courseName = document.getElementById('CourseName').value;
        const courseContent = document.getElementById('CourseContent').value;
        const providerName = document.getElementById('providerName').value;
        const confirmationElement = document.getElementById('SubmitConfirmation');

        confirmationElement.innerHTML = `${courseName} 發送成功 - 提供者：${providerName}`;

        data = {
            'courseCategory': courseCategory,
            'courseName': courseName,
            'courseContent': courseContent,
            'providerName': providerName
        }

        socket.send(JSON.stringify(data));

        document.getElementById('CourseName').value = '';
        document.getElementById('CourseContent').value = '';
    }
}
