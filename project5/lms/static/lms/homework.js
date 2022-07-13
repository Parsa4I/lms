document.addEventListener('DOMContentLoaded', () => {
    let hw_id = document.querySelector('#pk').innerHTML
    fetch(`/submited-homework/${hw_id}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(addSubmitedHomework);
    })
})

function addSubmitedHomework(submited) {
    const submitedHomework = document.querySelector('#submited-homework');
    let card = document.createElement('div');
    card.className = 'card mb-3 bg-light text-dark';
    card.innerHTML = `<div class="card-header"><a href="/user/${submited.student.pk}">${submited.student.username}</a></div>
        <div class="card-body">
            <a href="/download/${submited.file}" download>download submited file</a>
            <a href="/give-score/${submited.pk}">
                <button type="button" class="btn btn-dark btn-sm">Give Score</button>
            </a>
        </div>
    `;
    submitedHomework.append(card);
}
