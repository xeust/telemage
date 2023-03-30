const addBtn = document.querySelector('.add-id-btn');
const submBtn = document.querySelector('.submit-btn');
const idList = document.querySelector('.id-list');

addBtn.addEventListener('click', () => {
    const li = document.createElement('li');
    const input = document.createElement('input');
    addBtn.classList.add('hidden');
    submBtn.classList.remove('hidden');
    input.type = 'text';
    input.placeholder = 'Enter new chat ID';
    li.appendChild(input);
    idList.insertBefore(li, addBtn.parentNode);

    function handleSubmit(event) {
        event.preventDefault();
        submBtn.removeEventListener('click', handleSubmit);

        const value = input.value.trim();
        if (value !== '') {
            fetch('/authorize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ new_id: Number(value) })
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Failed to add chat ID!');
                    }
                })
                .then(_ => {
                    const newLi = document.createElement('li');
                    newLi.textContent = value;
                    idList.insertBefore(newLi, li);
                    input.value = '';
                    input.remove();
                    addBtn.classList.remove('hidden');
                    submBtn.classList.add('hidden');
                    submBtn.addEventListener('click', handleSubmit);
                })
                .catch(error => {
                    console.error(error);
                    submBtn.addEventListener('click', handleSubmit);
                });
        }
    }

    input.addEventListener('change', handleSubmit);
    submBtn.addEventListener('click', handleSubmit);
    input.focus();
});
