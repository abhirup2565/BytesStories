const container = document.querySelector('.main_container');
const registerBtn =document.querySelector('.register-btn');
const loginBtn =document.querySelector('.login-btn');

registerBtn.addEventListener('click',()=>{
    container.classList.add('active');
});

loginBtn.addEventListener('click',()=>{
    container.classList.remove('active');
});