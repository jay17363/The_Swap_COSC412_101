//error right now 
// does not provide error when entering nothing into login box
// hello in email field and anything in password should say please enter a valid email address
function handleLogin(){
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    //basic validation
    if(!email || !password){
        showError('Please fill in all fields');
        return;
    }

    if(!isValidEmail(email)){
        showError('Please enter a valid email');
        return;
    }

    if (password.length <6){
        showError('Password must be at least 6 characters');
        return;
    }

    // TODO: send to Python backend
    // fetch('/api/login', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ email, password })
    // })
    // .then(res => res.json())
    // .then(data => {
    //   if (data.success) window.location.href = '/dashboard';
    //   else showError(data.message);
    // });
    console.log('Login attempt: ', email);
}
function isValidEmail(email){
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    //regex 
    //^ -> start of the string 
    //[^\s@]+ -> one or more characters that are NOT a space or @
    //@ -> must have an @ symbol
    //[^\s@]+ - ? one or more character that are not a space or @
    //\. must have a dot
    //[^\s@]+ -> one or more characters that are NOT a space or @
    //$ -> end of the string
}

function showError(message){
    let err = document.getElementById('login-error');

    if(!err){
        err= document.createElement('p');
        err.id = 'login-error';
        err.style.cssText = 'color: red; margin-top: 10px;';
        document.querySelector('.login-box').appendChild(err);

    }
    err.textContent = message;
}

function toggle_signup(which){
    if(which === 'signup'){
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('signup-form').style.display = 'block';
    }else{
        document.getElementById('signup-form').style.display = 'none';
        document.getElementById('login-form').style.display = 'block'; 
    }
}
function handle_signup(){
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;
    const confirm = document.getElementById('signup-confirm').value;

    if (!email || !password || !confirm) {
        show_signup_error('Please fill in all fields.');
        return;
    }if(!isValidEmail(email)){
        show_signup_error('Please eneter a valid email address.');
        return;
    }if (password.length < 6) {
        show_signup_error('Password must be at least 6 characters.');
        return;
    }if (!/[A-Z]/.test(password)) {
        show_signup_error('Password must contain at least one uppercase letter.');
        return;
    }if (!/[0-9]/.test(password)) {
        show_signup_error('Password must contain at least one number.');
        return;
    }if (!/[^A-Za-z0-9]/.test(password)) {
        show_signup_error('Password must contain at least one special character.');
        return;
    }if(password !== confirm){
        show_signup_error('Passwords do not match.');
        return;
    }
    //TODO: send to python backend
    console.log('signup Attempt: ', email);
}

function show_signup_error(message){
    document.getElementById('signup-error').textContent = message;
}



