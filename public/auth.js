const addAuthBtn = document.querySelector('.add-id-btn')
const idList = document.querySelector('.id-list')


addAuthBtn.addEventListener('click', function () {
    const li = document.createElement('li');
    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Enter new chat ID';
    li.appendChild(input);
    idList.insertBefore(li, addAuthBtn.parentNode);

    input.addEventListener('change', function () {
        const value = input.value.trim();
        if (value !== '') {

            fetch('/authorize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ new_id: Number(value) })
            })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error(error));
            const newLi = document.createElement('li');
            newLi.textContent = value;
            idList.insertBefore(newLi, li);
            input.value = '';
            input.remove()
        }
    });
    input.focus()

});