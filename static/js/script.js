window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};
document.getElementById('venue-form').onsubmit = (e) => {
  e.preventDefault();
  var select = document.querySelector('.genres');
  var selected = [...select.options]
                    .filter(option => option.selected)
                    .map(option => option.value);
  console.log(selected, 3290);
  const data = new FormData(event.target);
  
  const formData = Object.fromEntries(data.entries());
  formData['genres'] = selected;
  console.log(formData);
  fetch('/venues/create', {
    method: 'POST',
    body: JSON.stringify(formData),
    headers:{
      'Content-Type': 'application/json'
    }
  }).then(response => {
    
  })
}