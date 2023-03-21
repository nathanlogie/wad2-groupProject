
    function checkPassword(password) {
        const regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
        return regex.test(password);
    }

  function login() {
    const form = document.getElementById('registration-form')
    const password = document.getElementById('password').value;
    if (checkPassword(password)) {
      alert('Login successful!');
      form.submit()
    } else {
      alert('Invalid password!');
    }
  }