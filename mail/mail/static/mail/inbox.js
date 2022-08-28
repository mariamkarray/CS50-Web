
document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

   // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
 
  // Send Mail
  document.querySelector('#compose-form').onsubmit = () =>
  {
    
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
        })
      })  
      .then(response => response.json())
      .then(result => {
        console.log(result);
      })
      return false;
  }
 
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  var view = document.getElementById('emails-view').getElementsByClassName('list-group list-group-flush')[0];
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch('/emails/inbox')
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
        const element = document.createElement('div');
        console.log(email);
        element.innerHTML = `&nbsp; <strong> ${email.sender} </strong> 	&nbsp;&nbsp;&nbsp;&nbsp; ${email.subject}`;
        element.style.border = "1px solid rgba(1, 1, 1, .3)";
        element.style.padding = "7px";
        document.querySelector("#emails-view").append(element);
        const element2 = document.createElement('div2');
        element2.innerHTML = `&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp${email.timestamp}`;
        element2.style.opacity = "0.5";
        element2.style.textAlign ="right";
        element.innerHTML += element2.textContent;
        if (email.read)
        element.style.backgroundColor = "#F8F8F8";
        
    });
  })
}