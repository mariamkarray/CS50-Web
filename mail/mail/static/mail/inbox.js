document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // By default, load the inbox
  load_mailbox('inbox');
});

function reply_compose_email(email) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-mail').style.display = 'none';

   // Fill out composition fields
   document.querySelector('#compose-recipients').value = email.sender;
   document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
   document.querySelector('#compose-body').value = `On ${email.timestamp} <${email.sender}> wrote: "${email.body}"\n\n`;
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-mail').style.display = 'none';

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
  document.querySelector('#view-mail').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  // inbox
 if (mailbox === 'inbox') {
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email => {
        const element = show_inbox_helper(email);
        element.addEventListener('click', function() {
        view_mail(email);
        });
      })
    });
}
// archive
else if (mailbox === 'archive') {
      fetch('/emails/archive')
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email => {
        const element = show_inbox_helper(email);
        element.addEventListener('click', function() {
        view_mail(email, email.id);
        });
      })
    });
  }

  // sent
  else if (mailbox === 'sent') {
    fetch('/emails/sent')
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      console.log(email);
      const element = show_inbox_helper(email);
      element.addEventListener('click', function() {
      view_mail(email, email.id);
      });
    })
  });
}
}


function show_inbox_helper(email) {
  // create div that contains each email
  const element = document.createElement('div');
  element.innerHTML = `&nbsp; <strong> ${email.sender} </strong> 	&nbsp;&nbsp;&nbsp;&nbsp; ${email.subject}`;
  element.style.border = "1px solid rgba(1, 1, 1, .3)";
  element.style.padding = "7px";
  if (email.read)
      element.style.backgroundColor = "#F8F8F8";
  document.querySelector("#emails-view").append(element);
  // mousevover and mouseout color change
  element.addEventListener('mouseover', function() {
    element.style.border = "2px solid #333333"
    });
element.addEventListener('mouseout', function() {
    element.style.border = "1px solid rgba(1, 1, 1, .3)"
    });
    // returning element so it can be updated 
  return element;
}

function view_mail(email) {
          id = email.id;
          document.querySelector('#view-mail').style.display = 'block';
          document.querySelector('#emails-view').style.display = 'none';
          
          fetch(`/emails/${id}`)
          .then(response => response.json())
          .then(email => {
            document.querySelector('#from').innerHTML = email.sender;
            document.querySelector('#to').innerHTML = email.recipients;
            document.querySelector('#subject').innerHTML = email.subject;
            document.querySelector('#date').innerHTML = email.timestamp;
            document.querySelector('#body').innerHTML = email.body;
            // mark as read
            fetch(`/emails/${id}`, {
              method: 'PUT',
              body: JSON.stringify({
                read: true
              })
            })
            // archive
            archive_button = document.querySelector('#archive');
            if (email.archived) {
              archive_button.innerHTML = "Unarchive";
              archive_button.addEventListener('click', function() {
                // mark as unarchived
                fetch(`/emails/${id}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                    archived: false
                  })
                })
                load_mailbox('inbox');
                location.reload();
              })
            }
            else {
            archive_button.innerHTML = "Archive";
            archive_button.addEventListener('click', function() {
              // mark as archived
              fetch(`/emails/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  archived: true
                })
              })
              load_mailbox('inbox');
              location.reload();
            })
          }
          // reply
          reply_button = document.querySelector('#reply');
          reply_button.addEventListener('click', () => {
            reply_compose_email(email);
          })
        })
}
