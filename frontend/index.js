// const fetch_addy = "http://127.0.0.1:5000/login";
// async function sendData(form) {
//     // Associate the FormData object with the form element
//     const formData = new FormData(form);
//     // console.log(formData.entries());

//     try {
//         let username = docuemnt.getElementById("user").value;
//         let password = document.getElementById("pass").value;

//         const response = await fetch(fetch_addy, {
//             method: "POST",
//             mode: 'cors',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: {
//                 'user': username,
//                 'pass': password
//             }
//         });
//         console.log(await response.json());
//     } catch (e) {
//         console.error(e);
//     }
// }

// window.addEventListener("DOMContentLoaded", (event) => {
//     let loginForm = document.getElementById("loginForm");

//     if (loginForm) {
//         loginForm.addEventListener("submit", (e) => {
//             e.preventDefault();
//             sendData(loginForm);
//         });
//     }
    
// });