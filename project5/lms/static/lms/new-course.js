document.addEventListener('DOMContentLoaded', () => {
    try {
        document.querySelector('#course-type').onclick = password_input;    
        document.querySelector('#course-type').checked = false;
    }
    catch {
        console.log('Student new course');
    }
})

function password_input() {
    try {
        let courseType = document.querySelector('#course-type');
        if (courseType.checked) {
            document.querySelector('#course-password').style.display = '';
            document.querySelector('#course-password').required = true;
        }
        else {
            document.querySelector('#course-password').style.display = 'none';
            document.querySelector('#course-password').required = false;
        }
    }
    catch {
        console.log('Student new course');
    }
}