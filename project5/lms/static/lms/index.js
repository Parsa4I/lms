document.addEventListener('DOMContentLoaded', () => {
    let user = document.querySelector('#user').innerHTML;

    fetch(`/courses/${user}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(addCourse);
    })

    fetch(`/index-homeworks`)
    .then(response => response.json())
    .then(data => {
        data.forEach(addHomework);
    })
})

function addCourse(thiscourse) {
    const courseCards = document.querySelector('#course-cards');
    let cardLink = document.createElement('a');
    cardLink.href = `/course/${thiscourse.pk}`;
    let card = document.createElement('div');
    card.className = 'card mb-3 bg-light text-dark';
    card.innerHTML = `<div class="card-header">${thiscourse.course_id}</div>
        <div class="card-body">
            <h5 class="card-title">${thiscourse.course_name}</h5>
        </div>`;
    cardLink.append(card);
    courseCards.append(cardLink);
}

function addHomework(homework) {
    const homeworkCards = document.querySelector('#homework-cards');
    let cardLink = document.createElement('a');
    cardLink.href = `/homework/${homework.pk}`;
    let card = document.createElement('div');
    card.className = 'card mb-3 bg-light text-dark';
    card.innerHTML = `<div class="card-header">${homework.title}</div>
        <div class="card-body">
            <div class="card-title">${homework.duedate} | ${homework.duetime}</div>
            <div class="card-text">${homework.description}</div>
        </div>`;

    cardLink.append(card);
    homeworkCards.append(cardLink);
}
