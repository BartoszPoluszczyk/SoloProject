const form = document.querySelector('form');
const errorMessage = document.querySelector('#error-message');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;

    // TO DO: implement your login logic here
    // For now, just display an error message
    errorMessage.textContent = 'Błędne dane logowania';
});