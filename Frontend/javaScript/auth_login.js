//error right now 
// does not provide error when entering nothing into login box
// hello in email field and anything in password should say please enter a valid email address
async function handleLogin(){
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');

    //basic validation
    //1. frontend valiadation (isntant feedback)

    // FIX: Check if the boxes exist AND if they are empty
    if(!emailField || !passwordField || !emailField.value || !passwordField.value){
        showError('Please fill in all fields');
        return;
    }
    const email = emailField.value.trim();
    const password = passwordField.value;

    if(!isValidEmail(email)){
        showError('Please enter a valid email');
        return;
    }

    if (password.length <8){
        showError('Password must be at least 8 characters');
        return;
    }
    //2. connect/send to backend
    
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
    const err = document.getElementById('login-error');

    if(err){
        err.textContent = message; 

    }else{
        alert(message); //Fallback so you still see the error if HTML is broken
    }
}

// This function handles the "Switching" between Login and Signup views
function toggle_signup(which){
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    
    //check 'which' side the user wants to see
    if(which === 'signup'){
        // FIX: Use the variables you defined above
        if(loginForm) loginForm.style.display = 'none';
        if(signupForm) signupForm.style.display = 'block';
    }else{
        //hide signup, show login
        if(signupForm) signupForm.style.display = 'none';
        if(loginForm) loginForm.style.display = 'block'; 
    }
}

// FIX: Added 'async' here so the 'await fetch' works
async function handle_signup(){
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;
    const confirm = document.getElementById('signup-confirm').value;
    
    
    const display_name = email.split('@')[0];
    // 1. frontend validation (instant feedback)
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
    // 2. Connect/send to backend
    try {
        const response = await fetch('http://127.0.0.1:8000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                email: email, 
                password: password, 
                display_name: email.split('@')[0] //display name is everything to the left of the @ on your email
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Account created! You can now login.");
            toggle_signup('login'); // Switch them back to login screen
        } else {
            show_signup_error(data.detail || "Signup failed");
        }
    } catch (error) {
        show_signup_error("Could not connect to server. Is your Python backend running?");
    }
    console.log('signup Attempt: ', email);
}

function show_signup_error(message){
    const err = document.getElementById('signup-error');
        if (err) {
            err.textContent = message;
        } else {
            alert(message); //fall back
        }
    }