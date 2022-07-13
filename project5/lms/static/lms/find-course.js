document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#search-btn').addEventListener('click', search);
})

function search() {
    const courseCards = document.querySelector('#course-cards');
    courseCards.innerHTML = '';
    let searchbar = document.querySelector('#search-bar');
    q = searchbar.value;
    fetch(`public-courses/${q}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(addCourse);
    })
}

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