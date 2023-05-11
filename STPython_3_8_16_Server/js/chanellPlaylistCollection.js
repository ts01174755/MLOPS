function initChannelPlaylistCollection() {
    const socket = new WebSocket('ws://' + location.host + '/stCloudCourse/ytChannelPlaylistCollection/ws');
    const courseName_ = document.getElementById('CourseName').value;

    socket.addEventListener('open', () => {
        console.log('WebSocket connection opened');
    });

    window.submitCourse = function() {
        const courseCategory = document.getElementById('CourseCategory').value;
        const courseName = document.getElementById('CourseName').value;
        const courseUrl = document.getElementById('CourseUrl').value;
        const courseContent = document.getElementById('CourseContent').value;
        const providerName = document.getElementById('providerName').value;

        data = {
            'courseCategory': courseCategory,
            'courseName': courseName,
            'courseUrl': courseUrl,
            'courseContent': courseContent,
            'providerName': providerName
        }
        socket.send(JSON.stringify({action: 'submit_course', data: data}));
        document.getElementById('CourseName').value = '';
        document.getElementById('CourseUrl').value = '';
        document.getElementById('CourseContent').value = '';

        document.getElementById('loadingMessage').style.display = 'block';
        document.getElementById('loadingMessage').innerText = 'Loading...0s';
        loadingTime = 0;
        loadingInterval = setInterval(() => {
            loadingTime += 1;
            document.getElementById('loadingMessage').innerText = `Loading...${loadingTime}s`;
        }, 1000);

        const progressBar = document.getElementById('progressBar');
        const progressIndicator = progressBar.getElementsByTagName('div')[0];
        progressIndicator.style.width = '0%';
        document.getElementById('progressText').innerText = '';
        progressBar.style.display = 'block';
    }

    socket.addEventListener('message', (event) => {
        const msg = event.data;
        const parsedData = JSON.parse(msg);

        if (parsedData.hasOwnProperty('progress')) {
            const progress = parsedData.progress;
            const percent = parsedData.percent;
            console.log('Progress:', progress, 'Percent:', percent);

            const progressBar = document.getElementById('progressBar');
            const progressIndicator = progressBar.getElementsByTagName('div')[0];
            progressIndicator.style.width = percent + '%';

            const progressText = document.getElementById('progressText');
            progressText.innerText = `已收集 ${progress} 個影片資料 (${percent}%)`;

            document.getElementById('loadingMessage').style.display = 'none';
            clearInterval(loadingInterval);
            loadingTime = 0;
        }

        document.getElementById('loadingMessage').style.display = 'none';
        clearInterval(loadingInterval);
        loadingTime = 0;
    });
}
