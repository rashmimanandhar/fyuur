window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};
document.getElementById('venue-form').onsubmit = (e) => {
  e.preventDefault();
  console.log(e);
  const data = new FormData(event.target);
  
  const formData = Object.fromEntries(data.entries());
  console.log(formData);
  console.log(JSON.stringify(formData));
  fetch('/venues/create', {
    method: 'POST',
    body: JSON.stringify(formData),
    headers:{
      'Content-Type': 'application/json'
    }
  }).then(response => {
    
  })
}