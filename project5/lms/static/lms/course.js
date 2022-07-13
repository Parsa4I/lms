document.addEventListener('DOMContentLoaded', () => {
    let courseId = parseInt(document.querySelector('#course-id').innerHTML)-1000;
    fetch(`/course/${courseId}/homework`)
    .then(response => response.json())
    .then(data => {
        data.forEach(addHomework);
    })
})

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