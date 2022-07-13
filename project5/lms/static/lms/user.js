document.addEventListener('DOMContentLoaded', () => {
    let user = document.querySelector('#user').innerHTML;

    fetch(`/courses/${user}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(addCourse);
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
